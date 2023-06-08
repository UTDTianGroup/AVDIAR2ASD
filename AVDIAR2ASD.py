"""
This file is used to create the ASD labels for the AVDIAR dataset
"""

import sys
import os
import argparse
import csv
from tools.csv_tools import read_all_rows, write_all_rows
from tools.avdiar_tools import reorder_rows_by_personID, readVideoProperties, read_speech_durations
from tools.cleanData import filter_list_by_regex
import glob, subprocess, tqdm, pandas
from scipy.io import wavfile
import cv2, numpy

#Method to read the input arguments
def parseArgs():
    parser = argparse.ArgumentParser(description = "Code to convert AVDIAR Labels to ASD Labels")
    parser.add_argument('--dataPathAVDIAR',  type=str, default="/mnt/data/datasets/AVDIAR/AVDIAR_All/", help='Path of the root directory of AVDIAR dataset.')
    parser.add_argument('--dataPathAVDIAR_ASD',  type=str, default="/mnt/data/datasets/AVDIAR_ASD/", help='Path to save the AVDIAR dataset in the AVA Active Speaker dataset format.')

    args = parser.parse_args()

    return args

class AVDIAR2ASD():

    def __init__(self, AVDIAR_Path, ASD_Path):
        self.source_dir = AVDIAR_Path
        self.target_dir = ASD_Path
        
        os.makedirs(self.target_dir, exist_ok=True)

    def createASDLabelCsv(self):
        csvDir = os.path.join(self.target_dir, 'csv')
        os.makedirs(csvDir, exist_ok=True)

        csvFilePath = os.path.join(csvDir, 'all_labels.csv') #File to save original path of all 
        
        with open(csvFilePath,'w') as csvfile:
            csvwriter = csv.writer(csvfile)

            first_row = ['video_id','frame_timestamp','entity_box_x1','entity_box_y1','entity_box_x2','entity_box_y2','label','entity_id','label_id','instance_id']
            csvwriter.writerow(first_row)

            allVidNames = os.listdir(self.source_dir)
            allVidNames = filter_list_by_regex(allVidNames, 'Seq[0-9][0-9]-[0-5]P-S[0-9]M[0-9]')
            for vidName in allVidNames:
                video_id = vidName
                _, _, _, _, fps, _, _, W, H = readVideoProperties(os.path.join(self.source_dir, video_id, 'summary.json'))

                rttm_file_path = os.path.join(self.source_dir, video_id, 'GroundTruth/speakers.rttm')
                numPersons = int(video_id.split('-')[1][0])
              
                person_speech_durations = read_speech_durations(rttm_file_path, numPersons)
                face_bb_file_path = os.path.join(self.source_dir, video_id, 'GroundTruth/face_bb.txt')
                face_bbs_all_rows = read_all_rows(face_bb_file_path)
                
                face_bbs_rows_reordered = reorder_rows_by_personID(face_bbs_all_rows, 0, 1, num_persons=numPersons)
                instance_count = 0 #For each entity, instance_count increments each time the label changes
                prevEntityID = None
                for face_bb_row in face_bbs_rows_reordered:
                    frame_number = int(face_bb_row[0])
                    p_id = int(face_bb_row[1])
                    entity_box_x1 = int(float(face_bb_row[2]))
                    entity_box_y1 = int(float(face_bb_row[3]))
                    entity_box_w = int(float(face_bb_row[4]))
                    entity_box_h = int(float(face_bb_row[5]))
                    entity_box_x2 = entity_box_x1 + entity_box_w
                    entity_box_y2 = entity_box_y1 + entity_box_h
                    time_stamp = frame_number/fps

                    #Converting to fraction
                    entity_box_x1 = entity_box_x1/W 
                    entity_box_y1 = entity_box_y1/H
                    entity_box_x2 = entity_box_x2/W
                    entity_box_y2 = entity_box_y2/H 
                    
                    if person_speech_durations:
                        
                        current_speech_durations = person_speech_durations[p_id]
                        
                        if len(current_speech_durations)>0:
                            if time_stamp < current_speech_durations[0][0]:
                                label_id = 0 #Current timestamp is before the first speech duration
                            else:
                                for dur in current_speech_durations:
                                    start_time = dur[0]
                                    end_time = dur[1]
                                    if time_stamp > end_time:
                                        continue
                                    elif time_stamp >= start_time:
                                        label_id = 1
                                        break
                                    else:
                                        label_id = 0
                                        break
                        else:
                            label_id=0
                    else:
                        label_id=0

                    if label_id==0:
                        label='NOT_SPEAKING'
                    elif label_id==1:
                        label='SPEAKING_AUDIBLE'
                    else:
                        print('Something is wrong. Program should not be executing this line.')
                        sys.exit()
                    
                    entity_id = video_id + '_' + face_bb_row[-1]
                    if prevEntityID is not None:
                        if entity_id == prevEntityID:
                            if prevLabelID != label_id:
                                prevLabelID = label_id
                                instance_count += 1
                        else:
                            prevEntityID = entity_id
                            prevLabelID = label_id
                            instance_count=0
                    else:
                        prevEntityID = entity_id
                        prevLabelID = label_id
                    instance_id = entity_id+'_'+str(instance_count)
                    row_to_write = [video_id, time_stamp, entity_box_x1, entity_box_y1, entity_box_x2, entity_box_y2, label, entity_id, label_id, instance_id]
                    csvwriter.writerow(row_to_write)

    def copyOrigVideos(self):
        allVidNames = os.listdir(self.source_dir)
        allVidNames = filter_list_by_regex(allVidNames, 'Seq[0-9][0-9]-[0-5]P-S[0-9]M[0-9]')
        dest_dir = os.path.join(self.target_dir, 'orig_videos')
        os.makedirs(dest_dir, exist_ok=True)
        for video_name in allVidNames:
            src_video_path = os.path.join(self.source_dir, video_name, 'Video', video_name+'_CAM1.mp4')
            dest_video_path = os.path.join(dest_dir, video_name+'.mp4')
            cmd = 'cp '+src_video_path+' '+dest_video_path
            os.system(cmd)

    def extractOrigAudio(self):
        orig_audio_dir = os.path.join(self.target_dir, 'orig_audios')
        os.makedirs(orig_audio_dir, exist_ok=True)
        videos = glob.glob("%s/*"%(os.path.join(self.target_dir, 'orig_videos')))
        for videoPath in tqdm.tqdm(videos):
            audioPath = '%s/%s'%(orig_audio_dir, videoPath.split('/')[-1].split('.')[0] + '.wav')
            cmd = ("ffmpeg -y -i %s -async 1 -ac 1 -vn -acodec pcm_s16le -ar 16000 -threads 8 %s -loglevel panic" % (videoPath, audioPath))
            subprocess.call(cmd, shell=True, stdout=None)

    def extract_audio_clips(self):
        # Take 3 minutes to extract the audio clips
        dic = {'train':'train', 'val':'val', 'test':'test'}
        for dataType in ['train', 'val', 'test']:
            df = pandas.read_csv(os.path.join(self.target_dir, 'csv', '%s_labels.csv'%(dataType)), engine='python')
            dfNeg = pandas.concat([df[df['label_id'] == 0], df[df['label_id'] == 2]])
            dfPos = df[df['label_id'] == 1]
            insNeg = dfNeg['instance_id'].unique().tolist()
            insPos = dfPos['instance_id'].unique().tolist()
            df = pandas.concat([dfPos, dfNeg]).reset_index(drop=True)
            df = df.sort_values(['entity_id', 'frame_timestamp']).reset_index(drop=True)
            entityList = df['entity_id'].unique().tolist()
            df = df.groupby('entity_id')
            audioFeatures = {}
            outDir = os.path.join(self.target_dir, 'clips_audios', dataType)
            audioDir = os.path.join(self.target_dir, 'orig_audios')
            for l in df['video_id'].unique().tolist():
                d = os.path.join(outDir, l[0])
                if not os.path.isdir(d):
                    os.makedirs(d)
            for entity in tqdm.tqdm(entityList, total = len(entityList)):
                insData = df.get_group(entity)
                videoKey = insData.iloc[0]['video_id']
                start = insData.iloc[0]['frame_timestamp']
                end = insData.iloc[-1]['frame_timestamp']
                entityID = insData.iloc[0]['entity_id']
                insPath = os.path.join(outDir, videoKey, entityID+'.wav')
                if videoKey not in audioFeatures.keys():                
                    audioFile = os.path.join(audioDir, videoKey+'.wav')
                    sr, audio = wavfile.read(audioFile)
                    audioFeatures[videoKey] = audio
                audioStart = int(float(start)*sr)
                audioEnd = int(float(end)*sr)
                audioData = audioFeatures[videoKey][audioStart:audioEnd]
                wavfile.write(insPath, sr, audioData)

    def train_val_split(self, all_labels_file_name='all_labels.csv', trainSplitFactor=0.7, valSplitFactor=0.1, testSplitFactor=0.2):
        #Method to split the labels into train, val and test sets.
        all_labels_path = os.path.join(self.target_dir, 'csv', all_labels_file_name)
        all_labels_rows = read_all_rows(all_labels_path)
        all_labels_rows = all_labels_rows[1:] #Removing the header
        totalRows = len(all_labels_rows)
        numTrainRows = int(trainSplitFactor*totalRows)
        numValRows = int(valSplitFactor*totalRows)
        numTestRows = int(testSplitFactor*totalRows)
        trainRows = all_labels_rows[0:numTrainRows]
        valRows = all_labels_rows[numTrainRows:numTrainRows+numValRows]
        testRows = all_labels_rows[numTrainRows+numValRows:]
        trainLabelsPath = os.path.join(self.target_dir, 'csv', 'train_labels.csv')
        valLabelsPath = os.path.join(self.target_dir, 'csv', 'val_labels.csv')
        testLabelsPath = os.path.join(self.target_dir, 'csv', 'test_labels.csv')
        first_row = ['video_id','frame_timestamp','entity_box_x1','entity_box_y1','entity_box_x2','entity_box_y2','label','entity_id','label_id','instance_id']
        write_all_rows(trainLabelsPath, trainRows, header=first_row)
        write_all_rows(valLabelsPath, valRows, header=first_row)
        write_all_rows(testLabelsPath, testRows, header=first_row)

    def extract_video_clips(self):
    
        dic = {'train':'train', 'val':'train', 'test':'test'}
        for dataType in ['train', 'val', 'test']:
            df = pandas.read_csv(os.path.join(self.target_dir, 'csv', '%s_labels.csv'%(dataType)))
            dfNeg = pandas.concat([df[df['label_id'] == 0], df[df['label_id'] == 2]])
            dfPos = df[df['label_id'] == 1]
            insNeg = dfNeg['instance_id'].unique().tolist()
            insPos = dfPos['instance_id'].unique().tolist()
            df = pandas.concat([dfPos, dfNeg]).reset_index(drop=True)
            df = df.sort_values(['entity_id', 'frame_timestamp']).reset_index(drop=True)
            entityList = df['entity_id'].unique().tolist()
            df = df.groupby('entity_id')
            outDir = os.path.join(self.target_dir, 'clips_videos', dataType)
            
            for l in df['video_id'].unique().tolist():
                d = os.path.join(outDir, l[0])
                if not os.path.isdir(d):
                    os.makedirs(d)
            for entity in tqdm.tqdm(entityList, total = len(entityList)):
                insData = df.get_group(entity)
                videoKey = insData.iloc[0]['video_id']
                entityID = insData.iloc[0]['entity_id']
                videoDir = os.path.join(self.target_dir, 'orig_videos')
                videoFile = glob.glob(os.path.join(videoDir, '{}.*'.format(videoKey)))[0]
                V = cv2.VideoCapture(videoFile)
                insDir = os.path.join(os.path.join(outDir, videoKey, entityID))
                if not os.path.isdir(insDir):
                    os.makedirs(insDir)
                j = 0
                for _, row in insData.iterrows():
                    imageFilename = os.path.join(insDir, str("%.2f"%row['frame_timestamp'])+'.jpg')
                    V.set(cv2.CAP_PROP_POS_MSEC, row['frame_timestamp'] * 1e3)
                    _, frame = V.read()
                    h = numpy.size(frame, 0)
                    w = numpy.size(frame, 1)
                    x1 = int(row['entity_box_x1'] * w)
                    y1 = int(row['entity_box_y1'] * h)
                    x2 = int(row['entity_box_x2'] * w)
                    y2 = int(row['entity_box_y2'] * h)
                    face = frame[y1:y2, x1:x2, :]
                    j = j+1
                    cv2.imwrite(imageFilename, face)

if __name__=="__main__":
    args = parseArgs()

    Conv2ASDOb = AVDIAR2ASD(args.dataPathAVDIAR, args.dataPathAVDIAR_ASD)

    # Conv2ASDOb.createASDLabelCsv()
    # Conv2ASDOb.train_val_split()
    # Conv2ASDOb.copyOrigVideos()
    # Conv2ASDOb.extractOrigAudio()
    # Conv2ASDOb.extract_audio_clips()
    Conv2ASDOb.extract_video_clips()
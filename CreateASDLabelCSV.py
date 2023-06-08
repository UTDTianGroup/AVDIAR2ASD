"""
This file is used to create the ASD labels for the AVDIAR dataset
"""

import sys
import os
import argparse
import csv
from tools.csv_tools import read_all_rows
from tools.avdiar_tools import reorder_rows_by_personID, readVideoProperties, read_speech_durations
from tools.cleanData import filter_list_by_regex

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

        csvFilePath = os.path.join(csvDir, 'orig.csv') #File to save original path of all 
        
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
                if video_id=='Seq29-3P-S1M0':
                    person_speech_durations = read_speech_durations(rttm_file_path, numPersons, True)
                else:
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


    def extractAudio():
        pass

    def extractFrames():
        pass

    def train_val_split():
        pass

if __name__=="__main__":
    args = parseArgs()

    Conv2ASDOb = AVDIAR2ASD(args.dataPathAVDIAR, args.dataPathAVDIAR_ASD)

    Conv2ASDOb.createASDLabelCsv()
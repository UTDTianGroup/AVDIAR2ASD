import json
import copy
from tools.csv_tools import read_all_rows

def reorder_rows_by_personID(rows, frame_col_index, id_col_index, num_persons):
    """
    Function to reorder a list of rows such that a sequence of occurrence of a person will be grouped together unless a person does not appear in two consecutive frames. This function also appends entity ID to the rows. 

    rows : Input rows to be reordered
    id_col_index : the index of the column in which the person ids exist
    num_persons : The number of persons corresponding to this list
    """

    # #If there is only person in the list then there no need to reorder the list
    # if num_persons==1:
    #     return rows
    
    reorderedRows = []
    rowAppended = [False for i in range(len(rows))] #Boolean value corresponding to each row in rows indicating whether the row has been appended to reorderedRows.

    #Create a dictionary which counts the entity ID for each person. Each set of consecutive frames of a person forms an entity. To make this simpler, I am also going to make person ID a part of entity ID. Person ID is 1-indexed.
    entity_id_count = {}
    for entity_key in range(1, num_persons+1):
        entity_id_count[entity_key] = 0

    for rowInd in range(len(rows)):

        if rowAppended[rowInd]:
            continue

        currentRow = rows[rowInd]
        currentPersonID = int(currentRow[id_col_index])
        currentFrameInd = int(currentRow[frame_col_index])
        entity_id_count[currentPersonID] = entity_id_count[currentPersonID] + 1
        currentRow.append(str(currentPersonID)+'_'+str(entity_id_count[currentPersonID]))
        reorderedRows.append(currentRow)
        rowAppended[rowInd] = True

        if rowInd + 1 != len(rows):
            for rowIndLocal in range(rowInd+1, len(rows)):

                if currentPersonID != int(rows[rowIndLocal][id_col_index]): #Let the code run only if 
                    continue

                elif int(rows[rowIndLocal][frame_col_index]) != currentFrameInd + 1:
                    break
                
                else:
                    rows[rowIndLocal].append(str(currentPersonID)+'_'+str(entity_id_count[currentPersonID]))
                    reorderedRows.append(rows[rowIndLocal])
                    rowAppended[rowIndLocal] = True
                    currentFrameInd = currentFrameInd + 1
    return reorderedRows

def readVideoProperties(jsonFilePath):
    #Funtion to Read video properties from the json file of the video
    
    fhd = open(jsonFilePath, 'r')
    data = json.load(fhd)
    video_length = float(data['Length_in_sec'])
    video_name = data['SequenceName']
    numAudioChannel = int(data['Audio_Channel'])
    audioSR = int(data['Audio_FS'])
    videoFPS = int(data['Video_FPS'])
    numImages = int(data['Number_of_Image'])
    CalibrationID=int(data['CalibrationID'])
    ImageRes = data['Image_Resoultion_WH']
    W = int(ImageRes[0])
    H = int(ImageRes[1])
    fhd.close()
    return video_length, video_name, numAudioChannel, audioSR, videoFPS, numImages, CalibrationID, W, H

def read_speech_durations(rttmFilePath, num_persons, verbose=False):
    all_speech_rows = read_all_rows(rttmFilePath, delimiter=' ')
    if verbose:
        print('all speech rows ', all_speech_rows)
    speech_durations = {}
    currentPersonID = 0
    if len(all_speech_rows)>1:
        for rowInd in range(len(all_speech_rows)):
            if verbose:
                print('rowInd ', rowInd)

            if all_speech_rows[rowInd][0] == 'SPKR-INFO':
                if verbose:
                    print('reading SPKR-INFO ', all_speech_rows[rowInd])
                if rowInd != 0:
                    speech_durations[currentPersonID] = copy.deepcopy(current_speech_durations)
                    if verbose:
                        print('appending speech durations when rowInd not 0 ', current_speech_durations)
                        print('current person id ', currentPersonID)
                        print('updated speech durations ', speech_durations)

                current_speech_durations = []
                
                nextPersonID = int(all_speech_rows[rowInd][7].split('-')[1])
                if verbose:
                    print('next person id ', nextPersonID)
                    print('current person id ', currentPersonID)
                if nextPersonID == currentPersonID + 1:
                    currentPersonID = nextPersonID
                    if verbose:
                        print('next person ID is on point ', nextPersonID)
                        print('current person id ', currentPersonID)
                else:
                    for personID in range(currentPersonID+1, num_persons+1):
                        if nextPersonID != personID:
                            
                            speech_durations[personID] = copy.deepcopy(current_speech_durations)
                            if verbose:
                                print('Supposed to be appending empty duration list ', current_speech_durations)
                                print('updated speech durations ', speech_durations)
                                print('next person id ', nextPersonID)
                                print('current person id ', currentPersonID)
                                print('person id ', personID)
                        else:
                            currentPersonID = personID
                            if verbose:
                                print('Found the rignt person after skipping some ')
                                print('speech durations ', speech_durations)
                                print('nextPersonID ', nextPersonID)
                                print('current person id ', currentPersonID)
                                print('person id ', personID)
                            break
            else:
                currentRow = all_speech_rows[rowInd]
                start_time = float(currentRow[3])
                dur = float(currentRow[4])
                end_time = start_time + dur
                current_speech_durations.append((start_time, end_time))
                if verbose:
                    print('appending to current_speech_durations ', current_speech_durations)

        speech_durations[currentPersonID] = copy.deepcopy(current_speech_durations) #For the last speaker
        if verbose:
            print('final speech durations ', speech_durations)
    return speech_durations
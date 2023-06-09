# AVDIAR2ASD
Code to relabel AVDIAR dataset for the ASD task.

This code has been tested with Python version 3.9.12

Download all the video sequences from the [AVDIAR dataset](https://team.inria.fr/perception/avdiar/).

After you download and unzip the dataset, it should have the following format.

```
AVDIAR_Root_Folder
├── Seq01-1P-S0M1
│   ├── Audio
│   │   └── Seq01-1P-S0M1.wav
│   ├── Detection
│   │   ├── face_bb.txt
│   │   └── person_bb.txt
│   ├── GroundTruth
│   │   ├── face_bb.txt
│   │   ├── person_bb.txt
│   │   ├── speakers.rttm
│   │   └── vad.rttm
│   ├── Seq01-1P-S0M1-thumbnail.png
│   ├── summary.json
│   └── Video
│       ├── Seq01-1P-S0M1_CAM1.mp4
│       └── Seq01-1P-S0M1_CAM2.mp4
├── Seq02-1P-S0M1
│   ├── Audio
│   │   └── Seq02-1P-S0M1.wav
│   ├── Detection
│   │   ├── face_bb.txt
│   │   └── person_bb.txt
│   ├── GroundTruth
│   │   ├── face_bb.txt
│   │   ├── person_bb.txt
│   │   ├── speakers.rttm
│   │   └── vad.rttm
│   ├── Seq02-1P-S0M1-thumbnail.png
│   ├── summary.json
│   └── Video
│       ├── Seq02-1P-S0M1_CAM1.mp4
│       └── Seq02-1P-S0M1_CAM2.mp4
|              .
|              .
|              .
└── Seq44-2P-S2M0
    ├── Audio
    │   └── Seq44-2P-S2M0.wav
    ├── Detection
    │   ├── face_bb.txt
    │   └── person_bb.txt
    ├── GroundTruth
    │   ├── face_bb.txt
    │   ├── person_bb.txt
    │   ├── speakers.rttm
    │   └── vad.rttm
    ├── Seq44-2P-S2M0-thumbnail.png
    ├── summary.json
    └── Video
        ├── Seq44-2P-S2M0_CAM1.mp4
        └── Seq44-2P-S2M0_CAM2.mp4
```

Run the following commands to convert AVDIAR data into an ASD dataset. We will be using an Anaconda Virtual Environment.

## Download the AVDIAR2ASD repository

```
git clone https://github.com/UTDTianGroup/AVDIAR2ASD.git
```

## Create a new environment
```
conda create -n avdiar2asd
conda activate avdiar2asd
cd AVDIAR2ASD/
pip install -r requirements.txt
```

## Command to convert AVDIAR data into an ASD dataset
Please replace the paths in the command below with paths to the AVDIAR dataset and the target folder to create the ASD dataset respectively
```
python AVDIAR2ASD.py --dataPathAVDIAR /path/to/AVDIAR_Root_Folder/ --dataPathAVDIAR_ASD /path/to/AVDIAR_ASD/
```

After running the above command the target directory should have the following directory structure
```

├── clips_audios
│   ├── test
│   │   ├── Seq01-1P-S0M1
│   │   ├── Seq02-1P-S0M1
│   │   ├── Seq03-1P-S0M1
│   │   ├── Seq04-1P-S0M1
│   │   ├── Seq06-2P-S1M0
│   │   ├── Seq07-2P-S1M0
│   │   ├── Seq18-2P-S1M1
│   │   ├── Seq20-2P-S1M1
│   │   ├── Seq27-3P-S1M1
│   │   ├── Seq29-3P-S1M0
│   │   └── Seq43-2P-S0M0
│   ├── train
│   │   ├── Seq05-2P-S1M0
│   │   ├── Seq08-3P-S1M1
│   │   ├── Seq09-3P-S1M1
│   │   ├── Seq10-3P-S1M1
│   │   ├── Seq12-3P-S1M1
│   │   ├── Seq13-4P-S2M1
│   │   ├── Seq17-2P-S1M1
│   │   ├── Seq19-2P-S1M1
│   │   ├── Seq22-1P-S0M1
│   │   ├── Seq28-3P-S1M1
│   │   ├── Seq30-3P-S1M1
│   │   ├── Seq32-4P-S1M1
│   │   └── Seq40-2P-S2M0
│   └── val
│       ├── Seq09-3P-S1M1
│       ├── Seq20-2P-S1M1
│       ├── Seq21-2P-S1M1
│       ├── Seq37-2P-S0M0
│       └── Seq44-2P-S2M0
├── clips_videos
│   ├── test
│   │   ├── Seq01-1P-S0M1
│   │   │   └── Seq01-1P-S0M1_1_1
│   │   ├── Seq02-1P-S0M1
│   │   │   └── Seq02-1P-S0M1_1_1
│   │   ├── Seq03-1P-S0M1
│   │   │   └── Seq03-1P-S0M1_1_1
│   │   ├── Seq04-1P-S0M1
│   │   │   └── Seq04-1P-S0M1_1_1
│   │   ├── Seq06-2P-S1M0
│   │   │   ├── Seq06-2P-S1M0_1_1
│   │   │   └── Seq06-2P-S1M0_2_1
│   │   ├── Seq07-2P-S1M0
│   │   │   ├── Seq07-2P-S1M0_1_1
│   │   │   └── Seq07-2P-S1M0_2_1
│   │   ├── Seq18-2P-S1M1
│   │   │   ├── Seq18-2P-S1M1_1_1
│   │   │   └── Seq18-2P-S1M1_2_1
│   │   ├── Seq20-2P-S1M1
│   │   │   ├── Seq20-2P-S1M1_1_1
│   │   │   ├── Seq20-2P-S1M1_1_2
│   │   │   ├── Seq20-2P-S1M1_2_1
│   │   │   └── Seq20-2P-S1M1_2_2
│   │   ├── Seq27-3P-S1M1
│   │   │   ├── Seq27-3P-S1M1_1_1
│   │   │   ├── Seq27-3P-S1M1_2_1
│   │   │   └── Seq27-3P-S1M1_3_1
│   │   ├── Seq29-3P-S1M0
│   │   │   ├── Seq29-3P-S1M0_1_1
│   │   │   ├── Seq29-3P-S1M0_2_1
│   │   │   └── Seq29-3P-S1M0_3_1
│   │   └── Seq43-2P-S0M0
│   │       ├── Seq43-2P-S0M0_1_1
│   │       └── Seq43-2P-S0M0_2_1
│   ├── train
│   │   ├── Seq05-2P-S1M0
│   │   │   ├── Seq05-2P-S1M0_1_1
│   │   │   └── Seq05-2P-S1M0_2_1
│   │   ├── Seq08-3P-S1M1
│   │   │   ├── Seq08-3P-S1M1_1_1
│   │   │   ├── Seq08-3P-S1M1_2_1
│   │   │   └── Seq08-3P-S1M1_3_1
│   │   ├── Seq09-3P-S1M1
│   │   │   ├── Seq09-3P-S1M1_1_1
│   │   │   └── Seq09-3P-S1M1_2_1
│   │   ├── Seq10-3P-S1M1
│   │   │   ├── Seq10-3P-S1M1_1_1
│   │   │   ├── Seq10-3P-S1M1_2_1
│   │   │   └── Seq10-3P-S1M1_3_1
│   │   ├── Seq12-3P-S1M1
│   │   │   ├── Seq12-3P-S1M1_1_1
│   │   │   ├── Seq12-3P-S1M1_2_1
│   │   │   └── Seq12-3P-S1M1_3_1
│   │   ├── Seq13-4P-S2M1
│   │   │   ├── Seq13-4P-S2M1_1_1
│   │   │   ├── Seq13-4P-S2M1_2_1
│   │   │   ├── Seq13-4P-S2M1_3_1
│   │   │   └── Seq13-4P-S2M1_4_1
│   │   ├── Seq17-2P-S1M1
│   │   │   ├── Seq17-2P-S1M1_1_1
│   │   │   └── Seq17-2P-S1M1_2_1
│   │   ├── Seq19-2P-S1M1
│   │   │   ├── Seq19-2P-S1M1_1_1
│   │   │   └── Seq19-2P-S1M1_2_1
│   │   ├── Seq22-1P-S0M1
│   │   │   └── Seq22-1P-S0M1_1_1
│   │   ├── Seq28-3P-S1M1
│   │   │   ├── Seq28-3P-S1M1_1_1
│   │   │   ├── Seq28-3P-S1M1_2_1
│   │   │   └── Seq28-3P-S1M1_3_1
│   │   ├── Seq30-3P-S1M1
│   │   │   ├── Seq30-3P-S1M1_1_1
│   │   │   ├── Seq30-3P-S1M1_2_1
│   │   │   └── Seq30-3P-S1M1_3_1
│   │   ├── Seq32-4P-S1M1
│   │   │   ├── Seq32-4P-S1M1_1_1
│   │   │   ├── Seq32-4P-S1M1_2_1
│   │   │   ├── Seq32-4P-S1M1_3_1
│   │   │   └── Seq32-4P-S1M1_4_1
│   │   └── Seq40-2P-S2M0
│   │       ├── Seq40-2P-S2M0_1_1
│   │       └── Seq40-2P-S2M0_2_1
│   └── val
│       ├── Seq09-3P-S1M1
│       │   ├── Seq09-3P-S1M1_2_1
│       │   └── Seq09-3P-S1M1_3_1
│       ├── Seq20-2P-S1M1
│       │   └── Seq20-2P-S1M1_1_1
│       ├── Seq21-2P-S1M1
│       │   ├── Seq21-2P-S1M1_1_1
│       │   └── Seq21-2P-S1M1_2_1
│       ├── Seq37-2P-S0M0
│       │   ├── Seq37-2P-S0M0_1_1
│       │   └── Seq37-2P-S0M0_2_1
│       └── Seq44-2P-S2M0
│           ├── Seq44-2P-S2M0_1_1
│           └── Seq44-2P-S2M0_2_1
├── csv
├── orig_audios
└── orig_videos
```

#!/usr/bin/env python

import sys, os
from subprocess import call
import argparse
from datetime import datetime

# Initialize
starttime = datetime.now()
runs = ["medopen", "medthink", "restnotask", "restopen", "restthink"]

# Command line options
parser = argparse.ArgumentParser()
parser.add_argument("--subjects", help="process listed subjects", nargs='+', action="store")
parser.add_argument("--all", help="process all subjects", action="store_true")
parser.add_argument("--segment", help="type of segmentation (csf or wm)", required=True)
args = parser.parse_args()

# Check segmentation type
if args.segment not in ["csf", "wm"]:
    print("Invalid segmentation type. Use 'csf' or 'wm'.")
    sys.exit()

# Set paths
pathbase = '/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/analyses/seed_fc'
pathbase2 = '/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing'

# Develop list of subjects
subjects = args.subjects

if args.all:
    subjects = os.listdir(pathbase)
    subjects = [elem for elem in subjects if 'sub-' in elem]
    subjects.sort()
    
    candidate_subjects = subjects
    subjects = []
    
    for candidate in candidate_subjects:
        testfolder1 = f"{pathbase}/segmentation/sub-{candidate}/warp_mask"
        if not os.path.exists(testfolder1):
            subjects.append(candidate[4:7])

if subjects:
    print(subjects)
else:
    print("Subjects must be specified. Use --all for all subjects or --subjects to list specific subjects.")
    sys.exit()

# Segmentation steps
for subject in subjects:
    subjectfolder = f"{pathbase2}/sub-{subject}"
    for run in runs:
        runfolder = f"{pathbase2}/sub-{subject}/preproc_{run}.feat"
        inputvolume = f"{runfolder}/filtered_func_data.nii.gz"
        outputvolume = f"{runfolder}/{args.segment}_timeseries"
        maskvolume = f"{runfolder}/{args.segment}_mask.nii.gz"
        command = f"fslmeants -i {inputvolume} -o {outputvolume} -m {maskvolume}"
        print(command)
        call(command, shell=True)

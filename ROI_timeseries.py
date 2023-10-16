#!/usr/bin/env python

import sys, os
from subprocess import call
import argparse
from datetime import datetime
import re

starttime = datetime.now()

runs = ["restnotask", "restopen", "restthink"]
masks = ["AG_left", "AG_right", "AI", "AI_right", "dACC", "dACC_right", "mpfc", "mpfc_right", "pcc", "pcc_right", "SMG", "SMG_right"]

# Command line options
parser = argparse.ArgumentParser()
parser.add_argument("--subjects", help="process listed subjects", nargs='+', action="store")
parser.add_argument("--all", help="process all subjects", action="store_true")
args = parser.parse_args()

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
        testfolder1 = f"{pathbase}/segmentation/sub-{candidate[4:7]}/warp_mask"
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
        for mask_name in mask_names:
            runfolder = f"{pathbase2}/sub-{subject}/preproc_{run}.feat"
            inputvolume = f"{runfolder}/filtered_func_data.nii.gz"
            outputvolume = f"{runfolder}/{mask_name}_timeseries"
            maskvolume = f"{runfolder}/{mask_name}_mask.nii.gz"
            command = f"fslmeants -i {inputvolume} -o {outputvolume} -m {maskvolume}"
            print(command)
            call(command, shell=True)

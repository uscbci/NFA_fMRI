#!/usr/bin/env python

import sys, os
from subprocess import call
import argparse
from datetime import datetime
import re

starttime = datetime.now()

runs = ["medopen", "medthink","restnotask","restopen","restthink"]

#command line options
parser = argparse.ArgumentParser()

parser.add_argument("--subjects",help="process listed subjects",nargs='+',action="store")
parser.add_argument("--all",help="process all subjects", action="store_true")

args = parser.parse_args()

#set paths
pathbase = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI"
pathbase2 = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing"

#develop list of subjects
subjects = args.subjects

if args.all:
	#Get list of subjects
	subjects = os.listdir(pathbase)
	subjects = [elem for elem in subjects if 'sub-' in elem]
	subjects.sort()

	#check if they've been done already
	candidate_subjects = subjects
	subjects = []
	
	for candidate in candidate_subjects:
		testfolder1 = "%s/analyses/seed_fc/segmentation/sub-%s" % (pathbase,subject)	
		if not os.path.exists(testfolder1):
			subjects.append(candidate[4:7])

if subjects:
	print (subjects)
else:
	print ("Subjects must be specified. Use --all for all subjects or --subjects to list specific subjects.")
	sys.exit()

#Segmentation steps
for subject in subjects:

	subjectfolder = pathbase2 + "/sub-" + subject
	for run in runs:
		inputvolume = '%s/sub-%s_T1w_brain.nii' %(subjectfolder, subject)
		outputvolume = '/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/analyses/seed_fc/segmentation/sub-%s' %(subject)

		command = 'fast -g -o %s %s' %(outputvolume, inputvolume)
		print(command)
		call(command,shell=True)

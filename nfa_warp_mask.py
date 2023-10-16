#!/usr/bin/python

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
pathbase = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing"

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
		testfolder1 = "%s/denoised/sub-%s" % (pathbase,subjects)	
		if not os.path.exists(testfolder1):
			subjects.append(candidate[4:7])

if subjects:
	print (subjects)
else:
	print ("Subjects must be specified. Use --all for all subjects or --subjects to list specific subjects.")
	sys.exit()

#Preprocessing steps
for subject in subjects:

	subjectfolder = pathbase + "/sub-" + subject
	for run in runs:
		inputvolume = '%s/preproc_%s.feat/ICA_AROMA/denoised_func_data_nonaggr.nii' %(subjectfolder, run)
		outputvolume = '%s/denoised/sub-%s_%s' %(pathbase,subject,run)
		referencevolume = '/usr/local/fsl6/data/standard/MNI152_T1_2mm.nii.gz'
		warpfile = '%s/preproc_%s.feat/reg/example_func2standard_warp' %(subjectfolder,run)

		command = 'applywarp -i %s -o %s -r %s -w %s' %(inputvolume, outputvolume, referencevolume, warpfile)
		print(command)
		call(command,shell=True)

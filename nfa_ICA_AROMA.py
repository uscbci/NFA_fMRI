#!/usr/bin/python

# MASTER ANALYSIS SCRIPT FOR MEDITATION NARRATIVE FREE AWARENESS STUDY
# NOV 2021

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
		testfolder1 = "%s/sub-%s/preproc_restthink.feat/ICA_AROMA" % (pathbase,candidate)	
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
		featfolder = '%s/preproc_%s.feat' %(subjectfolder, run)
		outfolder = '%s/ICA_AROMA' %(featfolder)
		command = 'ICA_AROMA.py -feat %s -out %s' %(featfolder, outfolder)
		print(command)
		call(command,shell=True)

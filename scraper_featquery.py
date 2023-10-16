#!/usr/bin/env python

import sys,os
from subprocess import call, check_output
import argparse
from datetime import datetime
import re

starttime = datetime.now()

#file = open('/Users/evanabdollahi/Desktop/scraperoutput.txt', 'w')

analysislist = ["preprocess"]

runs = ["restnotask","restopen", "restthink"]
masks = ["mpfc","pcc","dACC", "AI","dlPFC", "SMG", "AG_left"]
comparisonmasks = ["mpfc","pcc","dACC","AI", "dlPFC", "SMG", "AG_left"]

#command line options
parser = argparse.ArgumentParser()

parser.add_argument("--subjects",help="process listed subjects",nargs='+',action="store")
parser.add_argument("--all",help="process all subjects", action="store_true")
args = parser.parse_args()

#set paths
pathbase = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/analyses"

#develop list of subjects
subjects = args.subjects

if args.all:
	#Get list of subjects
	subjects = os.listdir(datapath)
	subjects = [elem for elem in subjects if 'sub-' in elem]
	subjects.sort()

	#check if they've been done already
	candidate_subjects = subjects
	subjects = []

	firstdesign = analysislist[-1]
	
	for candidate in candidate_subjects:
		testfolder1 = "%s/sub-%s/preproc_restthink.feat" % (outpath,candidate)	
		if not os.path.exists(testfolder1):
			subjects.append(candidate[4:7])

if subjects:
	print (subjects)
else:
	print ("Subjects must be specified. Use --all for all subjects or --subjects to list specific subjects.")
	sys.exit()

for subject in subjects:
	for run in runs:
		for mask in masks:
			for comparisonmask in comparisonmasks:
				#output = (subject, run, mask, comparisonmask)
				#value = "_".join(output)
				#print(value)
				featqueryfolder = '/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing/sub-%s/%s_fc_%s.feat' %(subject, run, mask)
				#add _right before .feat to do right hemi
				command = "cat '%s'/'ROI_analysis_%s'/report.txt | grep stats/cope1 | awk '{print $6}'" %(featqueryfolder,  comparisonmask)
				#add _right after second %s to do right hemi
				#file.write(command)
				call(command,shell=True)
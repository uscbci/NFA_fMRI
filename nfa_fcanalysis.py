#!/usr/bin/env python

import sys,os
from subprocess import call, check_output
import argparse
from datetime import datetime
import re

starttime = datetime.now()

analysislist = ["preprocess"]

runs = ["restnotask","restthink","restopen"]
masks = ["AG_left", "AG_right", "AI", "AI_right", "dACC", "dACC_right", "mpfc", "mpfc_right", "pcc", "pcc_right", "SMG", "SMG_right"]

#command line options
parser = argparse.ArgumentParser()

parser.add_argument("--subjects",help="process listed subjects",nargs='+',action="store")
parser.add_argument("--all",help="process all subjects", action="store_true")
args = parser.parse_args()

#set paths
pathbase = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/analyses"
outpath = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/analyses"
designpath = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/analyses/designs"

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


genericfile = designpath + "/generic_fc.fsf"

for subject in subjects:

	subjectfolder = outpath + "/sub-" + subject

	for mask in masks:

		for run in runs:
				run = str(run)

				outputfile = subjectfolder + "/fc_%s_%s.fsf" % (run,mask)
					
				command = "sed -e 's/DEFINERUN/%s/g' -e 's/DEFINESUBJECT/%s/g' -e 's/DEFINEMASK/%s/g' %s > %s" % (run,subject,mask,genericfile,outputfile)
				print(command)
				call(command,shell=True)

				command = "feat " + outputfile
				print (command)
				call(command,shell=True)
#!/usr/bin/env python

import sys,os
from subprocess import call, check_output
import argparse
from datetime import datetime
import re

starttime = datetime.now()

analysislist = ["preprocess"]

runs = ["restnotask","restopen", "restthink"]
masks = ["mpfc_right", "mpfc", "pcc_right", "pcc", "dACC_right", "dACC", "dlPFC_right", "dlPFC", "AI_right", "AI", "SMG_right", "SMG", "AG_right", "AG_left"]
seeds = ["mpfc_right", "mpfc", "pcc_right", "pcc", "dACC_right", "dACC", "dlPFC_right", "dlPFC", "AI_right", "AI", "SMG_right", "SMG", "AG_right", "AG_left"]


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
	for seed in seeds:
		for mask in masks:
			for run in runs:
			
				run = str(run)
				N_featdirs = 1
				featdirs = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing/sub-%s/%s_fc_%s.feat" %(subject, run, seed)
				n_stats = 2
				stats1 = "stats/cope1 stats/cope2"
				outputrootname = 'ROI_analysis_%s' %(mask)
				mask_ref = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing/sub-%s/preproc_%s.feat/%s_mask.nii.gz" %(subject, run, mask)
				command = 'featquery %s %s %s %s %s -p -s %s' %(N_featdirs, featdirs, n_stats, stats1, outputrootname, mask_ref)
		
				print(command)
				call(command,shell=True)
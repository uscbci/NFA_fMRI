#!/usr/bin/env python

# MASTER ANALYSIS SCRIPT FOR MEDITATION NARRATIVE FREE AWARENESS STUDY
# NOV 2021

import sys,os
from subprocess import call, check_output
import argparse
from datetime import datetime
import re

starttime = datetime.now()

analysislist = ["preprocess"]

runs = ["medopen", "medthink","restnotask","restopen","restthink"]

#command line options
parser = argparse.ArgumentParser()

parser.add_argument("--subjects",help="process listed subjects",nargs='+',action="store")
parser.add_argument("--all",help="process all subjects", action="store_true")
parser.add_argument("--nopre",help="skip all preprocessing steps", action="store_true")
parser.add_argument("--nodcm",help="skip dicom conversion", action="store_true")
parser.add_argument("--nocheckfiles",help="skip dicom conversion", action="store_true")
parser.add_argument("--nofieldmap",help="skip fieldmap prep", action="store_true")
parser.add_argument("--noskullstrip",help="skip skullstripping", action="store_true")
parser.add_argument("--nologfiles",help="skip logfile processing", action="store_true")
parser.add_argument("--nofeat",help="skip feat analysis", action="store_true")
parser.add_argument("--noreg",help="skip registration copying", action="store_true")
args = parser.parse_args()

#set paths
pathbase = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI"
outpath = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing"
designpath = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing/designs"
datapath = pathbase + "/Nifti"	
logfilename = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing/logs/analysis_log.txt"

def checkImageLength(imagename):
	command = 'fslinfo %s' % imagename
	results = check_output(command,shell=True)
	TR = results.split()[9]
	return int(TR)

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

#function to check for success of feat analysis
def checkfeat(featfolder):
	testfile = featfolder + "/filtered_func_data.nii.gz" 
	print ("testfile: %s" % testfile)
	if not os.path.exists(testfile):
		print ("WARNING: ANALYSIS DID NOT COMPLETE FOR %s" % featfolder)
		logfile.write("%s: WARNING: ANALYSIS DID NOT COMPLETE FOR %s\n" % (datetime.now().strftime('%I:%M:%S%p'),featfolder))
		
def dolowerlevels(designsuffix):
	for run in runs:
		
		fmri_file = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/Nifti/sub-%s/func/sub-%s_task-%s_run-01_bold" % (subject,subject,run)
		print("Working on run %s, input file is: %s" % (run,fmri_file))

		timepoints = checkImageLength(fmri_file)
		print("Number of timepoints: %d" % timepoints)

		timepoints = str(timepoints)
		run = str(run)

		if (run == "medopen"):
			genericfile = designpath + "/" + designsuffix + "-medopen.fsf"
		else:
			genericfile = designpath + "/" + designsuffix + ".fsf"
		
		outputfile = outpath + "/sub-" + subject + "/" + designsuffix + "-" + run + ".fsf"


		
		testdir = "/Volumes/Meditation/Narrative_Free_Awareness_Study/06_Data/fMRI/preprocessing/sub-%s/preproc_%s.feat" % (subject,run)
		print ("testdir: %s" % testdir)
			
		command = "sed -e 's/DEFINERUN/%s/g' -e 's/DEFINESUBJECT/%s/g' -e 's/DEFINETIMEPOINTS/%s/g' %s > %s" % (run,subject,timepoints,genericfile,outputfile)
		call(command,shell=True)

		command = "feat " + outputfile
		print (command)
		call(command,shell=True)
	
		checkfeat(testdir)

		if (run != "medopen"):
			sourcefolder = "%s/sub-%s/preproc_medopen.feat" % (outpath,subject)
			destfolder = "%s/sub-%s/preproc_%s.feat" % (outpath,subject,run)
			command = "copyreg.sh %s %s" % (sourcefolder,destfolder)
			call(command,shell=True)

def checkImageLength(imagename):
	command = 'fslinfo %s' % (imagename)
	results = check_output(command,shell=True)
	TR = results.split()[9]
	return int(TR)

#Preprocessing steps
for subject in subjects:

	subjectfolder = outpath + "/sub-" + subject
	if not os.path.exists(subjectfolder):
		os.mkdir(subjectfolder)

	logfile = open(logfilename,'a')
	logfile.write("\n-----Analysis of subject %s started at %s\n" % (subject,starttime.strftime('%b %d %G %I:%M%p')))

	if not args.nopre:
	
		if not args.noskullstrip:
			#Skull Strip
			command = 'skullstrip.py %s/sub-%s/anat %s' % (datapath,subject,subjectfolder)
			call(command,shell=True)
		
		if not args.nofieldmap:	
			#pre-processing field maps
			command = 'setupfieldmaps.py --infolder %s/sub-%s/fmap --outfolder %s' % (datapath,subject,subjectfolder)
			call(command,shell=True)

	else:
		print ("Skipping preprocessing steps...")

	
	if not args.nofeat:	
		
		for analysis in analysislist:
			dolowerlevels(analysis)

	else:
		print ("Skipping feats...")
		
	endtime = datetime.now()
	delta = endtime - starttime
	logfile.write("-----Analysis of subject %s finished at %s, duration %s\n" % (subject,endtime.strftime('%b %d %G %I:%M%p'),str(delta)))
	logfile.close()

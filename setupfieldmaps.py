#!/usr/bin/env python

import sys,os
from subprocess import call, check_output
import argparse

#This script will prepare the fieldmap images for use in FEAT
#For unwarping in FEAT, use the following params:
#-----------------------------------------
#Fieldmap = fieldmap_phase_rads
#Fieldmap mag = fieldmap_mag_brain
#EPI echo spacing = .25 ms 
#EPI TE = 25 ms 
#deltaTE = 2.46 ms
#Unwarp direction = -y
#%Signal loss threshold = 10%


#command line options
parser = argparse.ArgumentParser()
parser.add_argument("--infolder",help="folder that contains files",action="store")
parser.add_argument("--outfolder",help="folder that contains files",action="store")
args = parser.parse_args()

infolder = args.infolder
outfolder = args.outfolder

#determine which image is which
files = os.listdir(infolder)

for file in files:
	if "magnitude1.nii.gz" in file:
		magimage = file
	if "phasediff.nii.gz" in file:
		phaseimage = file

subject = magimage[0:7]


#skull strip mag image
command= "bet %s/%s %s/%s_magnitude1_brain -B" % (infolder,magimage,outfolder,subject)
print (command)
call(command,shell = True)


#convert phase to rads
command = "fsl_prepare_fieldmap SIEMENS %s/%s %s/%s_magnitude1_brain %s/%s_phasediff_rad 2.46" % (infolder,phaseimage,outfolder,subject,outfolder,subject)
print (command)
call(command,shell = True)
#!/usr/bin/env python


from __future__ import division
import sys
import os
import nibabel as nib
import numpy as np
import scipy.stats
from subprocess import call 
from shutil import copyfile

#command line options
if (len(sys.argv) < 2):
	print("\n\tusage: %s <input folder which contains t1> <output folder>\n" % sys.argv[0])
	sys.exit()
else:
	folder = sys.argv[1]
	outfolder = sys.argv[2]	

def threshold(a, threshmin=None, threshmax=None, newval=0):
	a = np.ma.array(a, copy=True)
	mask = np.zeros(a.shape, dtype=bool)
	if threshmin is not None:
	    mask |= (a < threshmin).filled(False)

	if threshmax is not None:
	    mask |= (a > threshmax).filled(False)

	a[mask] = newval
	return a

files = os.listdir(folder)
infile = [elem for elem in files if "T1w.nii.gz" in elem]

if len(infile) > 0:
	infile = infile[0]
else:
	print("Could not find T1 image in folder")
	sys.exit()

subject = infile[0:7]
out_t1 = os.path.join(outfolder,infile)
infile = os.path.join(folder,infile)
copyfile(infile,out_t1)

#load in mprage	
img = nib.load(infile)
xdim,ydim,zdim = img.shape
data = img.get_data()

#threshold to make background zero
clipped = threshold(data,150)

#find x center
begin = 0
end = 0
for x in range(xdim):

	count = clipped[x,:,:].sum()
	#print "%d: %d" % (x,count)
	if count > 0:
		if begin==0:
			begin = x
	else:
		if begin > 0 and end==0:
			end = x
if end == 0:
	end = xdim-1

xsize = end - begin
xradius = round(xsize/2)
xcenter = xradius + begin

print("Image starts at %d and ends at %d in x dimension.  Center is at %d" % (begin,end,xcenter))

#find y center
begin = 0
end = 0
for y in range(ydim):
	count = clipped[:,y,:].sum()
	if count > 0:
		if begin==0:
			begin = y
	else:
		if begin > 0 and end==0:
			end = y
if end == 0:
	end = ydim-1

ysize = end - begin
yradius = round(ysize/2)
ycenter = yradius + begin

print("Image starts at %d and ends at %d in y dimension.  Center is at %d" % (begin,end,ycenter))

#find z center
begin = 0
end = 0
for z in range(zdim):
	count = clipped[:,:,z].sum()
	if count > 0:
		if begin==0:
			begin = z
	else:
		if begin > 0 and end==0:
			end = z

if end == 0:
	end = zdim-1

zsize = end - begin
zradius = round(zsize/2)
zcenter = zradius + begin

print("Image starts at %d and ends at %d in z dimension.  Center is at %d" % (begin,end,zcenter))


#make small adjustments for head and neck
zcenter = zcenter + 40
ycenter = ycenter - 5

outfile = "%s/%s_T1w_brain" % (outfolder,subject)
betcommand = "bet %s %s -c %d %d %d -f .4 -o" % (infile,outfile,xcenter,ycenter,zcenter)
print(betcommand)
call(betcommand,shell=True)

#make report
command="slicer %s/%s_T1w_brain_overlay -a %s/skullstrip_results1.png" % (outfolder,subject,outfolder)
print(command)
call(command,shell=True)

command="slicer %s/%s_T1w_brain_overlay -S 10 1250 %s/skullstrip_results2.png" % (outfolder,subject,outfolder)
print(command)
call(command,shell=True)

from datetime import datetime
timestamp = datetime.now().strftime('%b %d %G %I:%M%p')

fsldir = os.environ['FSLDIR']
reportfile = os.path.join(outfolder,"skullstrip_report.html")
outfile = open(reportfile,'a')
outfile.write("<html><head><title>Skull Stripping Report</title><link REL=stylesheet TYPE=text/css href="+fsldir+"/doc/fsl.css></head><body><br><h2>Skull stripping report</h2>"+timestamp+"<br><hr><br>bet command:<br><b>" + betcommand + "</b><br><br><hr><img src=skullstrip_results1.png><br><br><img src=skullstrip_results2.png><br></body></html>")

outfile.close()

call("open " + reportfile,shell=True)


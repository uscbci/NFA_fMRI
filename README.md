NFA fMRI ROI Analysis Pipeline README

Authors: Brock Pluimer, Jonas Kaplan, Evan Abdollahi, Grace Hughes

**Overview**

This repository contains a collection of Python and Shell scripts for preprocessing and analyzing fMRI data for the Kaplan lab’s Narrative Free Awareness Study. The scripts constitute a preprocessing and seed-based functional connectivity analysis pipeline.


**skullstrip.py**

Purpose: Performs skull stripping on T1-weighted MRI images.

Input: T1-weighted MRI images in NIFTI format.

Output: Skull-stripped images and HTML report.

Operations: Utilizes Nibabel for NIFTI handling, NumPy for array operations, and FSL's BET for actual skull stripping. Creates a report including the applied BET command and resultant images.


**setupfieldmaps.py**

Purpose: Prepares fieldmap images for unwarping in FEAT.

Input: Magnitude and phase difference images, input and output folder paths.

Output: Skull-stripped magnitude images and phase images converted to radians.

Operations: Utilizes FSL's bet for skull-stripping and fsl_prepare_fieldmap for phase conversion.


**nfa_preprocess.py**

Purpose: Master preprocessing script for the Meditation Narrative Free Awareness Study.

Input: Raw fMRI data, subject IDs, optional flags to skip certain steps.

Output: Preprocessed fMRI data, log files.

Operations: Utilizes argparse for command-line options, FSL utilities for image processing, and custom functions for lower-level analyses. Can conditionally skip steps like skull stripping, fieldmap preparation, and feature analysis.


**nfa_ICA_AROMA.py**

Purpose: Applies ICA-AROMA for automatic removal of motion-related artifacts in fMRI data for the Meditation Narrative Free Awareness Study.

Input: Subject IDs and corresponding preprocessed fMRI data stored in FEAT folders.

Output: Denoised fMRI data with motion artifacts removed, stored in new ICA_AROMA directories within the existing FEAT folders.


**segmentation.py**

Purpose: Performs tissue segmentation on T1-weighted MRI images for the Meditation Narrative Free Awareness Study.

Input: Subject IDs, T1-weighted skull-stripped MRI images.

Output: Segmented brain tissues (Grey Matter, White Matter, CSF) stored in specified directories.

Operations: Utilizes argparse for command-line arguments, subprocess for executing shell commands. Employs FSL's fast for the segmentation process, targeting Grey Matter, White Matter, and CSF.


**nfa_warp_mask.py**

Purpose: Applies spatial transformations to denoised fMRI data to warp them into a standard MNI space.

Input: Subject IDs, denoised functional MRI data from ICA_AROMA output.

Output: Warped denoised fMRI data in standard MNI space, saved in specified directories.

Operations: Uses argparse for command-line arguments and subprocess for shell commands. Utilizes FSL's applywarp to perform the warping using predefined warp files.


**nfa_fcanalysis.py**

Purpose: Executes a comprehensive seed-based functional connectivity (FC) analysis on resting-state fMRI datasets for the Meditation Narrative Free Awareness Study. The script targets specific Regions of Interest (ROIs) such as the Anterior Cingulate Cortex (dACC), the Medial Prefrontal Cortex (mpfc), and the Angular Gyrus (AG) among others. It assesses the degree of temporal correlation between these ROIs and every other voxel in the brain across three distinct mental states: "restnotask," "restthink," and "restopen."

Input:
* Subject IDs: Either specific IDs or an option to process all subjects.
* Preprocessed fMRI Data: Located in FEAT folders.
* ROI Masks: A list of predefined ROI masks including AG_left, AG_right, AI, dACC, mpfc, etc.
* Resting-state Conditions: Three different mental states namely "restnotask," "restthink," and "restopen."
  
Output:
* FEAT Directories: Each directory contains functional connectivity maps tailored to each ROI and mental state.
* Functional Connectivity Maps: NIFTI files capturing the degree of temporal correlation between the seed ROI and all other voxels.
* Statistical Outputs: Z-statistic images, cluster-corrected significance maps, etc., are part of the FEAT outputs.
  
Operations:
* Argparse: Parses command-line arguments to specify which subjects to process and whether to process all subjects.
* Dynamic FSF Generation: Uses sed to replace placeholders in a generic FEAT design file (.fsf) with specific subject IDs, ROIs, and resting-state conditions.
* FSL's FEAT: Executes the FEAT (FMRI Expert Analysis Tool) command with the dynamically generated .fsf file to perform the actual FC analysis.


**ROI_timeseries.py**

Purpose: Gathers time series data for specific ROIs across different mental states ("restnotask," "restopen," "restthink") for each subject in the study.

Input:
* Subject IDs (specified or all)
* Preprocessed fMRI runs
* ROI masks like AG_left, AG_right, dACC
  
Output: Generates text files containing the average time series for each ROI and mental state.

Operations:
* Argparse for command-line options
* Checks for existing output directories
* Utilizes FSL's fslmeants to extract and save time series data from each ROI.


**segmentation_timeseries.py**

Purpose: Extracts time series data from segmented regions (CSF or WM) for various mental states (e.g., "medopen," "medthink," "restnotask") for each subject.

Input:
* Subject IDs (specified or all)
* fMRI runs
* Type of segmentation (CSF or WM), specified via command line
  
Output: Text files containing average time series for each segmented region (CSF or WM) for each mental state and subject.

Operations:
* Argparse for command-line options
* Validation for segmentation type ('csf' or 'wm')
* Iterates through subjects and runs to execute fslmeants
* Generates time series data for the segmented regions specified


**copyreg.sh**

Purpose: This shell script optimizes the registration process by copying pre-calculated registration matrices and images from a source folder to a destination folder. This avoids redundant calculations for each functional run for the same subject.

Input:
- Source feat folder (already registered from highres to standard)
- Destination feat folder (registered from example_func to highres but not to standard)
  
Output:
- Updated destination folder with copied registration matrices and images.
  
Operations:
- Checks for a minimum number of arguments
- Copies relevant files (matrices, masks, images) from source to destination folder
- Concatenates and converts transformations to generate new registration matrices and warps
- Applies the final warp to map example_func to standard space


**featquery.py**

Purpose: This script uses featquery from FSL to extract statistical values for specific brain regions (ROIs) from fMRI data.

Input: List of subjects, predefined seeds, masks, and runs.

Operations:
1. Selects subjects based on command-line options.
2. Iterates over subjects, seeds, masks, and runs.
3. Executes featquery to extract ROI statistics.
   
Example Command:
featquery 1 /path/to/feat_dir 2 "stats/cope1 stats/cope2" ROI_analysis_mask -p -s /path/to/mask_ref 

Output: ROI analysis files with statistics, prefixed with ROI_analysis_.


**scraper_featquery.py**

Purpose: Automates data extraction for ROI analysis. Scrapes statistical values from featquery report.

Input: Subjects, masks, runs.

Example Command to extract mean connectivity value between input map and mask ROI:

cat '/path/to/featquery_folder/ROI_analysis_mask/report.txt' | grep stats/cope1 | awk '{print $6}' 

Output: Statistical values are printed to the console which can then be copied to a dataframe of choice e.g. Excel


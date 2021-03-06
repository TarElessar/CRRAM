#!/usr/bin/python

# includes

import sys # standard
import os # terminal commands


cbu_id = sys.argv[1] # format CBU12345
foldername = cbu_id + "/"  


# Path  definitions
path_in = ""
path_out = ""
path_mrtrix = ""
path_fsl = ""
path_freesurfer = ""
freesurfer_home = ""
subjects_dir = ""

# Define functions
def call(*arg):
	command = ""
	for a in arg:
		command = command + a + " "
	command = command[:-1]
	os.system(command)

def mrpath(s):
	return path_mrtrix + s

def mrcall(*arg):
	lst = list(arg)
	lst[0] = path_mrtrix + lst[0]
	t = tuple(lst)
	call(*t)

def fscall(*arg):
	lst = list(arg)
	lst[0] = path_freesurfer + lst[0]
	t = tuple(lst)
	call(*t)


def mif(s):
	return path_out + s + "_" + foldername.replace('/','') + ".mif"

def tck(s):
	return path_out + s + "_" + foldername.replace('/','') + ".tck"

def txt(s):
	return path_out + s + "_" + foldername.replace('/','') + ".txt"

def csv(s):
	return path_out + s + "_" + foldername.replace('/','') + ".csv"

def anyfile(s, e):
	return path_out + s + "_" + foldername.replace('/','') + e

def skip(s):
	print("File/Folder <"+s+"> already exists - skip")

print("====================================================")

# set paths
#call("export FREESURFER_HOME=/imaging/local/software/freesurfer/latest/x86_64/")
#call("echo $FREESURFER_HOME")





# Create folder
path_out = path_out + foldername
if not os.path.exists(path_out):
	print("Creating folder <"+path_out+">")
	call("mkdir", path_out)
else:
	skip(path_out)

# mif conversion for convenience

dwi_raw = mif("dwi_raw")

if os.path.exists(dwi_raw):
	skip(dwi_raw)
else:
	mrcall("mrconvert", path_in + cbu_id + "_dti.mif", dwi_raw)
	#call("yes 1 |", path_mrtrix+"mrconvert", path_in + foldername, dwi_raw)

#call("yes 0 |", path_mrtrix+"mrinfo", path_in + foldername)

#mrcall("mrinfo", dwi_raw, "-dwgrad")

# Denoise data

dwi_den = mif("dwi_den")
dwi_den_noise = mif("noise")
dwi_den_residual = mif("residual")

if os.path.exists(dwi_den):
	skip(dwi_den)
else:
	mrcall("dwidenoise", dwi_raw, dwi_den, "-noise", dwi_den_noise)
	mrcall("mrcalc", dwi_raw, dwi_den, "-subtract", dwi_den_residual)

# Unringing data (Gibbs)

dwi_den_unr = mif("dwi_den_unr")
residualUnringed = mif("residualUnringed")

if os.path.exists(dwi_den_unr):
	skip(dwi_den_unr)
else:
	mrcall("mrdegibbs", dwi_den, dwi_den_unr, "-axes 0,1")
	mrcall("mrcalc", dwi_den, dwi_den_unr, "-subtract", residualUnringed)

# Motion/Distortion Correction - only for b0 images, don't think I have any of those, ask MC

mean_b0_AP = mif("mean_b0_AP")
dwi_den_unr_preproc = mif("dwi_den_unr_preproc")

"""
if os.path.exists(mean_b0_AP):
	skip(mean_b0_AP)
else:
	mrcall("dwiextract", dwi_den_unr, "- -bzero |", mrpath("mrmath"), "- mean", mean_b0_AP, "-axis 3")
	mrcall("mrconvert"
"""
dwi_den_unr_preproc = dwi_den_unr


"""
# Bias Field Correction - ANTS installation missing - ask IT

dwi_den_unr_preproc_unbiased = mif("dwi_den_unr_preproc_unbiased")
bias = mif("bias")

if os.path.exists(dwi_den_unr_preproc_unbiased):
	skip(dwi_den_unr_preproc_unbiased)
else:
	mrcall("dwibiascorrect", "-ants", dwi_den_unr_preproc, dwi_den_unr_preproc_unbiased, "-bias", bias)
"""


dwi_den_unr_preproc_unbiased = dwi_den_unr_preproc


# Brain Mask Estimation - no diffusion encoding information found in image - idk what that's about, ask MC

mask_den_unr_preproc_unb = mif("mask_den_unr_preproc_unb")

if os.path.exists(mask_den_unr_preproc_unb):
	skip(mask_den_unr_preproc_unb)
else:
	mrcall("dwi2mask", dwi_den_unr_preproc_unbiased, mask_den_unr_preproc_unb)


# Fibre Orientation Distribution

# Response Function Estimation

voxels = mif("voxels")



if os.path.exists(voxels):
	skip(voxels)
else:
	mrcall("dwi2response", "dhollander", dwi_den_unr_preproc_unbiased, txt("wm"), txt("gm"), txt("csf"), "-voxels", voxels)



# FOD estimation 


wmfod = mif("wmfod")
gmfod = mif("gmfod")
csffod = mif("csffod")
if os.path.exists(wmfod):
	skip(wmfod)
else:
	mrcall("dwi2fod msmt_csd", dwi_den_unr_preproc_unbiased, "-mask", mask_den_unr_preproc_unb, txt("wm"), wmfod, txt("gm"), gmfod, txt("csf"), csffod)

# I'll make it compatible with multi-shell for now
wmfod_norm = mif("wmfod_norm")
gmfod_norm = mif("gmfod_norm")
csffod_norm = mif("csffod_norm")
if os.path.exists(wmfod_norm):
	skip(wmfod_norm)
else:
	#mrcall("mtnormalise", wmfod, wmfod_norm, gmfod, gmfod_norm, csffod, csffod_norm, "-mask", mask_den_unr_preproc_unb)
	mrcall("mtnormalise", wmfod, wmfod_norm, csffod, csffod_norm, "-mask", mask_den_unr_preproc_unb)


# Whole-brain tractogram 

# setup fsl, did that externally
#call("export FSLDIR=/imaging/local/software/fsl/v6.0.1/centos7")    use structural here
T1_raw_structural = mif("T1_raw_structural")

if os.path.exists(T1_raw_structural):
	skip(T1_raw_structural)
else:
	# #call("yes 0 |", path_mrtrix+"mrinfo", path_in + foldername)
	# mrcall("mrconvert", path_in + foldername, T1_raw)
	mrcall("mrconvert", path_in + cbu_id + "_mprage.nii", T1_raw_structural)
	#call("yes 0 |", path_mrtrix+"mrconvert", path_in + foldername, T1_raw_structural)


ftt_nocoreg = mif("5tt_nocoreg")
if os.path.exists(ftt_nocoreg):
	skip(ftt_nocoreg)
else:
	mrcall("5ttgen fsl", T1_raw_structural, ftt_nocoreg)

# coregistering dwi and structural

mean_b0_preprocessed = mif("mean_b0_preprocessed")
if os.path.exists(mean_b0_preprocessed):
	skip(mean_b0_preprocessed)
else:
	mrcall("dwiextract", dwi_den_unr_preproc_unbiased, "- -bzero | "+ path_mrtrix+"mrmath - mean", mean_b0_preprocessed, "-axis 3")

# converting to nifti files, commonly used here

ftt_nocoreg_nii = anyfile("5tt_nocoreg", ".nii.gz")
if os.path.exists(ftt_nocoreg_nii):
	skip(ftt_nocoreg_nii)
else:
	mrcall("mrconvert", mean_b0_preprocessed, anyfile("mean_b0_preprocessed",".nii.gz"))
	mrcall("mrconvert", ftt_nocoreg, ftt_nocoreg_nii)


diff2struct_mrtrix = txt("diff2struct_mrtrix")
if os.path.exists(diff2struct_mrtrix):
	skip(diff2struct_mrtrix)
else:
	call("flirt -in", anyfile("mean_b0_preprocessed",".nii.gz"), "-ref", ftt_nocoreg_nii, "-interp nearestneighbour -dof 6 -omat", anyfile("diff2struct_fsl",".mat"))
	mrcall("transformconvert", anyfile("diff2struct_fsl",".mat"), anyfile("mean_b0_preprocessed",".nii.gz"), ftt_nocoreg_nii, "flirt_import", diff2struct_mrtrix)

ftt_coreg = mif("ftt_coreg")
if os.path.exists(ftt_coreg):
	skip(ftt_coreg)
else:
	mrcall("mrtransform", ftt_nocoreg, "-linear", diff2struct_mrtrix, "-inverse", ftt_coreg)

# first batch should end here ================================================================
#exit()

# mask generation
gmwmSeed_coreg = mif("gmwmSeed_coreg")
if os.path.exists(gmwmSeed_coreg):
	skip(gmwmSeed_coreg)
else: 
	mrcall("5tt2gmwmi", ftt_coreg, gmwmSeed_coreg)


# track generation

tracks_tenmio = tck("tracks_10mio")


if os.path.exists(tracks_tenmio):
	skip(tracks_tenmio)
else:
	mrcall("tckgen", "-act", ftt_coreg, "-backtrack -seed_gmwmi", gmwmSeed_coreg, "-select 1000000", wmfod_norm, tracks_tenmio)

# apply SIFT

sift_onemio = tck("sift_1mio")

if os.path.exists(sift_onemio):
	skip(sift_onemio)
else:
	mrcall("tcksift -act", ftt_coreg, "-term_number 1000000", tracks_tenmio, wmfod_norm, sift_onemio)

# atlas generation - ask for nifti at some point

# nifti conversion - we defined dwi_raw as the raw file
T1_raw = anyfile("T1_raw", ".nii.gz")

if os.path.exists(T1_raw):
	skip(T1_raw)
else:
	# #call("yes 0 |", path_mrtrix+"mrinfo", path_in + foldername)
	# mrcall("mrconvert", path_in + foldername, T1_raw)
	mrcall("mrconvert", path_in + cbu_id + "_mprage.nii", T1_raw)
	#call("yes 0 |", path_mrtrix+"mrconvert", path_in + foldername, T1_raw)


# second batch should end here ================================================================
#exit()

# preprocessing - will take a while
subject_name = foldername[:-1]
subject = anyfile(subject_name, "")

if os.path.exists(subject):
	skip(subject)
else:
	call("mkdir", subject)
	#call("source /imaging/local/software/freesurfer/latest/x86_64/SetUpFreeSurfer.csh")
	fscall("recon-all -s", subject_name, "-i", T1_raw, "-all")

#fscall("recon-all -s", foldername[:-1], "-i", T1_raw, "-all")
#fscall("recon-all -s", subject_name, "-autorecon2")
#fscall("recon-all -s", subject_name, "-autorecon3")

# map annotations - try atlas lh.aparc.a2005s.annot

hcpmmp1_parcels_coreg = mif("hcpmmp1_parcels_coreg")
hcpmmp1_parcels_nocoreg = mif("hcpmmp1_parcels_nocoreg")
if os.path.exists(hcpmmp1_parcels_coreg):
	skip(hcpmmp1_parcels_coreg)
else:

	fscall("mri_surf2surf --srcsubject fsaverage --trgsubject", subject_name, "--hemi lh --sval-annot $SUBJECTS_DIR/fsaverage/label/lh.aparc.a2005s.annot --tval $SUBJECTS_DIR/"+subject_name+"/label/lh.hcpmmp1.annot")
	fscall("mri_surf2surf --srcsubject fsaverage --trgsubject", subject_name, "--hemi rh --sval-annot $SUBJECTS_DIR/fsaverage/label/rh.aparc.a2005s.annot --tval $SUBJECTS_DIR/"+subject_name+"/label/rh.hcpmmp1.annot")
	fscall("mri_aparc2aseg --old-ribbon --s", subject_name, "--annot hcpmmp1 --o", anyfile("hcpmmp1",".mgz"))
	mrcall("mrconvert -datatype uint32", anyfile("hcpmmp1",".mgz"), mif("hcpmmp1"))
	mrcall("labelconvert", mif("hcpmmp1"), "/imaging/local/software/mrtrix/v3.0.3_nogui/share/mrtrix3/labelconvert/hcpmmp1_original.txt /imaging/local/software/mrtrix/v3.0.3_nogui/share/mrtrix3/labelconvert/hcpmmp1_ordered.txt", hcpmmp1_parcels_nocoreg)
	mrcall("mrtransform", hcpmmp1_parcels_nocoreg, "-linear", diff2struct_mrtrix, "-inverse -datatype uint32", mif("hcpmmp1_parcels_coreg"))

	#mrcall("mrtransform", hcpmmp1_parcels_nocoreg, "-datatype uint32", hcpmmp1_parcels_coreg)

# TODO Clean up this entire mess.... at least I got my atlas file now I guess




# connectome generation - using pre-made atlas for now, just wanted to see if it's possible

hcpmmp1 = csv("hcpmmp1")
assignments_hcpmmp1 = csv("assignments_hcpmmp1")

if os.path.exists(hcpmmp1):
	skip(hcpmmp1)
else:
	mrcall("tck2connectome -symmetric -zero_diagonal -scale_invnodevol", sift_onemio, hcpmmp1_parcels_coreg, hcpmmp1, "-out_assignments", assignments_hcpmmp1)









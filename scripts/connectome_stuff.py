#!/usr/bin/python

# includes

import sys # standard
import os # terminal commands


cbu_id = sys.argv[1] # format CBU12345
foldername = cbu_id + "/"  


# Path  definitions
path_in = "/imaging/mc04/fm03/test_series2/"
path_out = "/imaging/mc04/fm03/data/"
path_mrtrix = "/imaging/local/software/mrtrix/v3.0.3_nogui/bin/"
path_fsl = "/imaging/local/software/fsl/v6.0.1/centos7/bin/"
#path_atlas = "/imaging/mc04/fm03/Atlas/hcpmmp1_parcels_coreg.mif"
path_freesurfer = "/imaging/local/software/freesurfer/latest/x86_64/bin/"
freesurfer_home = "/imaging/local/software/freesurfer/latest/x86_64/"
subjects_dir = "/imaging/mc04/fm03/fs_subjects"

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


path_out = path_out + foldername
subject_name = foldername[:-1]
subject = anyfile(subject_name, "")


# ======================================================
hcpmmp1_parcels_coreg = mif("hcp_parcels_coreg")
hcpmmp1_parcels_nocoreg = mif("hcp_parcels_nocoreg")

"""
fscall("mri_surf2surf --srcsubject fsaverage --trgsubject", subject_name, "--hemi lh --sval-annot $SUBJECTS_DIR/fsaverage/label/lh.aparc.a2005s.annot --tval $SUBJECTS_DIR/"+subject_name+"/label/lh.hcpmmp1.annot")
fscall("mri_surf2surf --srcsubject fsaverage --trgsubject", subject_name, "--hemi rh --sval-annot $SUBJECTS_DIR/fsaverage/label/rh.aparc.a2005s.annot --tval $SUBJECTS_DIR/"+subject_name+"/label/rh.hcpmmp1.annot")
fscall("mri_aparc2aseg --old-ribbon --s", subject_name, "--annot hcpmmp1 --o", anyfile("hcp",".mgz"))
mrcall("mrconvert -force -datatype uint32", anyfile("hcp",".mgz"), mif("hcp"))
mrcall("labelconvert -force", mif("hcp"), "//imaging/local/software/mrtrix/v3.0.3_nogui/share/mrtrix3/labelconvert/hcpmmp1_original.txt /imaging/local/software/mrtrix/v3.0.3_nogui/share/mrtrix3/labelconvert/hcpmmp1_ordered.txt", hcpmmp1_parcels_nocoreg)
"""

"""
diff2struct_mrtrix = txt("diff2struct_mrtrix")
mrcall("mrtransform -force", hcpmmp1_parcels_nocoreg, "-linear", diff2struct_mrtrix, "-inverse -datatype uint32", hcpmmp1_parcels_coreg)
"""
mrcall("mrconvert -force", hcpmmp1_parcels_coreg, anyfile("hcp_coreg",".mgz"))
call("cp", "/imaging/local/software/mrtrix/v3.0.3_nogui/share/mrtrix3/labelconvert/hcpmmp1_ordered.txt", txt("hcp_coreg"))
"""
hcpmmp1 = csv("hcp")
assignments_hcpmmp1 = csv("assignments_hcp")
sift_onemio = tck("sift_1mio")
mrcall("tck2connectome -force -symmetric -zero_diagonal -scale_invnodevol", sift_onemio, hcpmmp1_parcels_coreg, hcpmmp1, "-out_assignments", assignments_hcpmmp1)
"""






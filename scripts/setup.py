import sys # standard
import os # terminal commands

path_in = "/imaging/mc04/MRIcalibration/Data/Dicom/Prisma/"
path_out = "/imaging/mc04/fm03/data/"
path_mrtrix = "/imaging/local/software/mrtrix/v3.0.3_nogui/bin/"
path_fsl = "/imaging/local/software/fsl/v6.0.1/centos7/bin/"
path_atlas = "/imaging/mc04/fm03/Atlas/hcpmmp1_parcels_coreg.mif"
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

call("echo $SUBJECTS_DIR")
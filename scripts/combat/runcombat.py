import os
#os.chdir('/users/ncullen/desktop/projects/_third_party/neuroCombat/examples/bladder')
import mycombat
import importlib
importlib.reload(mycombat)

import pandas as pd
import numpy as np
import nibabel as nib

from os import listdir
from os.path import isfile, join

path_in = "/imaging/mc04/fm03/test_series4"
path_out = "/imaging/mc04/fm03/test_series4/optimised"

#onlyfiles = [f for f in listdir(path_in) if isfile(join(mypath, f))]

# exec(open("runcombat.py").read())


fmri_files = []
pheno_file = ""
flag = True
if not 'data' in locals() or flag:
	for filename in sorted(listdir(path_in)):
		if ".nii" in filename and "epi" in filename and not "140931" in filename:
			print("Found fmri file <", filename,">")
			fmri_files.append(filename)
		if ".txt" in filename and "pheno" in filename:
			pheno_file = filename
		if ".nii" in filename and "epi" in filename and "140931" in filename:
			img = nib.load(os.path.join(path_in, filename))
			nib.save(img, os.path.join(path_out, filename))
	
	#print(fmri_files)
	fmri_array = []
	fmri_affine = []
	fmri_shape = []
	
	for filename in sorted(fmri_files):
		print("Converting file <", filename,"> to numpy array")
		img = nib.load(os.path.join(path_in, filename))
		arr = np.array(img.dataobj)
		fmri_shape.append(arr.shape)
		print(arr.shape)
		# 1D form
		arr_flatten = np.array(arr.ravel())
		fmri_array.append(arr_flatten)
		fmri_affine.append(img.affine)
	
	data = np.array(fmri_array)


# calculate new array
print("Running ComBat...")
covars = pd.read_csv(os.path.join(path_in, pheno_file), delimiter='\t')
discrete_cols = None
continuous_cols = None
batch_col = 'batch'


fmri_array_new = mycombat.neuroCombat(data=data,
                          covars=covars,
                          batch_col=batch_col,
                          discrete_cols=discrete_cols,
                          continuous_cols=continuous_cols)

# save as nii

for i in range(len(fmri_array_new)):
	print("Saving updated file <", fmri_files[i],"> as nifti")
	arr = np.reshape(fmri_array_new[i], fmri_shape[i])
	ni_img = nib.Nifti1Image(arr, fmri_affine[i])
	nib.save(ni_img, os.path.join(path_out, fmri_files[i]))



"""
#data = np.load('data/bladder-expr.npy')
#covars = pd.read_csv('data/bladder-pheno.txt', delimiter='\t')

#discrete_cols = ['cancer']
#continuous_cols = ['age']
batch_col = 'batch'

data_combat = neuroCombat(data=data,
                          covars=covars,
                          batch_col=batch_col,
                          discrete_cols=discrete_cols,
                          continuous_cols=continuous_cols)

"""

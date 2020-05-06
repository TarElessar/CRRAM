import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

def show_slices(slices, filename):
	fig, axes = plt.subplots(1, len(slices))
	for i, slice in enumerate(slices):
		axes[i].imshow(slice.T, cmap="gray", origin="lower")
	plt.savefig(filename)

print("start")

path_in = "/imaging/mc04/fm03/camcan_fmri/tsnr/group"
path1=os.path.join(path_in, "tsnr_group1.nii")
path2=os.path.join(path_in, "tsnr_group2.nii")
paths = (path1, path2)

for i in range(2):
	path = paths[i]
	img = nib.load(path)
	data = img.get_fdata()

	slice_0 = data[32, :, :]
	slice_1 = data[:, 32, :]
	slice_2 = data[:, :, 16]
	show_slices([slice_0, slice_1, slice_2], os.path.join(path_in, "group" + str(i) + ".png"))



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

path_in = "/imaging/mc04/fm03/camcan_fmri/tsnr"
path_out = "/imaging/mc04/fm03/camcan_fmri/tsnr/img"
path1=os.path.join(path_in, "tsnr_group1.nii")
path2=os.path.join(path_in, "tsnr_group2.nii")
paths = (path1, path2)

group1_ids = ["tsnrCBU140905_epi.nii", "tsnrCBU140953_epi.nii", "tsnrCBU140910_epi.nii", "tsnrCBU140962_epi.nii", "tsnrCBU140913_epi.nii", "tsnrCBU140979_epi.nii", "tsnrCBU140928_epi.nii", "tsnrCBU140982_epi.nii", "tsnrCBU140931_epi.nii", "tsnrCBU140984_epi.nii"]
group2_ids = ["tsnrCBU150062_epi.nii", "tsnrCBU150074_epi.nii", "tsnrCBU150057_epi.nii", "tsnrCBU150124_epi.nii", "tsnrCBU150056_epi.nii", "tsnrCBU150080_epi.nii", "tsnrCBU150239_epi.nii", "tsnrCBU150303_epi.nii", "tsnrCBU150060_epi.nii", "tsnrCBU150082_epi.nii", ]


directory = os.fsencode(path_in)

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.endswith(".nii"): 
		path=os.path.join(path_in, filename)
		print(path)
		img = nib.load(path)
		data = img.get_fdata()
	
		slice_0 = data[32, :, :]
		slice_1 = data[:, 32, :]
		slice_2 = data[:, :, 16]
		if filename in group1_ids: 
			show_slices([slice_0, slice_1, slice_2], os.path.join(path_out, "trio_" + str(filename[:-4]) + ".png"))
		if filename in group2_ids:
			show_slices([slice_0, slice_1, slice_2], os.path.join(path_out, "prisma_" + str(filename[:-4]) + ".png"))



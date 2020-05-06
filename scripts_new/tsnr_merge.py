import os
import numpy as np
import nibabel as nib

print("start")

path_in = "/imaging/mc04/fm03/camcan_fmri/tsnr"
path_out = "/imaging/mc04/fm03/camcan_fmri/tsnr/group"
directory = os.fsencode(path_in)
# 1 trio, 2 prisma
group1_ids = ["tsnrCBU140905_epi.nii", "tsnrCBU140953_epi.nii", "tsnrCBU140910_epi.nii", "tsnrCBU140962_epi.nii", "tsnrCBU140913_epi.nii", "tsnrCBU140979_epi.nii", "tsnrCBU140928_epi.nii", "tsnrCBU140982_epi.nii", "tsnrCBU140931_epi.nii", "tsnrCBU140984_epi.nii"]
group2_ids = ["tsnrCBU150062_epi.nii", "tsnrCBU150074_epi.nii", "tsnrCBU150057_epi.nii", "tsnrCBU150124_epi.nii", "tsnrCBU150056_epi.nii", "tsnrCBU150080_epi.nii", "tsnrCBU150239_epi.nii", "tsnrCBU150303_epi.nii", "tsnrCBU150060_epi.nii", "tsnrCBU150082_epi.nii", ]

shape = (64, 64, 32)
group1 = np.zeros(shape)
group2 = np.zeros(shape)

group1_cnt = 0
group2_cnt = 0

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.endswith(".nii"): 
		path=os.path.join(path_in, filename)
		print(path)
		img = nib.load(path)
		data = img.get_fdata()
		print(data.shape)

		if filename in group1_ids:
			print("g1")
			group1 = np.add(group1, data)
			group1_cnt = group1_cnt + 1
		if filename in group2_ids:
			print("g2")
			group2 = np.add(group2, data)
			group2_cnt = group2_cnt + 1

		print("finish subroutine")
		

print("normalise")
if not group1_cnt == 0:
	group1 = np.true_divide(group1, group1_cnt)
if not group2_cnt == 0:
	group2 = np.true_divide(group2, group2_cnt)

print("save files")
print(group1_cnt, group2_cnt)
print(group1[30][30][10])
print(group2[30][30][10])


img1 = nib.Nifti1Image(group1, np.eye(4))
path1=os.path.join(path_out, "tsnr_group1.nii")
nib.save(img1, path1)

img2 = nib.Nifti1Image(group2, np.eye(4))
path2=os.path.join(path_out, "tsnr_group2.nii")
nib.save(img2, path2)


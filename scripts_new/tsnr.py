import os
import numpy as np
import nibabel as nib

print("start")

path_in = "/imaging/mc04/fm03/camcan_fmri"
path_out = "/imaging/mc04/fm03/camcan_fmri/tsnr"
directory = os.fsencode(path_in)

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.endswith(".nii"): 
		path=os.path.join(path_in, filename)
		print(path)
		img = nib.load(path)
		data = img.get_fdata()
		print(data.shape)
		
		new_data = np.zeros((data.shape[0], data.shape[1], data.shape[2]), dtype=img.get_data_dtype())
		
		for x in range(data.shape[0]):
			for y in range(data.shape[1]):
				for z in range(data.shape[2]):
					temporal_subset = data[x, y, z, :]
					mean = np.mean(temporal_subset)
					std = np.std(temporal_subset)
					if std==0:
						tsnr = 0.0
					else:
						tsnr = np.nan_to_num(mean / std)
					new_data[x][y][z] = tsnr
					#print(x, y, z, tsnr)	
		img_new = nib.Nifti1Image(new_data, np.eye(4))
		path_new=os.path.join(path_out, "tsnr" + filename)
		nib.save(img_new, path_new)
		continue
	else:
		continue

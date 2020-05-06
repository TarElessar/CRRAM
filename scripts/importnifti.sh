#!/bin/bash

path_out="/imaging/mc04/fm03/test_series4/"

declare -a paths_input=("/imaging/mc04/MRIcalibration/Data/Dicom/Prisma/" "/imaging/mc04/MRIcalibration/Data/Dicom/Trio/")
#declare -a paths_input=("/imaging/mc04/MRIcalibration/CamCAN_calibration/PRISMA/Subj13/" "/imaging/mc04/MRIcalibration/CamCAN_calibration/PRISMA/Subj14/" "/imaging/mc04/MRIcalibration/CamCAN_calibration/PRISMA/Subj15/" "/imaging/mc04/MRIcalibration/CamCAN_calibration/PRISMA/Subj16/" "/imaging/mc04/MRIcalibration/CamCAN_calibration/PRISMA/Subj17/" "/imaging/mc04/MRIcalibration/CamCAN_calibration/TRIO/Subj13/" "/imaging/mc04/MRIcalibration/CamCAN_calibration/TRIO/Subj14/" "/imaging/mc04/MRIcalibration/CamCAN_calibration/TRIO/Subj15/" "/imaging/mc04/MRIcalibration/CamCAN_calibration/TRIO/Subj16/" "/imaging/mc04/MRIcalibration/CamCAN_calibration/TRIO/Subj17/")
p=pwd
for val in ${paths_input[@]}; do
cd "$val"
for d in */; do
	subject=${d%"/"}
	cd "$val""$d"
	for v in */;do
		if [[ $v == *"MPRAGE"* ]]; then
			mprage="$val""$d""$v"
		elif [[ $v == *"EPI"* ]]; then
			epi="$val""$d""$v"
		elif [[ $v == *"DTI"* ]]; then
# note: change back to DTI for original, DKI for combat
			dti="$val""$d""$v"
		fi
	done
	path_mprage="$path_out""$subject""_mprage.nii"
	path_epi="$path_out""$subject""_epi.nii"
	path_dti="$path_out""$subject""_dti.mif"
	mrconvert "$mprage" "$path_mprage"
	mrconvert "$epi" "$path_epi"
	mrconvert "$dti" "$path_dti"
done
done

cd "$p"


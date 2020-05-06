#!/bin/bash

path_in="/imaging/mc04/fm03/PatientData/"
path_out="/imaging/mc04/fm03/test_series_patientdata/"
pseudocbu="$path_out""subject_files.txt"

touch "$pseudocbu"
i=9
# starts at 000010
for d in "$path_in"*
do
if [[ $d == *".nii"* ]]; then
i=$((i+1))
suffix=".nii"
subject_id=$(echo $d | cut -c$((${#path_in}+1))- | rev | cut -c$((${#suffix}+1))- | rev)
cbu_id="CBU0000""$i"
echo "$subject_id"", ""$cbu_id" >> "$pseudocbu"
bval="$path_in""$subject_id"".bval"
bvec="$path_in""$subject_id"".bvec"
path_mprage="$path_out""$cbu_id""_mprage.nii"
path_dti="$path_out""$cbu_id""_dti.mif"
mrconvert "$d" "$path_mprage"
mrconvert "$d" -fslgrad "$bvec" "$bval" "$path_dti" 


#$ mrconvert dwi.nii -fslgrad dwi_bvecs dwi_bvals dwi.mif

fi
done

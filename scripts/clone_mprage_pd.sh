#!/bin/bash

path_in="/imaging/mc04/PD_MR10002/MPRAGEAnalysis/Session1/"
path_in2="/imaging/mc04/PD_MR10002/MPRAGEAnalysis/Session2/"
path_out="/imaging/mc04/fm03/test_series_patientdata/"
pseudocbu="$path_out""subject_files.txt"


i=9
for d in "$path_in"*.nii 
do
suffix="_MPRAGE_S1.nii"
title=$(echo $d | cut -c$((${#path_in}+1))- | rev | cut -c$((${#suffix}+1))- | rev)

if [[ $title == C02* ]] || [[ $title == C21* ]] || [[ $title == PD30* ]] || [[ $title == PD34* ]]; then
echo "skip"
elif [[ $title == P* ]] || [[ $title == C* ]]; then

echo "$title"
i=$((i+1))
loc="$path_in""$title""_MPRAGE_S1.nii"
cbu_id="CBU0000""$i"
path_mprage="$path_out""$cbu_id""_mprage.nii"
mrconvert "$loc" "$path_mprage"
i=$((i+1))
loc="$path_in2""$title""_MPRAGE_S2.nii"
cbu_id="CBU0000""$i"
path_mprage="$path_out""$cbu_id""_mprage.nii"
mrconvert "$loc" "$path_mprage"


fi

done

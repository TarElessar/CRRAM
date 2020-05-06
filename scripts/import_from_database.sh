#!/bin/bash

path_out="/imaging/mc04/fm03/test_series_multischeme/"
declare -a subject_list=("100639" "100699" "100726" "100729" "100730" "100731" "100732" "100733" "100737" "100738" "100739" "100740" "100741" "100743" "100759" "100760")

for val in ${subject_list[@]}; do
echo "importing subject $val"
path_study="/mridata/cbu/CBU""$val""_MR10012/"
echo "$path_study"
dirs=("$path_study"*/)
sub="${dirs[0]}"
files=("$sub"*/)
for file in "${files[@]}"
do
if [[ $file == *"MPRAGE"* ]]; then
  echo "$file"
  for i in {1..5}
  do
  #path_new_dir="$path_out""CBU""$val""00$i"
  path_new="$path_out""CBU$val""00$i""_mprage.nii"
  #mkdir -p "$path_new_dir"
  #echo "$path_new"
  mrconvert "$file" "$path_new"
  done
elif [[ $file == *"DTI"* ]] && ! [[ $file == *"ADC"* ]] && ! [[ $file == *"TRACEW"* ]] && ! [[ $file == *"EXP"* ]] && ! [[ $file == *"FA"* ]] && ! [[ $file == *"ColFA"* ]] && ! [[ $file == *"reps"* ]]; then
  if [[ $file == *"60x1"* ]]; then
    i="1"
  elif [[ $file == *"30x2"* ]]; then
    i="2"
  elif [[ $file == *"20x3"* ]]; then
    i="3"
  elif [[ $file == *"15x4"* ]]; then
    i="4"
  elif [[ $file == *"12x5"* ]]; then
    i="5"
  fi
 
 path_new="$path_out""CBU$val""00$i""_dti.mif"
 mrconvert "$file" "$path_new"

fi
done
done

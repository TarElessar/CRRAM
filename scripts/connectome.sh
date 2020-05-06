#!/bin/sh
#/imaging/mc04/fm03/scripts/cbufsl_branch -l 1 -x "python /imaging/mc04/fm03/scripts/connectome.py $1"
source /imaging/local/software/freesurfer/latest/x86_64/SetUpFreeSurfer.sh
python /imaging/mc04/fm03/scripts/connectome.py $1


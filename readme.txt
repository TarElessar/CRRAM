CRRAM - Connectome Repeatability and Reproducibility Analysis Module

Library files:
scripts
 | crram.py				# main module
 | crram_analysis.py			# sample script, call with: python3 crram_analysis working_dir data_dir
 | crram_call.sh			# bash call
 | crram_windows_to_linux.sh		# converts html format, windows -> linux (paste path into source); not supported on all UNIX distributions
 | crram_linux_to_windows.sh		# converts html format, linux -> windows (paste path into source)
 | readme.txt				# info


Expected file structure:
data_dir
 | connectomes
   | dmri
     | connectome_CBU12345.csv		# space or comma separated
   | fmri
     | connectome_CBU12345.csv		# space or comma separated
   | <other modality>
     | connectome_CBU12345.csv		# space or comma separated
 | subject_data
   | subjects_SCANNERNAME.csv		# <Subj,ID,sex,CBU,Study,Age,scan date> format, ignores first row (header)
 


Generated file structure:
working_dir
 | src					# contains all pictures and backed up tables - see list of formats below
   | modality12345modifier.png
   | modality_modifier.csv/.png
   | modality_scanner_modifier.csv/.png
   | modalityscanner12345modifier.png
   | info.txt 				# contains metadata / experiment information
 | analysis.html			# main analysis results
 | styles.css				# stylesheet for html page
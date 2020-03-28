# -*- coding: utf-8 -*-
"""
@author: Felix Menze
"""

import crram as cr
import sys
import os
import csv

# =====================================================================================================================

if(len(sys.argv) == 3):
    working_dir = sys.argv[1]
    data_dir = sys.argv[2]
else:
    print("Please provide valid arguments")
    exit()


# =====================================================================================================================
    
# main src directory
src_dir = os.path.join(working_dir, "src")

# =====================================================================================================================

flag = False
flag2 = False
flag3 = False
flag4 = False
flag5 = False


cr.init()
patient_data_files, path_connectome_main = cr.read_path_structure(data_dir)
map_cor = cr.read_patient_data(patient_data_files)
map_same = cr.create_patient_data_map(map_cor)

# connectome basic
if not 'connectome_list' in locals() or flag:
    connectome_list = cr.read_all_connectome_data(path_connectome_main)

# single scanner
if not 'scanner_separated_list' in locals() or flag2:
    scanner_separated_list = cr.generate_scanner_separated_list(connectome_list, map_cor)
    
# run on dmri, trio 140997 (match is 140981)
target_id = 140997
target = scanner_separated_list["dmri"][0][target_id]
result = {}

other_id = 140981
connectome = scanner_separated_list["dmri"][0][other_id]
#result[cbu_id] = {}
#result[cbu_id]["abs"] = cr.compare(target, connectome)
#result[cbu_id]["abs2"] = cr.compare2(target, connectome)
#result[cbu_id]["sim"] = cr.similarity(target, connectome)
#result[cbu_id]["sim2"] = cr.similarity2(target, connectome)
#(sim, sim2) = cr.gcap_iteration_array(connectome, target, 5)
#result[cbu_id]["gcap"] = sim
#result[cbu_id]["gca2p"] = sim2

file = os.path.join(src_dir, 'aaa.csv')

if not os.path.exists(file):
    open(file, 'w').close() 
with open(file, 'a') as f: 
    f.write(str(other_id) + " sim " + str(cr.similarity(target, connectome)) + "\n")
    f.close()
with open(file, 'a') as f: 
    f.write(str(other_id) + " sim2 " + str(cr.similarity2(target, connectome)) + "\n")
    f.close()
(sim, sim2) = cr.gcap_iteration_array(connectome, target, 5)
with open(file, 'a') as f: 
    f.write(str(other_id) + " gcap " + str(sim) + "\n")
    f.write(str(other_id) + " gcap2 " + str(sim2) + "\n")
    f.close()
    


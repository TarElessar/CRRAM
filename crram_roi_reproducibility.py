# -*- coding: utf-8 -*-
"""
@author: Felix Menze
"""

import crram as cr
import sys
import os
import numpy as np
# =====================================================================================================================

if(len(sys.argv) >= 3):
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


cluster_size = 1
sc1 = "alpha"
sc2 = "beta"
scanner1 = 0
scanner2 = 0

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
    

for i in range(4):
    if(cr.get_scanner_name(i, patient_data_files)) == sc1:
        scanner1 = i
    if(cr.get_scanner_name(i, patient_data_files)) == sc2:
        scanner2 = i

print(scanner1, scanner2)

statistics_file1 = os.path.join(working_dir, "cluster" + str(cluster_size) + "_dmri_" + str(sc1) + "_" + str(sc2) +".txt")
if os.path.exists(statistics_file1):
    f = open(statistics_file1,'r+')
    f.truncate(0)
    f.close()
else:
    open(statistics_file1, 'a').close()
    
f1 = open(statistics_file1,'w')
dimension = 379
for xx in range(dimension):
    f1.write("\n")
    f1.close()
    f1 = open(statistics_file1,'a')
    for yy in range(dimension):    
        print(xx, " / ", yy)
        # delete all entries not in cluster
        scanner_separated_list_temp = cr.apply_to_scanner_specific_connectomes(scanner_separated_list, lambda c : cr.remove_all_but_cluster(c, xx, yy, cluster_size))
        
        (comp_similarity, ordering1, ordering2) = cr.apply_to_cross_scanner_pairs_specify_pair(scanner_separated_list_temp, scanner1, scanner2, lambda x,y : cr.similarity(x, y))   
        
        for modality, m_list in comp_similarity.items():
            # mat = cr.sort_array_by_correspondence(scanner_sublist, ordering[modality][scanner], map_same)[0]
            mat = m_list
            (contrast_n, contrast_error, contrast) = cr.get_contrast_analysis_cross_scanner(mat)
            
            if modality == "dmri":
                f1.write(str(contrast) + ", ")
            
f1.close()


"""

modality_separated_list = cr.generate_modality_separated_list(scanner_separated_list)
(reduced_list, dimension) = cr.remove_zero_connections(modality_separated_list)
scanner_separated_list_updated = cr.generate_scanner_separated_from_modality_separated_list(reduced_list)
# apply stuff to list
statistics_file1 = os.path.join(working_dir, "cluster" + str(cluster_size) + "_fmri_" + cr.get_scanner_name(0, patient_data_files) +".txt")
statistics_file2 = os.path.join(working_dir, "cluster" + str(cluster_size) + "_dmri_" + cr.get_scanner_name(0, patient_data_files) +".txt")
statistics_file3 = os.path.join(working_dir, "cluster" + str(cluster_size) + "_fmri_" + cr.get_scanner_name(1, patient_data_files) +".txt")
statistics_file4 = os.path.join(working_dir, "cluster" + str(cluster_size) + "_dmri_" + cr.get_scanner_name(1, patient_data_files) +".txt")

if os.path.exists(statistics_file1):
    f = open(statistics_file1,'r+')
    f.truncate(0)
    f.close()
else:
    open(statistics_file1, 'a').close()

if os.path.exists(statistics_file2):
    f = open(statistics_file2,'r+')
    f.truncate(0)
    f.close()
else:
    open(statistics_file2, 'a').close()
    
if os.path.exists(statistics_file3):
    f = open(statistics_file3,'r+')
    f.truncate(0)
    f.close()
else:
    open(statistics_file3, 'a').close()
    
if os.path.exists(statistics_file4):
    f = open(statistics_file4,'r+')
    f.truncate(0)
    f.close()
else:
    open(statistics_file4, 'a').close()



f1 = open(statistics_file1,'w')
f2 = open(statistics_file2,'w')
f3 = open(statistics_file3,'w')
f4 = open(statistics_file4,'w')


f1.write("Analysing ROI clusters of size " + str(cluster_size))
f2.write("Analysing ROI clusters of size " + str(cluster_size))
f3.write("Analysing ROI clusters of size " + str(cluster_size))
f4.write("Analysing ROI clusters of size " + str(cluster_size))
for xx in range(dimension):
    f1.write("\n")
    f2.write("\n")
    f3.write("\n")
    f4.write("\n")
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f1 = open(statistics_file1,'a')
    f2 = open(statistics_file2,'a')
    f3 = open(statistics_file3,'a')
    f4 = open(statistics_file4,'a')
    for yy in range(dimension):    
        print(xx, " / ", yy)
        # delete all entries not in cluster
        scanner_separated_list_temp = cr.apply_to_scanner_specific_connectomes(scanner_separated_list_updated, lambda c : cr.remove_all_but_cluster(c, xx, yy, cluster_size))
        
        
        (comp_similarity, ordering) = cr.apply_to_scanner_specific_connectome_pairs(scanner_separated_list_temp, lambda x,y : cr.similarity(x, y))
        
        
        for modality, m_list in comp_similarity.items():
            for scanner, scanner_sublist in m_list.items():
                mat = cr.sort_array_by_correspondence(scanner_sublist, ordering[modality][scanner], map_same)[0]
                match = []
                other = []
                for x in range(len(mat)):
                    for y in range(x):
                        if x % 2 != 0 and x == y + 1:
                            match.append(mat[y][x])
                        else:
                            other.append(mat[y][x])
                name = cr.get_scanner_name(scanner, patient_data_files)
                std_factor = 1.96
                contrast = (np.mean(other) - std_factor * np.std(other) - std_factor * np.std(match) - np.mean(match)) / np.mean(other)
                contrast_error = (np.mean(other) - np.std(other) - np.std(match) - np.mean(match)) / np.mean(other)
                contrast_n = (np.mean(other) - np.mean(match)) / np.mean(other)
                
                if np.mean(other) == 0:
                    contrast = 0.0
                
                print(modality, scanner)
                if modality == "fmri":
                    if scanner == 0:
                        f1.write(str(contrast) + ", ")
                    if scanner == 1:
                        f3.write(str(contrast) + ", ")
                if modality == "dmri":
                    if scanner == 0:
                        f2.write(str(contrast) + ", ")
                    if scanner == 1:
                        f4.write(str(contrast) + ", ")
                        
            
f1.close()
f2.close()
f3.close()
f4.close()



"""


# -*- coding: utf-8 -*-
"""
@author: Felix Menze
"""

import crram as cr
import sys
import os
import numpy as np
import csv
from matplotlib import pyplot as plt

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree


# =====================================================================================================================
# define ROIs
roi_list = {}
roi_list["bn"] = {}
roi_list["glasser"] = {}
roi_list["schaefer116"] = {}
roi_list["schaefer232"] = {}
roi_list["schaefer454"] = {}

roi_location = {}
roi_location["bn"] = r"D:\research\MRI_newstuff\ROIs\bn.csv"
roi_location["glasser"] = r"D:\research\MRI_newstuff\ROIs\glasser.csv"
roi_location["schaefer116"] = r"D:\research\MRI_newstuff\ROIs\schaefer116.csv"
roi_location["schaefer232"] = r"D:\research\MRI_newstuff\ROIs\schaefer232.csv"
roi_location["schaefer454"] = r"D:\research\MRI_newstuff\ROIs\schaefer454.csv"

roi_list_accel = {}
roi_list_accel["bn"] = np.zeros(500)
roi_list_accel["glasser"] = np.zeros(500)
roi_list_accel["schaefer116"] = np.zeros(500)
roi_list_accel["schaefer232"] = np.zeros(500)
roi_list_accel["schaefer454"] = np.zeros(500)


# true = complete; false = already in env
flag = True

# =====================================================================================================================

if(len(sys.argv) == 3):
    working_dir = sys.argv[1]
    data_dir = sys.argv[2]
else:
    working_dir = r"D:\research\MRI_newstuff\CamCAN\analysis_all"
    data_dir = r"D:\research\MRI_newstuff\CamCAN\data"

# main src directory
src_dir = os.path.join(working_dir, "src")
if not os.path.exists(src_dir):
    os.makedirs(src_dir)
#else:
    #TODO
    #cr.delete_folder_contents(src_dir)

# =====================================================================================================================


def reset_file(title):
    new_file = os.path.join(working_dir, title)
    if os.path.exists(new_file):
        f = open(new_file,'r+')
        f.truncate(0)
        f.close()
    else:
        open(new_file, 'a').close()
    return new_file

def open_new(title):
    new_file = reset_file(title)
    f_new = open(new_file,'w')
    return f_new

def open_new_src(title, n='\n'):
    new_file = os.path.join(src_dir, title)
    if os.path.exists(new_file):
        f = open(new_file,'r+')
        f.truncate(0)
        f.close()
    else:
        open(new_file, 'a').close()
    f_new = open(new_file,'w', newline=n)
    return f_new


def read_rois():

    for mod in roi_list:
        print(mod)
        file = open(roi_location[mod], "r")
        data = list(csv.reader(file))
        file.close()
        
        for item in data:
            roi = item[2]
            num = int(item[0])
            lh = True
            if 'schaefer' in mod:
                lh = 'LH' in item[1]
            elif 'bn' in mod:
                lh = '_L_' in item[1]
            elif 'glasser' in mod:
                lh = num <= 200
            prefix = ""
            if lh:
                prefix = "lh"
            else:
                prefix = "rh"
            full_roi = prefix + "_" + roi
            if not full_roi in list(roi_list[mod].keys()):
                roi_list[mod][full_roi] = []
            roi_list[mod][full_roi].append(num)
            
        for item in data:
            roi = item[2]
            num = int(item[0])
            lh = True
            if 'schaefer' in mod:
                lh = 'LH' in item[1]
            elif 'bn' in mod:
                lh = '_L_' in item[1]
            elif 'glasser' in mod:
                lh = num <= 200
            prefix = ""
            if lh:
                prefix = "lh"
            else:
                prefix = "rh"
            full_roi = prefix + "_" + roi
            roi_list_accel[mod][num] = int(list(roi_list[mod].keys()).index(full_roi) + 1)

    return

# =====================================================================================================================

 
    

read_rois()




  

methods_matrix = {}
methods_roi = {}
    

# add stats functions - stat mod needs to be unique
methods_matrix["diff_mat"] = (lambda x, y : matrix_difference(x, y))
methods_matrix["diff_mat_mst"] = (lambda x, y : MST_difference(x, y))
methods_matrix["diff_mat_rel"] = (lambda x, y : matrix_difference_rel(x, y))
methods_matrix["diff_mat_rmds"] = (lambda x, y : matrix_rmds(x, y))
methods_roi["diff_roi_rel"] = (lambda x, y : roi_difference_rel(x, y))


# create empty files for stats

stat_files = {}
connectivity_vs_files = {}

Imatch_arrays = {}
Inonmatch_arrays = {}

for stat in methods_matrix:
    stat_files[stat] = open_new("stat_matrix_" + stat + "_overview.csv")
    stat_files[stat].write("mod/scanner, id, contrast, repro, match_mean, match_std, nonmatch_mean, nonmatch_std, diff_in_std\n")
    Imatch_arrays[stat] = []
    Inonmatch_arrays[stat] = []
    
for stat in methods_roi:
    stat_files[stat] = open_new("stat_roi_" + stat + "_overview.csv")
    stat_files[stat].write("mod/scanner, id, contrast, repro, match_mean, match_std, nonmatch_mean, nonmatch_std, diff_in_std\n")
    Imatch_arrays[stat] = []
    Inonmatch_arrays[stat] = []
    
    
# numpy.random.rand(5,5)
    
# =====================================================================================================================

def maximum_spanning_tree(A):
    return binary(-minimum_spanning_tree(csr_matrix(-A)).toarray().astype(float))

def MST_difference(a, b):
    return matrix_difference(maximum_spanning_tree(np.abs(a)), maximum_spanning_tree(np.abs(b)))

def matrix_difference(a, b):
    diff = np.sum(np.abs(a - b))
    return diff

def matrix_difference_rel(a, b):
    diff = np.mean(2 * np.nan_to_num(np.abs(a - b) / (np.abs(a) + np.abs(b))))
    return diff


def matrix_rmds(a, b):
    diff = 0
    diff_matrix =  (a - b) * (a - b)
    diff = np.sum(diff_matrix)
    diff = np.sqrt(diff) / len(a)
    return diff

def roi_difference_rel(a, b):
    if (np.abs(a) + np.abs(b)) == 0:
        sim = 0.0
    else:
        sim = 2 * np.abs(a - b) / (np.abs(a) + np.abs(b))
    return sim


def binary(con):
    c = np.copy(con)
    c[c > 0] = 1
    c[c < 0] = -1
    return c

def abs_con(con):
    c = np.copy(con)
    for x in range(len(con)):
        for y in range(len(con)):
            if con[y][x] < 0:
                c[y][x] = - con[y][x]
            else:
                c[y][x] = con[y][x]
    return c

def binary_filter(con, percentage):
    c = np.copy(con)
    maximum = np.amax(con)
    minimum = np.amin(con)
    average = 0.5*(maximum + minimum)
    ran = 0.5 * (maximum - minimum)
    for x in range(len(con)):
        for y in range(len(con)):
            if con[y][x] > percentage * ran + average:
                c[y][x] = 1
            elif con[y][x] < average - percentage * ran:
                c[y][x] = -1
            else:
                c[y][x] = 0
    return c

def value_filter(con, percentage):
    c = np.copy(con)
    maximum = np.amax(con)
    minimum = np.amin(con)
    average = 0.5*(maximum + minimum)
    ran = 0.5 * (maximum - minimum)
    for x in range(len(con)):
        for y in range(len(con)):
            if con[y][x] > percentage * ran + average:
                c[y][x] = con[y][x]
            elif con[y][x] < average - percentage * ran:
                c[y][x] = con[y][x]
            else:
                c[y][x] = 0
    return c

def value_filter_range(con, p_lower, p_upper):
    c = np.copy(con)
    maximum = np.amax(con)
    minimum = np.amin(con)
    average = 0.5*(maximum + minimum)
    ran = 0.5 * (maximum - minimum)
    for x in range(len(con)):
        for y in range(len(con)):
            if con[y][x] > p_upper * ran + average:
                c[y][x] = 0
            elif con[y][x] < average + p_lower * ran:
                c[y][x] = 0
            else:
                c[y][x] = con[y][x]
    return c

def remove_zeros(connectome):
    con = np.copy(connectome)
    con = con[~np.all(con == 0, axis=1)]
    con = con[:, ~np.all(con == 0, axis=0)]
    return con



def get_max(connectome, count):
    con = np.copy(connectome)
    maxima = []
    for i in range(count):
        maximum = np.amax(con)
        pos = np.unravel_index(con.argmax(), con.shape)
        maxima.append((maximum, pos))
        con[pos[0]][pos[1]] = -50
        con[pos[1]][pos[0]] = -50
    return maxima

def get_max_all(connectome):
    con = np.copy(connectome)
    maxima = []
    while True:
        maximum = np.amax(con)
        if maximum == 0.0:
            break
        pos = np.unravel_index(con.argmax(), con.shape)
        maxima.append((maximum, pos))
        con[pos[0]][pos[1]] = -50
        con[pos[1]][pos[0]] = -50
    return maxima

def to_csv(maxima):
    c = ""
    for i in range(len(maxima)):
        c = c + str(maxima[i][0]) + ", " + str(maxima[i][1][0]) + ", " + str(maxima[i][1][1]) + "\n"
    return c

def plot_connectome(con):
    fig = plt.figure(figsize=(10, 6))
        
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(con)
    ax.set_aspect('equal')
        
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()

def get_bins(con):
    maximum = np.amax(con)
    minimum = np.amin(con)
    #average = 0.5*(maximum + minimum)
    ran = (maximum - minimum)
    bins = np.zeros((21))
    for x in range(len(con)):
        for y in range(len(con)):
            v = int(20.0 * (con[y][x] - minimum) / ran) 
            bins[v] = bins[v] + 1
    return bins

def remove_from_con(con, remove):
    c = np.copy(con)
    for i in remove:
        c[i[1][0]][i[1][1]] = 0
        c[i[1][1]][i[1][0]] = 0
    return c

def merge_arrays(a, b):
    c = []
    for i in a:
        c.append((i[0], i[1]))
    for i in b:
        c.append((i[0], i[1]))
    return c

def save_max(con, mod, scanner, title):
    noise_upper = value_filter_range(con, 0.5, 1.0)
    noise_upper_max = to_csv(get_max_all(noise_upper))
    file = open(os.path.join(src_dir, title + "_" + mod + "_" + cr.get_scanner_name(scanner, patient_data_files) + ".csv"), "w")
    file.write(noise_upper_max)
    file.close()
    
def save_max_abs(con, mod, scanner, title):
    noise_upper = value_filter_range(np.abs(con), -0.5, 1.0)
    noise_upper_max = to_csv(get_max_all(noise_upper))
    file = open(os.path.join(src_dir, title + "_" + mod + "_" + cr.get_scanner_name(scanner, patient_data_files) + ".csv"), "w")
    file.write(noise_upper_max)
    file.close()
    
def save_min(con, mod, scanner, title):
    save_max(-1.0 * con, mod, scanner, title)

def save_con(con, mod, scanner, title):
    cr.save_connectome(con, src_dir, title + "_" + mod + "_" + cr.get_scanner_name(scanner, patient_data_files))
    with open(os.path.join(src_dir, title + "_" + mod + "_" + cr.get_scanner_name(scanner, patient_data_files) + ".csv"),'w', newline='') as myfile:
        wr = csv.writer(myfile,delimiter=',')
        wr.writerows(con)
        
def save_con_cbar(con, mod, scanner, title, cmin, cmax):
    cr.save_connectome_cbar(con, src_dir, title + "_" + mod + "_" + cr.get_scanner_name(scanner, patient_data_files), cmin, cmax)
    with open(os.path.join(src_dir, title + "_" + mod + "_" + cr.get_scanner_name(scanner, patient_data_files) + ".csv"),'w', newline='') as myfile:
        wr = csv.writer(myfile,delimiter=',')
        wr.writerows(con)
        
def new_similarity(a, b):
    sim = 0
    for x in range(len(a)):
        for y in range(len(a)):
            if not (np.abs(a[x][y]) + np.abs(b[x][y])) == 0:
                sim = sim + 2 * np.abs(a[x][y] - b[x][y]) / (np.abs(a[x][y]) + np.abs(b[x][y]))
    return sim


def scannermod_id(mod, scanner):
    mod_id = 0
    
    if "dmri" in mod:
        mod_id = 0
    elif "fmri" in mod:
        mod_id = 8
        
    if "th" in mod or "mtn" in mod:
        mod_id = mod_id + 1.5
    
    # bn is 0, cba to code it in
    if "glasser" in mod:
        mod_id = mod_id + 0.2
    elif "schaefer116" in mod:
        mod_id = mod_id + 0.4
    elif "schaefer232" in mod:
        mod_id = mod_id + 0.6
    elif "schaefer454" in mod:
        mod_id = mod_id + 0.8
    
    # scanner: 0 - prisma, 1 - trio
    mod_id = mod_id + 4 * scanner
    return mod_id

def roi_identifier(mod, label_id):
    if "bn" in mod:
        for roi, l in roi_list["bn"].items():
            if label_id in l:
                return list(roi_list["bn"].keys()).index(roi) + 1
    elif "glasser" in mod:
        for roi, l in roi_list["glasser"].items():
            if label_id in l:
                return list(roi_list["glasser"].keys()).index(roi) + 1
    elif "schaefer116" in mod:
        for roi, l in roi_list["schaefer116"].items():
            if label_id in l:
                return list(roi_list["schaefer116"].keys()).index(roi) + 1
    elif "schaefer232" in mod:
        for roi, l in roi_list["schaefer232"].items():
            if label_id in l:
                return list(roi_list["schaefer232"].keys()).index(roi) + 1
    elif "schaefer454" in mod:
        for roi, l in roi_list["schaefer454"].items():
            if label_id in l:
                return list(roi_list["schaefer454"].keys()).index(roi) + 1
    return 0

def max_roi(mod):
    for m in ["bn", "glasser", "schaefer116", "schaefer232", "schaefer454"]:
        if m in mod:
            return len(list(roi_list[m].keys())) + 1
    return 0
    

def roi_identifier_accel(mod, label_id):
    for m in ["bn", "glasser", "schaefer116", "schaefer232", "schaefer454"]:
        if m in mod:
            return roi_list_accel[m][label_id]
    return 0

def analyse_similarities(Imatch, Inonmatch):
    if np.mean(Inonmatch) > 0:
        contrast = (np.mean(Inonmatch) - np.mean(Imatch)) / (np.mean(Inonmatch) + np.mean(Imatch))
        repro = (np.mean(Inonmatch) - np.mean(Imatch) - 1.96 * np.std(Imatch) - 1.96 * np.std(Inonmatch)) / (np.mean(Inonmatch) + np.mean(Imatch))
    else:
        contrast = -5
        repro = -5
    
    if (np.std(Imatch) + np.std(Inonmatch)) > 0:
        diff_in_std = (np.amin(Inonmatch) - np.amax(Imatch)) / (np.std(Imatch) + np.std(Inonmatch))
    else:
        diff_in_std = -5
        
    return (contrast, repro, np.mean(Imatch), np.std(Imatch), np.mean(Inonmatch), np.std(Inonmatch), diff_in_std)

# =====================================================================================================================






cr.init()
if not 'map_same' in locals() or flag:
    patient_data_files, path_connectome_main = cr.read_path_structure(data_dir)
    map_cor = cr.read_patient_data(patient_data_files)
    map_same = cr.create_patient_data_map(map_cor)

# connectome basic
if not 'connectome_list' in locals() or flag:
    cr.format_connectome_data(path_connectome_main)
    connectome_list = cr.read_all_connectome_data(path_connectome_main)

# single scanner
if not 'scanner_separated_list' in locals() or flag:
    scanner_separated_list = cr.generate_scanner_separated_list(connectome_list, map_cor)
    

# =====================================================================================================================

ICC_file_dp = open_new("ICCs_dmri_prisma.csv")
ICC_file_dt = open_new("ICCs_dmri_trio.csv")
ICC_file_fp = open_new("ICCs_fmri_prisma.csv")
ICC_file_ft = open_new("ICCs_fmri_trio.csv")


def stuff(mod, scanner):
    # complete analysis
    
    print(mod + " / " + cr.get_scanner_name(scanner, patient_data_files))
    scanner_name = str(cr.get_scanner_name(scanner, patient_data_files))
    
    if "fmri" in mod:
        if "t" in scanner_name:
            ICC_file = ICC_file_ft
        else:
            ICC_file = ICC_file_fp
    else:
        if "t" in scanner_name:
            ICC_file = ICC_file_dt
        else:
            ICC_file = ICC_file_dp
    
    
    con_list = scanner_separated_list[mod][scanner]
    keys = list(con_list.keys())
    
    dimension = len(scanner_separated_list[mod][scanner][list(scanner_separated_list[mod][scanner].keys())[0]])

    
    # remove average to just get features
    mean = np.zeros((dimension, dimension))
    l = 0
    for cbu_id, con in con_list.items():
        l = l + 1
        mean = mean + con
    mean = mean / l
    con_list_new = {}
    for cbu_id, con in con_list.items():
        con_list_new[cbu_id] = con - mean
        #con_list_new[cbu_id] = con
    
        
    
    #save_max_abs(mean, mod, scanner, "roi_mean_max")
    save_con_cbar(mean, mod, scanner, "conn_mean", 0.0, 0.9)
    
    std_matrix = np.std(list(con_list_new.values()),axis=0)
    
    #print(numpy.std([a,b,c],axis=0))
    
 
    
  
    
    # ============================================================================
    print("matrix-wise stuff")
    # matrix-wise stuff
    
    Imatch = {}
    Inonmatch = {}
    
    MSb = {}
    MSw = {}
    
    for k in keys:
        MSb[k] = []
        MSw[k] = 0

    for stat in methods_matrix:
        Imatch[stat] = []
        Inonmatch[stat] = []
    
    for x in range(len(keys)):
        for y in range(x + 1, len(keys)):
            k1 = keys[x]
            k2 = keys[y]
            for stat, fun in methods_matrix.items():
                sim = fun(con_list_new[k1], con_list_new[k2])
                match = (k2 == cr.get_same_scanner_match(k1, map_same))
                if(match):
                    Imatch[stat].append(sim)
                else:
                    Inonmatch[stat].append(sim)
            rmds = matrix_rmds(con_list_new[k1], con_list_new[k2])
            if(match):
                MSw[k1] = rmds
                MSw[k2] = rmds
            else:
                MSb[k1].append(rmds)
                MSb[k2].append(rmds)
    
    # ICC stuff
    ICC = {}
    ICC_file.write(mod + "/" + scanner_name + ", ")
    for k in keys:
        ICC[k] = (np.mean(MSb[k]) - MSw[k]) / (np.mean(MSb[k]) + MSw[k])
    ICC_overall = np.mean(list(ICC.values()))
    for subject in map_same[scanner]:
        id1 = map_same[scanner][subject][0]
        id2 = map_same[scanner][subject][1]
        ICC_file.write(str(ICC[id1]) + ", " + str(ICC[id2]) + ", " + ", ")
    ICC_file.write(" , " + str(ICC_overall) + "\n")
    
    
    # general stuff
    for stat in methods_matrix:
        (contrast, repro, match_mean, match_std, nonmatch_mean, nonmatch_std, diff_in_std) = analyse_similarities(Imatch[stat], Inonmatch[stat]) 
        
        body = mod + "/" + cr.get_scanner_name(scanner, patient_data_files) + ", " + str(scannermod_id(mod, scanner))
        body = body + ", " + str(contrast) + ", " + str(repro)
        body = body + ", " + str(match_mean) + ", " + str(match_std)
        body = body + ", " + str(nonmatch_mean) + ", " + str(nonmatch_std)
        body = body + ", " + str(diff_in_std)
        stat_files[stat].write(body + "\n")
        
        for i in Imatch[stat]:
            Imatch_arrays[stat].append((i, scannermod_id(mod, scanner)))
        for i in Inonmatch[stat]:
            Inonmatch_arrays[stat].append((i, scannermod_id(mod, scanner)))
        
    
    # ============================================================================
    print("roi-wise stuff")
    # roi-wise stuff
    
    matrices_contrast = {}
    matrices_repro = {}
    matrices_diff = {}
    connectivity_vs_file = {}
    connectivity_vs_file_rois = {}
    
    connectivity_rois = {}
    
    for stat in methods_roi:
        matrices_contrast[stat] = np.zeros((dimension, dimension))
        matrices_repro[stat] = np.zeros((dimension, dimension))
        matrices_diff[stat] = np.zeros((dimension, dimension))
        connectivity_vs_file[stat] = open_new_src("connectivity_vs_" + stat + "_" + mod + "_" + cr.get_scanner_name(scanner, patient_data_files) + ".csv")
        connectivity_vs_file_rois[stat] = open_new_src("rois_connectivity_vs_" + stat + "_" + mod + "_" + cr.get_scanner_name(scanner, patient_data_files) + ".csv", n='')
        connectivity_rois[stat] = []
        for i in range(3 * max_roi(mod)):
            connectivity_rois[stat].append([])
    
    tmp = 0.0
    # TODO: stuff
    if True:
        for x in range(dimension):
            for y in range(dimension):
                
                per = (dimension * x + y) * 100.0 / dimension / dimension 
                if per > tmp:
                    print(str(tmp) + "%")
                    tmp = tmp + 10.0
                
                Imatch_roi = {}
                Inonmatch_roi = {}
                
                for stat in methods_roi:
                    Imatch_roi[stat] = []
                    Inonmatch_roi[stat] = []
                
                for i in range(len(keys)):
                    for j in range(i + 1, len(keys)):
                        k1 = keys[i]
                        k2 = keys[j]
                        
                
                        a = con_list_new[k1][x][y]
                        b = con_list_new[k2][x][y]
                        for stat, fun in methods_roi.items():
                            sim = fun(a, b)
                            
                            match = (k2 == cr.get_same_scanner_match(k1, map_same))
                            if(match):
                                Imatch_roi[stat].append(sim)
                            else:
                                Inonmatch_roi[stat].append(sim)
                    
                for stat in methods_roi:
                    (contrast, repro, match_mean, match_std, nonmatch_mean, nonmatch_std, diff_in_std) = analyse_similarities(Imatch_roi[stat], Inonmatch_roi[stat]) 
                    matrices_contrast[stat][x][y] = contrast
                    matrices_repro[stat][x][y] = repro
                    matrices_diff[stat][x][y] = diff_in_std
                    
                    conn = mean[x][y]
                    
                    if not conn == 0:
                        body = str(conn) + ", " + str(contrast) + ", " + str(repro) + ", " + str(roi_identifier_accel(mod, x)) + ", " + str(roi_identifier_accel(mod, y))
                        connectivity_vs_file[stat].write(body + "\n")
                        if roi_identifier_accel(mod, x) == roi_identifier_accel(mod, y):
                            connectivity_rois[stat][int(3 * roi_identifier_accel(mod, x))].append(conn)
                            connectivity_rois[stat][int(3 * roi_identifier_accel(mod, x) + 1)].append(contrast)
                            connectivity_rois[stat][int(3 * roi_identifier_accel(mod, x) + 2)].append(repro)
                
    # take avg and save
    for stat in methods_roi:
        connectivity_vs_file[stat].close()
        
        writer = csv.writer(connectivity_vs_file_rois[stat])
        writer.writerows(connectivity_rois[stat])
            
        connectivity_vs_file_rois[stat].close()
        
        
        save_con(matrices_contrast[stat], mod, scanner, "stat_roi_contrast_" + stat)
        save_con(matrices_repro[stat], mod, scanner, "stat_roi_repro_" + stat)
        save_con(matrices_diff[stat], mod, scanner, "stat_roi_diff_" + stat)
        
        contrast = np.mean(matrices_contrast[stat])
        repro = np.mean(matrices_repro[stat])
        
        body = mod + "/" + cr.get_scanner_name(scanner, patient_data_files) + ", " + str(scannermod_id(mod, scanner))
        body = body + ", " + str(contrast) + ", " + str(repro)
        stat_files[stat].write(body + "\n")
    

    
    # ============================================================================
    
 
    
    # roi-wise stuff
    if False:
        contrast_array = np.zeros((dimension, dimension))
        repro_array = np.zeros((dimension, dimension))
        tmp = 0.0
        for a in range(len(repro_array)):
            for b in range(len(repro_array)):
                per = (len(repro_array) * a + b) * 100.0 / len(repro_array) / len(repro_array) 
                if per > tmp:
                    print(str(tmp) + "%")
                    tmp = tmp + 10.0
                Imatch=[]
                Inonmatch=[]
                for x in range(len(keys)):
                    for y in range(x + 1, len(keys)):
                        k1 = keys[x]
                        k2 = keys[y]
                        v1 = con_list_new[k1][a][b]
                        v2 = con_list_new[k2][a][b]
                        if (np.abs(v2) + np.abs(v1)) == 0:
                            sim = 1.0
                        else:
                            sim = np.abs(v2 - v1) / (np.abs(v2) + np.abs(v1))
                        match = (k2 == cr.get_same_scanner_match(k1, map_same))
                        if(match):
                            Imatch.append(sim)
                        else:
                            Inonmatch.append(sim)
                contrast = (np.mean(Inonmatch) - np.mean(Imatch)) / (np.mean(Inonmatch))
                repro = (np.mean(Inonmatch) - np.mean(Imatch) - 1.96 * np.std(Imatch) - 1.96 * np.std(Inonmatch)) / (np.mean(Inonmatch))
                contrast_array[a][b] = contrast
                repro_array[a][b] = repro
        # normalise
        
        cr.plot_connectome(contrast_array)
        cr.plot_connectome(repro_array)
        save_max(contrast_array, mod, scanner, "roi_contrast_max")
        save_max(repro_array, mod, scanner, "roi_repro_max")
        save_min(contrast_array, mod, scanner, "roi_contrast_min")
        save_min(repro_array, mod, scanner, "roi_repro_min")
        
        contrast_array[contrast_array == 0.0] = -5.0
        repro_array[repro_array == 0.0] = -5.0
        save_con_cbar(contrast_array, mod, scanner, "conn_roi_contrast", -0.8, 0.9)
        save_con_cbar(repro_array, mod, scanner, "conn_roi_repro", -4.0, 0.5)
        contrast_array[contrast_array == -5.0] = 0.0
        repro_array[repro_array == -5.0] = 0.0
        
    else:
        contrast_array = np.zeros((dimension, dimension))
        repro_array = np.zeros((dimension, dimension))
        print("skipping to save time")
    print("==========================================================")
    return


def stuff_repro(mod):
    
    # prep
    print(mod + " / cross-scanner")
    con_list = scanner_separated_list[mod]
    keys = [list(con_list[0].keys()), list(con_list[1].keys())]
    
    dimension = len(scanner_separated_list[mod][0][list(scanner_separated_list[mod][0].keys())[0]])

    
    # remove average to just get features
    mean = [np.zeros((dimension, dimension)), np.zeros((dimension, dimension))]
    con_list_new = [{}, {}]
    l = 0
    for s in [0, 1]:
        for cbu_id, con in con_list[s].items():
            l = l + 1
            mean[s] = mean[s] + con
        mean[s] = mean[s] / l

        for cbu_id, con in con_list[s].items():
            con_list_new[s][cbu_id] = con - mean[s]
            #con_list_new[cbu_id] = con
    
    print(dimension)
    print(cr.similarity(mean[0], mean[1]))
    print(mean[0])
    print(mean[1])
    
    std_matrix_scanner = [np.std(list(con_list_new[0].values()),axis=0), np.std(list(con_list_new[1].values()),axis=0)]
    std_matrix_both = np.std(list(con_list_new[0].values()) + list(con_list_new[1].values()),axis=0)

    # # calculate ICCs
    # for subject in map_same[0]:
    #     # note: could use con_list_new, no difference
    #     ct1 = con_list[0][map_same[0][subject][0]]
    #     ct2 = con_list[0][map_same[0][subject][1]]
    #     cp1 = con_list[1][map_same[1][subject][0]]
    #     cp2 = con_list[1][map_same[1][subject][1]]
    #     MSw_t = (matrix_rmds(ct1, ct2))
    #     MSw_p = (matrix_rmds(cp1, cp2))
    #     MSb = (matrix_rmds(ct1, cp1) + matrix_rmds(ct1, cp2) + matrix_rmds(ct2, cp2) + matrix_rmds(ct2, cp1)) / 4
    
    #     ICC_t = (MSb - MSw_t) / (MSb + MSw_t)
    #     ICC_p = (MSb - MSw_p) / (MSb + MSw_p)
    #     print(MSw_t, MSw_p, " / ", MSb, " / ", ICC_t, ICC_p)
    
    # print("\n\n")    
    # for subject in map_same[0]:
    #     # note: dont use con_list_new
    #     ct1 = con_list_new[0][map_same[0][subject][0]]
    #     ct2 = con_list_new[0][map_same[0][subject][1]]
    #     cp1 = con_list_new[1][map_same[1][subject][0]]
    #     cp2 = con_list_new[1][map_same[1][subject][1]]
    #     MSw_t = (matrix_rmds(ct1, ct2))
    #     MSw_p = (matrix_rmds(cp1, cp2))
    #     MSb = (matrix_rmds(ct1, cp1) + matrix_rmds(ct1, cp2) + matrix_rmds(ct2, cp2) + matrix_rmds(ct2, cp1)) / 4
    
    #     ICC_t = (MSb - MSw_t) / (MSb + MSw_t)
    #     ICC_p = (MSb - MSw_p) / (MSb + MSw_p)
    #     print(MSw_t, MSw_p, " / ", MSb, " / ", ICC_t, ICC_p)
        
    
    return
    
    
def finish_writing():
    for stat in methods_matrix:
        file_new = open_new("stat_matrix_" + stat + "_sim.csv")
        for i in range(len(Inonmatch_arrays[stat])):
            if i < len(Imatch_arrays[stat]):
                body = str(Inonmatch_arrays[stat][i][0]) + ", " + str(Inonmatch_arrays[stat][i][1]) + ", " + str(Imatch_arrays[stat][i][0]) + ", " + str(Imatch_arrays[stat][i][1])
                file_new.write(body + "\n")
            else:
                body = str(Inonmatch_arrays[stat][i][0]) + ", " + str(Inonmatch_arrays[stat][i][1])
                file_new.write(body + "\n")
        file_new.close()
        
    for stat in methods_roi:
        file_new = open_new("stat_roi_" + stat + "_sim.csv")
        for i in range(len(Inonmatch_arrays[stat])):
            if i < len(Imatch_arrays[stat]):
                body = str(Inonmatch_arrays[stat][i][0]) + ", " + str(Inonmatch_arrays[stat][i][1]) + ", " + str(Imatch_arrays[stat][i][0]) + ", " + str(Imatch_arrays[stat][i][1])
                file_new.write(body + "\n")
            else:
                body = str(Inonmatch_arrays[stat][i][0]) + ", " + str(Inonmatch_arrays[stat][i][1])
                file_new.write(body + "\n")
        file_new.close()
    
    ICC_file_dp.close()
    ICC_file_dt.close()
    ICC_file_fp.close()
    ICC_file_ft.close()
    return



print("==========================================================")
print("Begin analysis")


#stuff_repro("fmri_glasser")

#stuff("dmri_glasser", 0)
#stuff("fmri_glasser", 0)

for m in list(scanner_separated_list.keys()):
    print(m)
    if not "mri" in m:
        continue
    stuff(m, 0)
    stuff(m, 1)

finish_writing()

for stat in methods_matrix:
    stat_files[stat].close()
for stat in methods_roi:
    stat_files[stat].close()
    


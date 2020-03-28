# -*- coding: utf-8 -*-
"""
@author: Felix Menze
"""

import crram as cr
import sys
import os
import numpy as np
import csv
import matplotlib.pyplot as plt

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
#patient_data_files, path_connectome_main = cr.read_path_structure(data_dir)

patient_data_files, path_connectome_main = cr.read_path_structure(data_dir)
map_cor = cr.read_patient_data(patient_data_files)
map_same = cr.create_patient_data_map(map_cor)

# connectome basic
if not 'connectome_list' in locals() or flag:
    #connectome_list = cr.read_all_connectome_data(path_connectome_main)
    connectome_list = cr.read_all_connectome_data(path_connectome_main)

# single scanner
if not 'scanner_separated_list' in locals() or flag2:
    scanner_separated_list = cr.generate_scanner_separated_list(connectome_list, map_cor)

mean_connectome_list = cr.apply_to_scanner_specific_entries(scanner_separated_list, lambda x : cr.mean(x))
#cr.plot_connectome(mean_connectome_list["dmri"][0])
#cr.plot_connectome(mean_connectome_list["dmri"][1])

alpha = mean_connectome_list["dmri"][0]
beta = mean_connectome_list["dmri"][1]
gamma = mean_connectome_list["dmri"][4]
delta = mean_connectome_list["dmri"][2]
epsilon = mean_connectome_list["dmri"][3]

def in_reduced(i):
    if i >= 0 and i <= 1:
        return False
    if i >= 81 and i <= 181:
        return False
    if i >= 261 and i <= 359:
        return False
    return True

def in_roi(mod, x, y):
    if mod == "rh":
        if in_rh(x) and in_rh(y):
            return True
    if mod == "lh":
        if in_lh(x) and in_lh(y):
            return True
    if mod == "homo":
        if in_lh(x) and in_rh(y):
            return True
        if in_rh(x) and in_lh(y):
            return True
    if mod == "sub":
        if not in_lh(x) and not in_rh(x):
            return True
        if not in_lh(y) and not in_rh(y):
            return True
    return False

def in_rh(i):
    if i >= 79 and i <= 157:
        return True
    return False

def in_lh(i):
    if i >= 0 and i <= 78:
        return True
    return False
    
def reduce_connectome(connectome):
    #remove: 0-1, 81-181, 261-360, 202 removed in total
    con = np.zeros((177, 177))
    xx = 0
    yy = 0
    for x in range(len(connectome)):
        for y in range(len(connectome)):
            if in_reduced(y) and in_reduced(x):
                con[yy][xx] = connectome[y][x]
                yy = yy + 1
        yy = 0
        if in_reduced(x):
            xx = xx + 1             
    con[con == 0.0] = -50
    # remove low values and set them to -10
    con[con < - 5] = -5
    return con

def reduce_connectome_raw(connectome):
    #remove: 0-1, 81-181, 261-360, 202 removed in total
    con = np.zeros((177, 177))
    xx = 0
    yy = 0
    for x in range(len(connectome)):
        for y in range(len(connectome)):
            if in_reduced(y) and in_reduced(x):
                con[yy][xx] = connectome[y][x]
                yy = yy + 1
        yy = 0
        if in_reduced(x):
            xx = xx + 1             
    return con

def extract_region(connectome, roi):
    con = np.zeros((177, 177))
    for x in range(len(connectome)):
        for y in range(len(connectome)):
            if in_roi(roi, x, y):
                con[y][x] = connectome[y][x]
    con[con == 0.0] = -50
    # remove low values and set them to -10
    con[con < - 5] = -5
    return con

def extract_region_raw(connectome, roi):
    con = np.zeros((177, 177))
    for x in range(len(connectome)):
        for y in range(len(connectome)):
            if in_roi(roi, x, y):
                con[y][x] = connectome[y][x]
    return con

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






# =================================================================================
    

cross_sim = np.zeros((5,5))
for x in range(5):
    for y in range(5):
        cross_sim[y][x] = cr.similarity(mean_connectome_list["dmri"][y], mean_connectome_list["dmri"][x])

plot_connectome(cross_sim)

ac1 = abs_con(epsilon - delta)
ac2 = abs_con(epsilon - alpha)

ac1_r = reduce_connectome_raw(ac1)
ac2_r = reduce_connectome_raw(ac2)

ac1_rh = remove_zeros(extract_region_raw(ac1_r, "rh"))
ac2_rh = remove_zeros(extract_region_raw(ac2_r, "rh"))
ac1_lh = remove_zeros(extract_region_raw(ac1_r, "lh"))
ac2_lh = remove_zeros(extract_region_raw(ac2_r, "lh"))
dac_rh = ac2_rh - ac1_rh
dac_lh = ac2_lh - ac1_lh

plot_connectome(dac_rh)
plot_connectome(binary(dac_rh))


std = np.std(remove_zeros(dac_rh)) / 0.15
nnt = value_filter_range(remove_zeros(dac_rh), 9.0 * std, 1.0)
mmt = -1 * value_filter_range(remove_zeros(dac_rh), -1.0, -9.0 * std)
plot_connectome(nnt)
plot_connectome(mmt)

"""

ac1 = abs_con(alpha - gamma)
ac2 = abs_con(beta - delta)

ac1_r = reduce_connectome_raw(ac1)
ac2_r = reduce_connectome_raw(ac2)

ac1_rh = remove_zeros(extract_region_raw(ac1_r, "rh"))
ac2_rh = remove_zeros(extract_region_raw(ac2_r, "rh"))
ac1_lh = remove_zeros(extract_region_raw(ac1_r, "lh"))
ac2_lh = remove_zeros(extract_region_raw(ac2_r, "lh"))
dac_rh = ac2_rh - ac1_rh
dac_lh = ac2_lh - ac1_lh

#plot_connectome(dac_rh)
#plot_connectome(binary(dac_rh))
#plot_connectome(dac_lh)

std = np.std(remove_zeros(dac_lh)) / 0.025
nnt = value_filter_range(remove_zeros(dac_lh), 1.96 * std, 1.0)
mmt = -1 * value_filter_range(remove_zeros(dac_lh), -1.0, -1.96 * std)
avg = value_filter_range(remove_zeros(dac_lh), -1.96 * std, 1.96 * std)
#plot_connectome(nnt)
#plot_connectome(mmt)
#plot_connectome(avg)
#print(to_csv(get_max_all(nnt)))
#print("=======")
#print(to_csv(get_max_all(mmt)))





"""


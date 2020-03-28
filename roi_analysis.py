# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:02:39 2020

@author: Felix
"""

import numpy as np
import os
import csv
import matplotlib.pyplot as plt

path_in = "C:/Projects/MRI/patientdata/analysis/"

control = os.path.join(path_in, "cluster1_dmri_alpha_beta.txt")
pddata = path_in + "cluster1_dmri_gamma_delta.txt"


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

def read_connectome(path_connectome):
     with open(path_connectome, 'r') as f:
       reader = csv.reader(f, delimiter=" ")
       con = list(reader)
       connectome = np.array(con).astype(np.float)

     return connectome

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

con_c = reduce_connectome(read_connectome(control))
con_p = reduce_connectome(read_connectome(pddata))


con_c_r = reduce_connectome_raw(read_connectome(control))
con_p_r = reduce_connectome_raw(read_connectome(pddata))

#print(con_c)
#plot_connectome(con_c)
#plot_connectome(con_p)
#plot_connectome(extract_region(con_c, "rh"))
#plot_connectome(extract_region(con_c, "lh"))
#plot_connectome(extract_region(con_c, "homo"))
#plot_connectome(extract_region(con_c, "sub"))

c_rh = extract_region(con_c, "rh")
c_lh = extract_region(con_c, "lh")
c_homo = extract_region(con_c, "homo")
c_sub = extract_region(con_c, "sub")

p_rh = extract_region(con_p, "rh")
p_lh = extract_region(con_p, "lh")
p_homo = extract_region(con_p, "homo")
p_sub = extract_region(con_p, "sub")

d_rh = c_rh - p_rh
d_lh = c_lh - p_lh
d_homo = c_homo - p_homo
d_sub = c_sub - p_sub

#plot_connectome(d_rh)

#plot_connectome(remove_zeros(d_rh))
#plot_connectome(remove_zeros(d_lh))
#plot_connectome(remove_zeros(np.tril(d_homo)))
#plot_connectome(remove_zeros(binary(d_lh)))
#plot_connectome(remove_zeros(binary(d_rh)))
#plot_connectome(binary(remove_zeros(np.tril(d_homo))))

d_hemisphere = 0.5 * (remove_zeros(d_rh) + remove_zeros(d_lh))
#plot_connectome(d_hemisphere)

maxima = get_max(d_hemisphere, 5)




c_rh_sum = np.sum(extract_region_raw(con_c_r, "rh"))
p_rh_sum = np.sum(extract_region_raw(con_p_r, "rh"))


c_rh_r = extract_region_raw(con_c_r, "rh")
c_lh_r = extract_region_raw(con_c_r, "lh")
c_sub_r = extract_region_raw(con_c_r, "sub")
c_homo_r = extract_region_raw(con_c_r, "homo")
p_rh_r = extract_region_raw(con_p_r, "rh")
p_lh_r = extract_region_raw(con_p_r, "lh")
p_sub_r = extract_region_raw(con_p_r, "sub")
p_homo_r = extract_region_raw(con_p_r, "homo")
d_rh_r = c_rh_r - p_rh_r
d_lh_r = c_lh_r - p_lh_r
d_sub_r = c_sub_r - p_sub_r
d_homo_r = c_homo_r - p_homo_r

#plot_connectome(remove_zeros(d_rh_r))
#plot_connectome(binary(remove_zeros(d_rh_r)))

std = np.std(remove_zeros(d_homo_r)) / 40
nnt = value_filter_range(remove_zeros(d_homo_r), 3 * std, 1.0)
mmt = -1 * value_filter_range(remove_zeros(d_homo_r), -1.0, -3 * std)
plot_connectome(nnt)
plot_connectome(mmt)
print(to_csv(get_max_all(nnt)))
print("=======")
print(to_csv(get_max_all(mmt)))
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 10:57:31 2020

@author: Felix
"""


import csv
import numpy as np
import os, shutil, sys
import matplotlib.pyplot as plt
import ntpath
import re
import math
from datetime import datetime
import inspect


def init():
    """
    Initialises crram - call before using.
  
    """
    print("CRRAM 2020 v1.6\n")
    if not os.path.exists("log"):
        os.makedirs("log")
    log_file = os.path.join("log", "log.txt")
    if os.path.exists(log_file):
        with open(log_file) as f:
            first_line = f.readline()
            f.close()
            log_file_new = log_file.replace(".txt", first_line.replace("\n", "") + ".txt")
            os.rename(log_file, log_file_new)
    f = open(log_file, "w")
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    f.write(dt_string + "\nConnectivity Repeatability and Reproducibility Analysis Module - log file\n\n")
    f.close()


# =====================================================================================================================

#utility 
    
def log(*objects, l=0, end='\n'):
    """
    Custom log function which automatically writes into the log file (not implemented yet)
    
    Parameters
    ----------
    *objects : 
        Arguments to be printed
    l : int
        Layer of identation, default is 0
    end : str
        End sequence, default is newline
    """
    f = open(os.path.join("log", "log.txt"), "a")
    if(l > 0):
        log_str = ' '*(2 * l) + '|'
        print(log_str, *objects, end=end)
        print(log_str, *objects, end=end, file=f)
    else:
        print(*objects, end=end)
        print(*objects, end=end, file=f)
    f.close()
        
    return


def delete_folder_contents(folder):
    """
    Deletes the contents of the specified folder.
    
    Parameters
    ----------
    folder : str
        Complete path to the folder which will be deleted
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return

def read_images_into_list(folder, mod):
    """
    Reads file names of images into a list including metadata
    
    Parameters
    ----------
    folder : str
        Complete path to the source folder of the images
    mod : str
        Image modifier used for filename identification, expected format of "myalphanumericalname12345mod.png"
    Returns
    -------
    array
        Array with entries of the type (filename, [myalphanumericalname, 12345])
    """
    image_list = []
    for filename in sorted(os.listdir(folder)):
        if mod + ".png" in filename:
            #meta = str(filename).replace(mod + ".png", "")
            meta = str(filename)
            match = re.match(r"([a-z]+)([0-9]+)", meta, re.I)
            if match:
                meta = match.groups()
            image_list.append((filename, meta))
    return image_list



def read_modality_scanner_format_into_list(folder, mod):
    """
    Reads file names of images into a list including metadata, uses the modality_scanner format
    
    Parameters
    ----------
    folder : str
        Complete path to the source folder of the images
    mod : str
        Image modifier used for filename identification, expected format of "modality_scanner12345mod.png"
    Returns
    -------
    array
        Array with entries of the type (filename, [modality, _, scanner, _, 12345])
    """
    image_list = []
    for filename in sorted(os.listdir(folder)):
        if mod + ".png" in filename:
            #meta = str(filename).replace(mod + ".png", "")
            meta = str(filename)
            match = re.match(r"([a-z]+)(_)([a-z]+)(_)", meta, re.I)
            if match:
                meta = match.groups()
            image_list.append((filename, meta))
    return image_list
# =====================================================================================================================

# html creation

def src(s):
    """
    Short utility function linking to the src folder (see readme).
    
    Parameters
    ----------
    s : str
        Filename in the src folder
    
    Returns
    -------
    path
        Joined path of src folder and filename
    """
    return os.path.join("src", s)

def generate_css():
    """
    Generates the css containing stylesheets and alike.
    
    Returns
    -------
    str
        Content of the css as a string
    """
    text = """
             /* Style the button that is used to open and close the collapsible content */
        .collapsible {
          background-color: #eee;
          color: #444;
          cursor: pointer;
          padding: 18px;
          width: 100%;
          border: none;
          text-align: left;
          outline: none;
          font-size: 15px;
        }
        
        /* Add a background color to the button if it is clicked on (add the .active class with JS), and when you move the mouse over it (hover) */
        .active, .collapsible:hover {
          background-color: #ccc;
        }
        
        /* Style the collapsible content. Note: hidden by default */
        .content {
          padding: 0 18px;
          display: none;
          overflow: hidden;
          background-color: #f1f1f1;
        } 
    """
    return text


def generate_js():
    """
    Generates the javascript content of the html page (Automatically called in :func:`~crram.html_end`).
    
    Returns
    -------
    str
        js content of the html page as a string
    """
    
    text = """<script>
                var coll = document.getElementsByClassName("collapsible");
                var i;
                
                for (i = 0; i < coll.length; i++) {
                  coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.display === "block") {
                      content.style.display = "none";
                    } else {
                      content.style.display = "block";
                    }
                  });
                }
                </script>"""
    return text

def html_header():
    """
    Generates the header of the html page.
    
    Returns
    -------
    str
        Header of the html page as a string
    """
    body = """<!DOCTYPE html>
                    <html>
                        <head>
                            <title>CRRAM</title>
                            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                            <link rel="stylesheet" href="styles.css">
                            <style>
                                html,body { width: 100%; height: 100%; }
                            </style>
                        </head>"""                
    body += "<div id='top'>Connectome Repeatability and Reproducibility Analysis Module CRRAM<br></div>"
    
    #TODO: add metadata at start of body?
    
    return body

def html_end():
    """
    Generates the end of the html page. Calls :func:`~crram.generate_js`.
    
    Returns
    -------
    str
        End of the html page as a string
    """
    body = generate_js() + """</html>"""
    return body

def html_patient_data_table(map_same, patient_data_files, title, mod='tab'):
    """
    Generates html code adding the supplied correspondence map as a table in a collapsible section.
    Also generates optional jump-to buttons as additions to the header.
    
    Parameters
    ----------
    map_same : list
        Correspondence map
    patient_data_files : list
        List of patient data files
    title : str
        Title of the table
    mod : str
        Modifier used for html reference purposes
    
    Returns
    -------
    tuple(str, str)
        2-tuple of html body and optional addition to the header
    """
    body = "<button type='button' id='" + mod + "' class='collapsible'>" + title + "</button><div class='content'>"
    
    body += "<div><body><b>" + title + "</b><br></body><body><a href='#top'>top</a></body></div>"
    for scanner in range(len(map_same)):
        name = get_scanner_name(scanner, patient_data_files)
        name = "Scanner: " + name + "&nbsp;" * 3 * (6 - len(name)) + " / ID: " + str(scanner)
        body +=  "<table style='width:90%'><tr><th>" + name + "</th><th> </th><th> </th></tr>"
        for patient_id, cbu_id_list in map_same[scanner].items():
            if(len(cbu_id_list) > 1):
                body += "<tr><td>Patient ID: " + str(patient_id) + "</td><td>" + str(cbu_id_list[0]) + "</td><td>" + str(cbu_id_list[1]) + "</td></tr>"
            else:
                 body += "<tr><td>Patient ID: " + str(patient_id) + "</td><td>" + str(cbu_id_list[0]) + "</td><td>" + str(cbu_id_list[0]) + "</td></tr>"
        body +=  """</table> """
    body += "</div>"
    
    
    header_addition = "<body><a href='#" + mod + "'>Jump to " + mod + "</a><br></body>"
    return (body, header_addition)


def html_image_series(img_dir, title, mod='raw'):
    """
    Generates html code adding the supplied image series as a collapsible section.
    Also generates optional jump-to buttons as additions to the header.
    
    Parameters
    ----------
    img_dir : str
        Complete path to the directory containing all images
    title : str
        Title of the collapsible section
    mod : str
        Image modifier used for filename identification
    
    Returns
    -------
    tuple(str, str)
        2-tuple of html body and optional addition to the header
    """
    
    body = "<button type='button' id='" + mod + "' class='collapsible'>" + title + "</button><div class='content'>"
    
    body += "<div><body><b>" + title + "</b><br></body><body><a href='#top'>top</a></body></div>"
    body += "<div class='row'><div class='column'>"
    for (file, meta) in read_images_into_list(img_dir, mod):
        img_name = "ID: " + meta[1] + ", modality: " + meta[0] + ", modifier: " + mod
        body += "<img src='" + src(file) + "' alt='" + img_name + "' title='" + img_name  + "' style='width:45%;'>"
    
    body += """</div></div>"""
    body += "</div>"
    
    header_addition = "<body><a href='#" + mod + "'>Jump to " + mod + "</a><br></body>"
    return (body, header_addition)

def html_modality_scanner_series(img_dir, title, mod=''):
    """
    Generates html code adding the supplied series in the modality_scanner format as a collapsible section.
    Also generates optional jump-to buttons as additions to the header.
    
    Parameters
    ----------
    img_dir : str
        Complete path to the directory containing all images
    title : str
        Title of the collapsible section
    mod : str 
        Image modifier used for filename identification
    
    Returns
    -------
    tuple(str, str)
        2-tuple of html body and optional addition to the header
    """
    body = "<button type='button' id='" + mod + "' class='collapsible'>" + title + "</button><div class='content'>"
    
    body += "<div><body><b>" + title + "</b><br></body><body><a href='#top'>top</a></body></div>"
    body += "<div class='row'><div class='column'>"
    for (file, meta) in read_modality_scanner_format_into_list(img_dir, mod):
        img_name = "Modality: " + meta[0] + ", scanner: " + meta[2] + ", modifier: " + mod
        body += "<img src='" + src(file) + "' alt='" + img_name + "' title='" + img_name  + "' style='width:45%;'>"
    
    body += """</div></div>"""
    body += "</div>"
    
    header_addition = "<body><a href='#" + mod + "'>Jump to " + mod + "</a><br></body>"
    return (body, header_addition)

# =====================================================================================================================

def write_meta_data(src_dir, patient_data_files, path_connectome_main, map_cor, map_same):
    """
    Writes a metadata text file containing patient data and alike
    
    Parameters
    ----------
    src_dir : str
        Complete path to the directory containing all images and alike.
    patient_data_files: list
        List of patient data info as generated by :func:`~crram.read_path_structure`
    path_connectome_main : str
        Complete path to the main directory containing all connectome data
    map_cor : list
        List of test series sorted by modality and scanner as generated by :func:`~crram.read_patient_data`
    map_same : list
        List of test series sorted by modality and scanner with grouped test ids for the same patient id as generated by :func:`~crram.create_patient_data_map`
    """
    metadata_path = os.path.join(src_dir, "info.txt")
    f = open(metadata_path,'w')
    # scanner names, modalities, subject count x scanner x tests
    f.write("Info\n\n")
    
    f.write("Modalities: ")
    path_connectome_all_modalities = os.listdir(path_connectome_main)
    for m in path_connectome_all_modalities:
        f.write(str(m) + " ")
    f.write("\n")
    
    f.write("Scanners: ")
    for i in range(len(patient_data_files)):
        f.write(ntpath.basename(patient_data_files[i]).replace("subjects_","").replace(".csv","") + " ")
    f.write("\n")
    
    
    f.write("Test series: ")
    f.write(str(len(map_cor[0])) + " tests on " + str(len(map_same)) + " scanners (" + str(len(map_same)*len(map_cor[0])) + " total) ")
    f.write("for " + str(len(map_same[0])) + " unique patients")
    f.write("\n")
    
    f.close()
    return

def read_meta_data(src_dir):
    #TODO
    return

def get_scanner_name(scanner, patient_data_files):
    """
    Returns the scanner name as found in the given patient data file.
    
    Parameters
    ----------
    scanner : int
        The key associated with the scanner, typically an integer starting at 0
    patient_data_files : list
        Path to the patient data file structure as given by :func:`~crram.read_path_structure`
    
    Returns
    -------
    str
        The name of the scanner as specified by the patient data files (check the readme for file name conventions)
    """
    return ntpath.basename(patient_data_files[int(scanner)]).replace("subjects_","").replace(".csv","")

def read_path_structure(data_dir):
    """
    Reads the path structure, assuming it follows the convention specified in the readme.
    
    Parameters
    ----------
    data_dir : str
        Full location of the data directory
    
    Returns
    -------
    Tuple
        The location of the patient data files as well as the path to the connectomes as a 2-tuple
    """
    log("Reading data structure...")
    path_patient_data_files = os.path.join(data_dir, "subject_data")
    patient_data_files = list(map(lambda x:os.path.join(path_patient_data_files, x), os.listdir(path_patient_data_files)))
    path_connectome_main = os.path.join(data_dir, "connectomes")
    log("Patient data: subject info found for <", len(patient_data_files),"> scanners", l=1)
    log("Connectome data: connectome data found for <", len(os.listdir(path_connectome_main)), "> modalities", l=1)
    log("Reading data structure complete\n")
    return patient_data_files, path_connectome_main

def format_connectome_data(path_connectome_main):
    """
    Formats the connectome data (i.e. converts from comma separation to space separation which is used in this module).
    
    Parameters
    ----------
    path_connectome_main : str
        Path to the main connectome data as given by :func:`~crram.read_path_structure`
    """
    log("Formatting connectome data...")
    path_connectome_all_modalities = os.listdir(path_connectome_main)
    log("Connectome data found for <", len(path_connectome_all_modalities),"> modalities", l=1)
    for m in path_connectome_all_modalities:
        log("Reading modality <", m, ">", l=2)
        tmp_dir = os.path.join(path_connectome_main, m)
        all_connectome_files = os.listdir(tmp_dir)
        log("Connectomes found: <", len(all_connectome_files), ">", l=2)
        for c in all_connectome_files:
            current_file = os.path.join(tmp_dir, c)
            log("Current file: <", c, "> .... ", end = '', l=3)
            with open(current_file, 'r+') as f:
                text = f.read()
                if "," in text:
                    log("Rewriting format")
                    f.seek(0)
                    f.truncate()
                    f.write(text.replace(',', ' '))
                else:
                    log("No formatting necessary")
                    
    log("Formatting connectome data complete\n")
    return
    
def read_all_connectome_data(path_connectome_main):
    """
    Reads all connectomes into a modality connectome (mc) nested list.
    
    Parameters
    ----------
    path_connectome_main : str
        Path to the main connectome data as given by :func:`~crram.read_path_structure`
    
    Returns
    -------
    list
        Connectome data in a nested list, mc format
    """
    log("Reading all connectomes...")
    connectome_list_all_modalities = {}
    path_connectome_all_modalities = os.listdir(path_connectome_main)
    log("Connectome data found for <", len(path_connectome_all_modalities),"> modalities", l=1)
    for m in path_connectome_all_modalities:
        log("Reading connectome data for modality <", m, ">", l=2)
        tmp_dir = os.path.join(path_connectome_main, m)
        connectome_list = read_connectome_data(tmp_dir)
        connectome_list_all_modalities[m] = connectome_list
    
    log("Reading all connectomes complete\n")
    return connectome_list_all_modalities

def read_patient_data(paths_cor):
    """
    Reads patient data into a [modality][scanner](patient ID, series ID) structure
    
    Parameters
    ----------
    paths_cor : list
        List of paths to patient data files as generated by :func:`~crram.read_path_structure`
    
    Returns
    -------
    list
        List containing patient ID - series ID correspondences
    """
    
    log("Reading patient data...")
    map_cor = []
    log("Found patient data for <", len(paths_cor), "> scanners", l=1)
    for i in range(len(paths_cor)):
        log("Reading patient data from file <", paths_cor[i], ">", l=2)
        with open(paths_cor[i], 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
            data.pop(0)
            log("Reading patient data for <", len(data), "> individual tests", l=3)
            for val in data:
                del val[0]
                del val[1]
                del val[2:5]
            map_cor.append(data)
    log("Reading patient data complete\n")
    return map_cor


def create_patient_data_map(map_cor):
    """
    Converts the patient ID - series ID correspondence map to a merged list containing all corresponding series IDs, i.e. [modality][scanner](patient ID, series ID) => [modality][scanner][patient_id](all series IDs)
    
    Parameters
    ----------
    map_cor : list
        Correspondence map as generated by :func:`~crram.read_patient_data`
    
    Returns
    -------
    list
        List of the ms[patient ID] format
    """
    log("Creating patient data map...")
    map_same = []
    for l in map_cor:
        lookup = {}
        for entry in l:
            key = int(entry[0])
            val = int(entry[1])
            lookup.setdefault(key,[])
            lookup[key].append(val)
        map_same.append(lookup)
    log("Mapped <", len(map_same[0]),"> unique patients to <", len(map_same),"> x <", len(map_cor[0]), "> tests", l=1)
    log("Creating patient data map complete\n")
    return map_same



def read_connectome_data(path_connectome):
    """
    Reads all connectomes at the given path into a mc [modality][connectome] structure
    
    Parameters
    ----------
    path_connectome : str
        Complete path to the directory containing all connectome data
    
    Returns
    -------
    list
        List of the mc format
    """
    log("Reading connectome data...", l=2)
    connectome_list = {}
    directory = os.fsencode(path_connectome)
    log("Connectomes found: <", len(os.listdir(directory)), ">", l=3)
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         if filename.endswith(".csv"):
             cbu_id = filename.replace("connectome_CBU","").replace(".csv","")
             location = os.path.join(path_connectome, filename)
             log("Reading connectome <", filename, "> with ID <", cbu_id, ">", l=4)
             with open(location, 'r') as f:
               reader = csv.reader(f, delimiter=" ")
               con = list(reader)
               connectome_list[int(cbu_id)] = np.array(con).astype(np.float)
             continue
         else:
             continue
    log("Reading connectome data complete", l=2)
    return connectome_list


def plot_all(connectome_list, img_dir, mod=''):
    """
    Saves all connectomes in the supplied list with mc structure in the default format
    
    Parameters
    ----------
    connectome_list : list
        List of connectomes, mc structure
    img_dir : str
        Complete path to the directory containing all images
    mod : str
        Image modifier used for filename identification
    """
    log("Generating plots for all connectomes in the given list...")
    for modality, sublist in connectome_list.items():
        for cbu_id, connectome in sublist.items():
            log("Generating plot for modality <", modality ,"> and id <", cbu_id ,">", l=1)
            save_connectome(connectome, img_dir, str(modality) + str(cbu_id) + mod)
    log("Generating plots complete\n")
    return

def plot_all_s(connectome_list, img_dir, patient_data_files, mod=''):
    """
    Saves all connectomes in the supplied list with mc structure in the modality_scanner format
    
    Parameters
    ----------
    connectome_list : list
        List of connectomes, mc structure
    img_dir : str
        Complete path to the directory containing all images
    mod : str
        Image modifier used for filename identification
    """
    log("Generating plots for all connectomes in the given list...")
    for modality, sublist in connectome_list.items():
        for scanner, scanner_sublist in sublist.items():
            for cbu_id, connectome in scanner_sublist.items():
                log("Generating plot for modality <", modality ,"> and id <", cbu_id ,"> on scanner <", scanner, ">", l=1)
                save_connectome(connectome, img_dir, str(modality) + get_scanner_name(scanner, patient_data_files) + str(cbu_id) + mod)
    log("Generating plots complete\n")
    return

def plot_all_binary(connectome_list, img_dir, mod=''):
    """
    Saves a binary version of all connectomes in the supplied list with mc structure in the default format
    
    Parameters
    ----------
    connectome_list : list
        List of connectomes, mc structure
    img_dir : str
        Complete path to the directory containing all images
    mod : str
        Image modifier used for filename identification
    """
    log("Generating binary plots for all connectomes in the given list...")
    for modality, sublist in connectome_list.items():
        for cbu_id, connectome in sublist.items():
            log("Generating plot for modality <", modality ,"> and id <", cbu_id ,">", l=1)
            save_connectome(generate_normalised_connectome(connectome), img_dir, str(modality) + str(cbu_id) + mod)
    log("Generating binary plots complete\n")
    return

def create_same_scanner_merge(connectome_list, map_same):
    """
    Deprecated function, creates mean and absolute difference for a same scanner two connectome merge, deprecated connectome list format.
    
    Parameters
    ----------
    connectome_list : list
        mc structure
    map_same : list
        Correspondence map
    
    Returns
    -------
    tuple
        2-tuple containing mean and delta
    """
    subjects_delta = []
    subjects_mean = []
    for i in range(len(map_same)):
        delta = {}
        mean = {}
        for key, value in map_same[i].items():
            mean[key] = 0.5 * (connectome_list[value[0]] + connectome_list[value[1]])
            delta[key] = abs(connectome_list[value[0]] - connectome_list[value[1]])
        subjects_delta.append(delta)
        subjects_mean.append(mean)
    return subjects_mean, subjects_delta

def save_connectome(connectome, img_dir, title):
    """
    Saves supplied connectome.
    
    Parameters
    ----------
    connectome : 2D array
        Connectome to be saved
    img_dir : str
        Complete path to the image directory
    title:
        title of the connectome
    """
    log("Saving connectome <", title, ">", l=2)
    fig = plt.figure(figsize=(18, 10))
        
    ax = fig.add_subplot(111)
    ax.set_title(title)
    plt.imshow(connectome)
    ax.set_aspect('equal')
        
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    fig.savefig(os.path.join(img_dir, title + ".png"), dpi=100)
    plt.close()


def plot_comparison_matrix(matrix, ordering):
    """
    Plots the supplied comparison matrix, both axes for the same data set
    
    Parameters
    ----------
    matrix : 2D array
        Comparison matrix
    ordering : list
        List of IDs 
    """
    log("Plotting comparison matrix starting with id <", ordering[0], ">", l=2)
    fig = plt.figure(figsize=(18, 10))
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(matrix)
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(matrix.shape[1]), minor=False)
    ax.set_yticks(np.arange(matrix.shape[0]), minor=False)
    ax.invert_yaxis()
    ax.set_xticklabels(ordering, minor=False)
    ax.set_yticklabels(ordering, minor=False)
        
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()
    plt.close()
    return

def plot_comparison_matrix_xy(matrix, orderingx, orderingy):
    """
    Plots the supplied comparison matrix, different data sets on different axes
    
    Parameters
    ----------
    matrix : 2D array
        Comparison matrix
    orderingx : list
        List of IDs for the x-axis
    orderingy : list
        List of IDs for the y-axis
    """
    log("Plotting comparison matrix starting with id <", orderingx[0], "/", orderingy[0], ">", l=2)
    fig = plt.figure(figsize=(18, 10))
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(matrix)
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(matrix.shape[1]), minor=False)
    ax.set_yticks(np.arange(matrix.shape[0]), minor=False)
    ax.invert_yaxis()
    ax.set_xticklabels(orderingx, minor=False)
    ax.set_yticklabels(orderingy, minor=False)
        
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()
    plt.close()
    return

def save_comparison_matrix(matrix, ordering, img_dir, title):
    """
    Saves the supplied comparison matrix, both axes for the same data set
    
    Parameters
    ----------
    matrix : 2D array
        Comparison matrix
    ordering : list
        List of IDs 
    img_dir : str
        Complete path to the directory containing all images
    title : str
        Title of the comparison map
    """
    log("Saving comparison matrix <", title ,"> starting with id <", ordering[0], ">", l=2)
    fig = plt.figure(figsize=(18, 10))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    plt.imshow(matrix)
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(matrix.shape[1]), minor=False)
    ax.set_yticks(np.arange(matrix.shape[0]), minor=False)
    ax.invert_yaxis()
    ax.set_xticklabels(ordering, minor=False)
    ax.set_yticklabels(ordering, minor=False)
        
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    fig.savefig(os.path.join(img_dir, title + ".png"), dpi=100)
    np.savetxt(os.path.join(img_dir, title + ".csv"), matrix, delimiter=",")
    plt.close()
    return

def save_comparison_matrix_xy(matrix, orderingx, orderingy, img_dir, title):
    """
    Saves the supplied comparison matrix, different data sets on different axes
    
    Parameters
    ----------
    matrix : 2D array
        Comparison matrix
    orderingx : list
        List of IDs for the x-axis
    orderingy : list
        List of IDs for the y-axis
    img_dir : str
        Complete path to the directory containing all images
    title : str
        Title of the comparison map
    """
    log("Plotting comparison matrix <", title, "> starting with id <", orderingx[0], "/", orderingy[0], ">", l=2)
    fig = plt.figure(figsize=(18, 10))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    plt.imshow(matrix)
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(matrix.shape[1]), minor=False)
    ax.set_yticks(np.arange(matrix.shape[0]), minor=False)
    ax.invert_yaxis()
    ax.set_xticklabels(orderingx, minor=False)
    ax.set_yticklabels(orderingy, minor=False)
        
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    fig.savefig(os.path.join(img_dir, title + ".png"), dpi=100)
    np.savetxt(os.path.join(img_dir, title + ".csv"), matrix, delimiter=",")
    plt.close()
    return


# generates reduced connectomes and scanner averaged maps, structure mc => msc
def generate_reduced_connectomes(connectome_list, map_cor):
    """
    Generates reduced connectome, i.e. the connectome minus the averaged scanner map
    
    Parameters
    ----------
    connectome_list : list
        List of connectomes in mc format
    map_cor : list
        Correspondence map
    
    Returns
    -------
    list
        List of reduced connectomes in msc format
    """
    log("Generating reduced connectomes...")
    connectome_list_reduced = {}
    scanner_specific_maps = {}  
    for modality, sublist in connectome_list.items():
         scanner_maps = split_list_by_scanner(sublist, map_cor)  
         connectome_list_reduced[modality] = {}
         scanner_specific_maps[modality] = {}
         for scanner, scanner_sublist in scanner_maps.items():
             log("Calculating scanner specific map for modality <", str(modality), "> on scanner <", str(scanner), ">", l=1)
             connectome_list_reduced[modality][scanner] = {}
             
             l = len(scanner_sublist[list(scanner_sublist.keys())[0]])
             con = np.zeros((l, l))
             for cbu_id, connectome in scanner_sublist.items():
                 con = con + connectome
             con = con / len(list(scanner_sublist.keys()))
             
             scanner_specific_maps[modality][scanner] = con
             
             for cbu_id, connectome in scanner_sublist.items():
                 log("Generating reduced connectome with id <", str(cbu_id), "> for modality <", str(modality), "> on scanner <", str(scanner), ">", l=2)
                 connectome_list_reduced[modality][scanner][cbu_id] = connectome - scanner_specific_maps[modality][scanner]
    log("Generating reduced connectomes complete\n")
    return (connectome_list_reduced, scanner_specific_maps)

# splits connectome data into scanner separated list, structure mc => msc
def generate_scanner_separated_list(connectome_list, map_cor):
    log("Converting data structure type mc to type msc...")
    """
    Generates a connectome list separated by scanner, i.e. turns the mc format into the msc format.
    
    Parameters
    ----------
    connectome_list : list
        List of connectomes in the mc format
    map_cor : list
        Correspondence map
    
    Returns
    -------
    list
        List of connectomes in the msc format
    """
    connectome_list_specific = {}
    for modality, sublist in connectome_list.items():
         scanner_maps = split_list_by_scanner(sublist, map_cor)  
         connectome_list_specific[modality] = {}
         for scanner, scanner_sublist in scanner_maps.items():
             connectome_list_specific[modality][scanner] = {}
             for cbu_id, connectome in scanner_sublist.items():
                 log("Connectome <", cbu_id,"> correlated to scanner <", scanner,">", l=2)
                 connectome_list_specific[modality][scanner][cbu_id] = connectome
    log("Converting data structure type mc to type msc complete\n")
    return connectome_list_specific

# msc to scm structure
def generate_modality_separated_list(scanner_separated_list):
    modality_separated_list = {}
    for modality, modality_sublist in scanner_separated_list.items():
        for scanner, scanner_sublist in modality_sublist.items():
            for cbu_id, connectome in scanner_sublist.items():
                if not scanner in modality_separated_list:
                    modality_separated_list[scanner] = {}
                if not cbu_id in modality_separated_list[scanner]:
                    modality_separated_list[scanner][cbu_id] = {}
                modality_separated_list[scanner][cbu_id][modality] = connectome
    
    return modality_separated_list

def generate_scanner_separated_from_modality_separated_list(modality_separated_list):
    scanner_separated_list = {}
    for scanner, scanner_sublist in modality_separated_list.items():
        for cbu_id, sublist in scanner_sublist.items():
            for modality, connectome in sublist.items():
                if not modality in scanner_separated_list:
                    scanner_separated_list[modality] = {}
                if not scanner in scanner_separated_list[modality]:
                    scanner_separated_list[modality][scanner] = {}
                scanner_separated_list[modality][scanner][cbu_id] = connectome
    
    return scanner_separated_list

def remove_zero_connections(modality_separated_list):
    modality_separated_list_updated = {}
    dimension = 0
    for scanner, scanner_sublist in modality_separated_list.items():
        modality_separated_list_updated[scanner] = {}
        for cbu_id, sublist in scanner_sublist.items():
            modality_separated_list_updated[scanner][cbu_id] = {}
            # remove fmri zeros
            fmri = np.copy(sublist["fmri"])
            dmri = np.copy(sublist["dmri"])
            dmri = dmri[~np.all(fmri == 0, axis=1)]
            dmri = dmri[:, ~np.all(fmri == 0, axis=0)]
            fmri = fmri[~np.all(fmri == 0, axis=1)]
            fmri = fmri[:, ~np.all(fmri == 0, axis=0)]
            modality_separated_list_updated[scanner][cbu_id]["fmri"] = fmri
            modality_separated_list_updated[scanner][cbu_id]["dmri"] = dmri
            if len(fmri) > dimension:
                dimension = len(fmri)
                
    # bring to same length
    for scanner, scanner_sublist in modality_separated_list_updated.items():
        for cbu_id, sublist in scanner_sublist.items():
            for modality, connectome in sublist.items():
                connectome_new = np.zeros((dimension, dimension))
                for x in range(len(connectome)):
                    for y in range(len(connectome)):
                        connectome_new[y][x] = connectome[y][x]
                modality_separated_list_updated[scanner][cbu_id][modality] = connectome_new
    
    return (modality_separated_list_updated, dimension)

# splits list of ids into a scanner separated list, structure [...]c => [...]sc
def split_list_by_scanner(connectome_list, map_cor):
    """
    Splits the supplied single-level connectome list into one separated by scanner, i.e. [...]c => [...]sc
    
    Parameters
    ----------
    connectome_list : list
        List of connectomes without modality or scanner layers
    map_cor : list
        Correspondence map
    
    Returns
    -------
    list
        List of connectomes in the sc format
    """
    log("Splitting list by scanner...", l=1)
    scanner_separated_list = {}
    for scanner in range(len(map_cor)):
        scanner_separated_list[scanner] = {}
    for cbu_id, connectome in connectome_list.items():
        s = 0
        for scanner in range(len(map_cor)):
            for correlation in map_cor[scanner]:
                if(str(correlation[1]) == str(cbu_id)):
                    s = scanner
        log("Connectome <", cbu_id,"> correlated to scanner <", s,">", l=2)            
        scanner_separated_list[s][cbu_id] = connectome
    log("Splitting list by scanner complete", l=1)
    return scanner_separated_list

# applies function to connectome
def apply_to_single_connectome(connectome, function):
    """
    Applies the supplied lambda to the supplied connectome
    
    Parameters
    ----------
    connectome : 2D array
        Connectome
    function : lambda
        Function to be applied
    
    Returns
    -------
    function(2D array)
        Result of the function
    """
    log("Applying function <", inspect.getsource(function),"> to connectome", l=3)
    return function(connectome)

# applies function to data structure underlying modality level
def apply_to_all_modality_data(connectome_list, function):
    """
    Applies the supplied lambda to the data structure underlying each [modality].
    
    Parameters
    ----------
    connectome_list : list
        List of any data, first-level key correspondds to modality
    function : lambda
        Function to be applied
    
    Returns
    -------
    list
        List of results of applied function
    """
    log("Applying function <", inspect.getsource(function),"> to all modality data...")
    new_connectome_list = {}
    for modality, sublist in connectome_list.items():
        log("Applying to modality data for modality <", modality,">", l=1)
        new_connectome_list[modality] = function(sublist)
    log("Applying function to all modality data complete\n")
    return new_connectome_list

# applies function to all connectomes individually, structure msc
def apply_to_scanner_specific_connectomes(scanner_separated_list, function):
    """
    Applies the supplied lambda to each connectome in a msc type data structure.
    
    Parameters
    ----------
    scanner_separated_list : list
        List of msc type
    function : lambda
        Function to be applied
    
    Returns
    -------
    list
        List of results of applied function, msc type
    """
    log("Applying function <", inspect.getsource(function),"> to scanner specific connectomes...")
    new_connectome_list = {}
    for modality, sublist in scanner_separated_list.items():
        new_connectome_list[modality] = {}
        for scanner, scanner_sublist in sublist.items():
            new_connectome_list[modality][scanner] = {}
            for cbu_id, connectome in scanner_sublist.items():
                log("Applying function to connectome <", cbu_id,">", l=1)
                new_connectome_list[modality][scanner][cbu_id] = apply_to_single_connectome(scanner_separated_list[modality][scanner][cbu_id], function)
    log("Applying function to scanner specific connectomes complete\n")
    return new_connectome_list

def apply_to_modality_specific_connectomes(scanner_separated_list, modality_x, function):
    """
    Applies the supplied lambda to each connectome with one specific modality in a msc type data structure, copies all connectomes not matching the modality.
    
    Parameters
    ----------
    scanner_separated_list : list
        List of msc type
    modality_x : str
        Modality for which the function is to be applied
    function : lambda
        Function to be applied
    
    Returns
    -------
    list
        List of results of applied function, msc type
    """
    log("Applying function <", inspect.getsource(function),"> to all connectomes of modality <", modality_x,">...")
    new_connectome_list = {}
    for modality, sublist in scanner_separated_list.items():
        new_connectome_list[modality] = {}
        for scanner, scanner_sublist in sublist.items():
            new_connectome_list[modality][scanner] = {}
            for cbu_id, connectome in scanner_sublist.items():
                if modality == modality_x:
                    log("Applying function to connectome <", cbu_id,">", l=1)
                    new_connectome_list[modality][scanner][cbu_id] = apply_to_single_connectome(scanner_separated_list[modality][scanner][cbu_id], function)
                else:
                    log("Skipping connectome <", modality_x,"> different modality", l=1)
                    new_connectome_list[modality][scanner][cbu_id] = scanner_separated_list[modality][scanner][cbu_id]
    log("Applying function to all connectomes of modality <", modality_x,"> complete\n" )
    return new_connectome_list

# applies function to all same scanner pairs, structure msc
def apply_to_scanner_specific_connectome_pairs(scanner_separated_list, function):
    """
    Applies the supplied lambda to each pair of connectomes in a msc structure, separated by scanner.
    
    Parameters
    ----------
    scanner_separated_list : list
        List of msc type
    function : lambda
        Function to be applied
    
    Returns
    -------
    tuple
        2-tuple of 2D matrix of function results and array containing all connectome IDs in order
    """
    log("Applying function <", inspect.getsource(function),"> to scanner specific connectome pairs...")
    result = {}
    ordering = {}
    for modality, sublist in scanner_separated_list.items():
        result[modality] = {}
        ordering[modality] = {}
        for scanner, scanner_sublist in sublist.items():
            ordering[modality][scanner] = list(scanner_sublist.keys())
            result[modality][scanner] = np.zeros((len(list(scanner_sublist.keys())), len(list(scanner_sublist.keys()))))
            for i in range(len(ordering[modality][scanner])):
                for j in range(len(ordering[modality][scanner])):
                    log("Applying function to <", ordering[modality][scanner][j],"> and <", ordering[modality][scanner][i],">", l=1)
                    tmp = function(scanner_sublist[ordering[modality][scanner][j]], scanner_sublist[ordering[modality][scanner][i]])
                    result[modality][scanner][j][i] = tmp
    log("Applying function to scanner specific connectome pairs complete\n")
    return (result, ordering)

# applies function to all cross scanner pairs, structure msc
def apply_to_cross_scanner_pairs(scanner_separated_list, function):
    """
    Applies the supplied lambda to each pair of connectomes in a msc structure, one from each scanner type, type 0 and type 1
    
    Parameters
    ----------
    scanner_separated_list : list
        List of msc type
    function : lambda
        Function to be applied
    
    Returns
    -------
    tuple
        3-tuple of 2D matrix of function results and array containing all connectome IDs in order for each scanner
    """
    log("Applying function <", inspect.getsource(function),"> to cross scanner pairs...")
    result = {}
    ordering1 = {}
    ordering2 = {}
    for modality, sublist in scanner_separated_list.items():
        scanner1 = list(sublist.keys())[0]
        scanner2 = list(sublist.keys())[1]
        result[modality] = np.zeros((len(list(sublist[scanner1].keys())), len(list(sublist[scanner2].keys()))))
        ordering1[modality] = list(sublist[scanner1].keys())
        ordering2[modality] = list(sublist[scanner2].keys())
        for i in range(len(ordering2[modality])):
                for j in range(len(ordering1[modality])):
                    log("Applying function to <", ordering1[modality][j],"> and <", ordering2[modality][i],">", l=1)
                    tmp = function(sublist[scanner1][ordering1[modality][j]], sublist[scanner2][ordering2[modality][i]])
                    result[modality][j][i] = tmp
    log("Applying function to cross scanner pairs complete, returning result\n")
    return (result, ordering1, ordering2)

def apply_to_cross_scanner_pairs_specify_pair(scanner_separated_list, x, y, function):
    """
    Applies the supplied lambda to each pair of connectomes in a msc structure, one from each scanner type, type 0 and type 1
    
    Parameters
    ----------
    scanner_separated_list : list
        List of msc type
    function : lambda
        Function to be applied
    
    Returns
    -------
    tuple
        3-tuple of 2D matrix of function results and array containing all connectome IDs in order for each scanner
    """
    log("Applying function <", inspect.getsource(function),"> to cross scanner pairs...")
    result = {}
    ordering1 = {}
    ordering2 = {}
    for modality, sublist in scanner_separated_list.items():
        scanner1 = list(sublist.keys())[x]
        scanner2 = list(sublist.keys())[y]
        result[modality] = np.zeros((len(list(sublist[scanner1].keys())), len(list(sublist[scanner2].keys()))))
        ordering1[modality] = list(sublist[scanner1].keys())
        ordering2[modality] = list(sublist[scanner2].keys())
        for i in range(len(ordering2[modality])):
                for j in range(len(ordering1[modality])):
                    log("Applying function to <", ordering1[modality][j],"> and <", ordering2[modality][i],">", l=1)
                    tmp = function(sublist[scanner1][ordering1[modality][j]], sublist[scanner2][ordering2[modality][i]])
                    result[modality][j][i] = tmp
    log("Applying function to cross scanner pairs complete, returning result\n")
    return (result, ordering1, ordering2)
        
        
        
    
def apply_to_scanner_specific_entries(scanner_separated_list, function):
    """
    Applies the supplied lambda to each scanner specific sublist in a ms[...] structure.
    
    Parameters
    ----------
    scanner_separated_list : list
        List of msc type
    function : lambda
        Function to be applied
    
    Returns
    -------
    list
        List of results of applied function, ms[...] type
    """
    result = {}
    log("Applying function <", inspect.getsource(function),"> to scanner specific entries...")
    for modality, sublist in scanner_separated_list.items():
        result[modality] = {}
        for scanner, scanner_sublist in sublist.items():
            log("Applying function to connectome list of scanner <", scanner,"> for modality <", modality,">", l=1)
            result[modality][scanner] = function(scanner_sublist)          
    log("Applying function to scanner specific entries complete, returning result\n")
    return result

def apply_to_scanner_specific_entries_nr(scanner_separated_list, function):
    """
    Applies the supplied lambda to each scanner specific sublist in a ms[...] structure, no return values.
    
    Parameters
    ----------
    scanner_separated_list : list
        List of ms[...] type
    function : lambda
        Function to be applied
    """
    log("Applying function <", inspect.getsource(function),"> to scanner specific entries...")
    for modality, sublist in scanner_separated_list.items():
        for scanner, scanner_sublist in sublist.items():
            log("Applying function to connectome list of scanner <", scanner,"> for modality <", modality,">", l=1)
            function(scanner_sublist) 
    log("Applying function to scanner specific entries complete\n")
    return 

def apply_to_scanner_specific_entries_metadata_nr(scanner_separated_list, function):
    """
    Applies the supplied lambda to each scanner specific sublist in a ms[...] structure, no return values, supplies modality and scanner as additional arguments for function.
    
    Parameters
    ----------
    scanner_separated_list : list
        List of ms[...] type
    function : lambda
        Function to be applied
    """
    log("Applying function <", inspect.getsource(function),"> to scanner specific entries, supplied metadata as additional arguments...")
    for modality, sublist in scanner_separated_list.items():
        for scanner, scanner_sublist in sublist.items():
            log("Applying function to connectome list of scanner <", scanner,"> for modality <", modality,">", l=1)
            function(scanner_sublist, modality, scanner)       
    log("Applying function to scanner specific entries complete\n")
    return 

def apply_to_entries_metadata_nr(general_list, function):
    """
    Applies the supplied lambda to each modality specific sublist in a m[...] structure, no return values, supplies modality as additional argument for function.
    
    Parameters
    ----------
    scanner_separated_list : list
        List of m[...] type
    function : lambda
        Function to be applied
    """
    log("Applying function <", inspect.getsource(function),"> to modality sublists...")
    for modality, sublist in general_list.items():
        log("Applying function to sublist of modality <", modality,">", l=1)
        function(sublist, modality)  
    log("Applying function to modality sublists complete\n")          
    return 

# sorts array with same x and y ordering by correspondence, two corresponding test series will be adjacent
def sort_array_by_correspondence(array, ordering, map_same):
    """
    Sorts 2D array so that adjacent entries correspond to matching connectome IDs.
    
    Parameters
    ----------
    array : 2D array
        Matrix containing the data, e.g. a comparison map
    ordering : array
        Initial ordering of connectome IDs in the supplied matrix
    map_same : list
        Correspondence map
    
    Returns
    -------
    tuple
        2-tuple of sorted matrix and sorted ordering
    """
    log("Sorting array according to correspondence map...", l=1)
    # both rows and columns
    order = ordering.copy()
    result = array.copy()
    
    for i in range(len(order)):
        # on element i, check neighbor
        ordered = False
        match = get_same_scanner_match(order[i], map_same)
        if match == 0:
            continue
        if (i < len(order) - 1 and order[i + 1] == match) or (i > 0 and order[i - 1] == match):
            ordered = True
        if not ordered:
            # swap match_pos and i+1
            match_pos = list(order).index(match)
            log("Swapping entries <", i + 1,"> and <", match_pos,">", l=2)
            order[match_pos] = order[i+1]
            order[i+1] = match
            order_map = np.arange(len(order))
            order_map[i+1] = match_pos
            order_map[match_pos] = i+1
            result = result[:, order_map]
            result = result[order_map, :]
    log("Sorting array according to correspondence map complete, returning result", l=1)
    return (result, order)

# finds the lowest values per row column individually, expects symmetrical x y correspondence
def find_best_matches_in_array(arr):
    """
    For a symmetrical matrix with irrelevant diagonal entries, greedily searches for global minima to find the best set of matches containing each row and column only once.
    
    Parameters
    ----------
    arr : 2D array
        Matrix containing the data
    
    Returns
    -------
    2D array
        Matrix containing best possible matches highlighted from best to worst, diagonal elements are highlighted with negative values for convenience
    """
    log("Searching for best matches in supplied array (sym)...", l=1)
    skip = []
    tmp = np.zeros((len(arr), len(arr)))
    flag = 1
    colour = 1
    while flag == 1:
        i = -1
        j = -1
        val = np.amax(arr)
        for x in range(len(arr)):
            for y in range(len(arr)):
                if x in skip or y in skip:
                    continue
                if x == y:
                    continue
                if arr[y][x] < val:
                    val = arr[y][x]
                    i = x
                    j = y
                
        if i == -1 or j == -1:
            flag = 0
            break
        tmp[j][i] = colour
        tmp[i][j] = colour
        tmp[i][i] = -1
        tmp[j][j] = -1
        log("Found new best match: <", i,"> / <", j,">", l=2)
        colour = colour - 1 / (len(arr) + 1)
        skip.append(i)
        skip.append(j)
        log("Reducing matrix", l=2)
    log("Searching for best matches in supplied array complete, returning result", l=1)
    return tmp

def find_best_matches_in_array_asym(arr):
    """
    For any matrix with independent horizontal and vertical entries, greedily searches for global minima to find the best set of matches containing each row and column only once.
    
    Parameters
    ----------
    arr : 2D array
        Matrix containing the data
    
    Returns
    -------
    2D array
        Matrix containing best possible matches highlighted from best to worst
    """
    log("Searching for best matches in supplied array (asym)...", l=1)
    skipx = []
    skipy = []
    tmp = np.zeros((len(arr), len(arr)))
    flag = 1
    colour = 1
    while flag == 1:
        i = -1
        j = -1
        val = np.amax(arr)
        for x in range(len(arr)):
            for y in range(len(arr)):
                if x in skipx or y in skipy:
                    continue
                if arr[y][x] < val:
                    val = arr[y][x]
                    i = x
                    j = y
                
        if i == -1 or j == -1:
            flag = 0
            break
        tmp[j][i] = colour
        log("Found new best match: <", i,"> / <", j,">", l=2)
        colour = colour - 1 / (len(arr) + 1)
        skipx.append(i)
        skipy.append(j)
        log("Reducing matrix", l=2)
    log("Searching for best matches in supplied array complete, returning result", l=1)
    return tmp

# finds the lowest possible values in the connectome, ignores 0, one per row/column, greedy
def find_best_matches_per_subject(arr):
    """
    For a symmetric matrix with irrelevant diagonal entries, finds the best and second best match per column individually.
    
    Parameters
    ----------
    arr : 2D array
        Matrix containing the data
    
    Returns
    -------
    2D array
        Matrix containing best possible matches with 1 for best and 0.5 for second best, diagonal highlighted for convenience
    """
    log("Searching for best matches per individual subject in supplied array...", l=1)
    tmp = np.zeros((len(arr), len(arr)))
    for x in range(len(arr)):
        min_f = np.amax(arr)
        min_s = np.amax(arr)
        i = 0
        j = 0
        p = 0
        q = 0
        for y in range(len(arr)):
            if arr[y][x] == 0:
                tmp[y][x] = -1
                continue
            if arr[y][x] < min_f:
                min_s = min_f
                p = i
                q = j
                min_f = arr[y][x]
                i = x
                j = y
            elif arr[y][x] < min_s:
                min_s = arr[y][x]
                p = x
                q = y
        tmp[j][i] = 1
        #tmp[i][j] = 0.7
        tmp[q][p] = 0.5
        #tmp[p][q] = 0.35
        log("For <", x,">, the best match is <", j,"> and second best match is <", q,">", l=2)
    log("Searching for best matches per individual subject in supplied array complete, returning result", l=1)
    return tmp

# returns the matching id for the same patient on the same scanner
def get_same_scanner_match(cbu_id, map_same):
    """
    Returns the matching connectome ID
    
    Parameters
    ----------
    cbu_id : int
        ID to be matched
    map_same : list
        Correspondence map
    
    Returns
    -------
    int
        Matching ID
    """
    
    for scanner_sublist in map_same:
        for patient, x in scanner_sublist.items():
            if cbu_id == x[0]:
                log("Same scanner match: <", cbu_id,"> corresponds to <", x[1],">", l=2)
                return x[1]
            if cbu_id == x[1]:
                log("Same scanner match: <", cbu_id,"> corresponds to <", x[0],">", l=2)
                return x[0]
    return 0

# converts data of the first scanner to second scanner type data and returns the result, structure msc
def convert_cross_scanner(connectome_list_scanner_separated, scanner_specific_maps):
    """
    Converts data of the first scanner to data of the second scanner, msc structure
    
    Parameters
    ----------
    connectome_list_scanner_separated : list
        Connectome list of msc structure
    scanner_specific_maps : list
        Scanner specific maps as generated by :func:`~crram.generate_reduced_connectomes`
    
    Returns
    -------
    list
        Converted data, msc structure
    """
    cross_scanner_converted_data = {}
    for modality, sublist in connectome_list_scanner_separated.items():
        cross_scanner_converted_data[modality] = {}
        # convert scanner
        scanner_convertable = list(sublist.keys())[0]
        scanner_other = list(sublist.keys())[1]
        for scanner, scanner_sublist in sublist.items():
            cross_scanner_converted_data[modality][scanner] = {}
            for cbu_id, connectome in scanner_sublist.items():
                if scanner_convertable == scanner:
                    con = np.copy(connectome)
                    con = con - scanner_specific_maps[modality][scanner] + scanner_specific_maps[modality][scanner_other]
                    cross_scanner_converted_data[modality][scanner][cbu_id] = con
                else:
                    cross_scanner_converted_data[modality][scanner][cbu_id] = np.copy(connectome)
    return cross_scanner_converted_data


# merges test series with the same patient id per scanner, structure msc
def create_same_subject_merge(connectome_list_scanner_separated, map_same):
    """
    Merges connectoms with the same patient ID, msc structure.
    
    Parameters
    ----------
    connectome_list_scanner_separated : list
        Connectome list, msc structure
    map_same : list
        Correspondence map
    
    Returns
    -------
    list
        List of connectomes with same patient IDs merged, msc type
    """
    same_subject_merge = {}
    for modality, sublist in connectome_list_scanner_separated.items():
        same_subject_merge[modality] = {}
        for scanner, scanner_sublist in sublist.items():
            same_subject_merge[modality][scanner] = {}
            for subject_id, cbu_ids in map_same[scanner].items():
                if cbu_ids[0] in scanner_sublist.keys():
                    con = np.zeros((len(scanner_sublist[cbu_ids[0]]), len(scanner_sublist[cbu_ids[0]])))
                    for i in range(len(cbu_ids)):
                        con = con + scanner_sublist[cbu_ids[i]]
                    con = con / len(cbu_ids)
                    same_subject_merge[modality][scanner][subject_id] = con
                
    return same_subject_merge

# merges test series with the same patient id per scanner, structure msc, ignores connectomes in ignore list
def create_same_subject_merge_ignore(connectome_list_scanner_separated, map_same, ignore_list):
    """
    Merges connectoms with the same patient ID, msc structure.
    
    Parameters
    ----------
    connectome_list_scanner_separated : list
        Connectome list, msc structure
    map_same : list
        Correspondence map
    ignore_list : array
        List of cbu_ids to be ignored
    
    Returns
    -------
    list
        List of connectomes with same patient IDs merged, msc type
    """
    same_subject_merge = {}
    for modality, sublist in connectome_list_scanner_separated.items():
        same_subject_merge[modality] = {}
        for scanner, scanner_sublist in sublist.items():
            same_subject_merge[modality][scanner] = {}
            for subject_id, cbu_ids in map_same[scanner].items():
                if cbu_ids[0] in scanner_sublist.keys():
                    con = np.zeros((len(scanner_sublist[cbu_ids[0]]), len(scanner_sublist[cbu_ids[0]])))
                    cnt = 0
                    for i in range(len(cbu_ids)):
                        if cbu_ids[i] in ignore_list:
                            log("ignore", cbu_ids[i])
                            cnt = cnt + 1
                        else:
                            con = con + scanner_sublist[cbu_ids[i]]
                    con = con / (len(cbu_ids) - cnt)
                    same_subject_merge[modality][scanner][subject_id] = con
                
    return same_subject_merge


def change_to_cluster_resolution(connectome, size):
    """
    Generates new connectome with each entry corresponding to the average of each size*size entries in the original connectome.
    
    Parameters
    ----------
    connectome : 2D array
        Connectome as a 2D array
    size : int
        Size of the cluster that will be averaged
    
    Returns
    -------
    new_connectome
        New connectome as a 2D array
    """
    length = int(len(connectome) / size)
    new_connectome = np.zeros((length, length))
    for x in range(length):
        for y in range(length):
            value = 0
            for i in range(size):
                for j in range(size):
                    value = value + connectome[size * y + j][size * x + i]
            value = value / (size * size)
            new_connectome[y][x] = value
    return new_connectome

def find_connectome_in_substructure(connectome_list, cbu_id):
    """
    Finds connectome with supplied ID in any <=3 - level structure/sub-structure.
    
    Parameters
    ----------
    connectome_list : list
        List containing connectomes in any of up to three layers
    cbu_id : int
        ID of the connectome
    
    Returns
    -------
    2D array
        Connectome as a 2D array, empty if not found
    """
    if cbu_id in list(connectome_list.keys()):
        return connectome_list[cbu_id]
    else:
        for sub_key, sub_list in connectome_list.items():
            if cbu_id in list(sub_list.keys()):
                return sub_list[cbu_id]
            else:
                for sub_sub_key, sub_sub_list in connectome_list.items():
                    if cbu_id in list(sub_sub_list.keys()):
                        return sub_sub_list[cbu_id]
                    else:
                        return []


def reduce_connectome_to_triangular_form(connectome):
    """
    Generates a copy of the supplied connectome reduced to triangular form.
    
    Parameters
    ----------
    connectome : 2D array
        Connectome as a 2D array
    
    Returns
    -------
    2D array
        Reduced (triangular form) connectome as a 2D array
    """
    con = np.zeros((len(connectome), len(connectome)))
    for x in range(len(connectome)):
        for y in range(len(connectome)):
            if x <= y:
                con[y][x] = connectome[y][x]
            else:
                con[y][x] = 0
    return con

def restore_connectome_from_triangularform(connectome):
    """
    Generates a copy of the supplied connectome restored from the triangular form to the standard symmetrical form.
    
    Parameters
    ----------
    connectome : 2D array
        Connectome as a 2D array
    
    Returns
    -------
    2D array
        Restored (symmetrical form) connectome as a 2D array
    """
    con = np.zeros((len(connectome), len(connectome)))
    for x in range(len(connectome)):
        for y in range(len(connectome)):
            if x == y:
                con[y][x] = connectome[y][x]
            else:
                con[y][x] = connectome[y][x] + connectome[x][y]
    return con

# gravitation-based connectome alignment procedure GCAP - aligns connectome with target
def gcap_generate(connectome, target):
    """
    Gravitational-based Connectome Alignement Procedure (GCAP) - aligns supplied connectome with target connectome based on their binary maps.
    
    Parameters
    ----------
    connectome : 2D array
        Connectome to be aligned as a 2D array
    target : 2D array
        Reference connectome as a 2D array
    
    Returns
    -------
    2D array
        Aligned connectome as a 2D array
    """
    #TODO: optimise, esp wrt triangular symmetry 
    log("Initial comparison:", compare(connectome, target), l=1)
    # generate binary map
    con_binary = generate_normalised_connectome(connectome)
    con_binary_target = generate_normalised_connectome(target)
    
    # initial size / number of clusters
    size = int(len(connectome) / 3)
    cluster_max = 2
#    size = 10
#    cluster_max = 2
    flag = True
    
    con_binary_temp = np.copy(con_binary)
    con_temp = np.copy(connectome)
    
    # iterate over cluster sizes
    
    while(flag):
        log("Start iteration with <", cluster_max,"> clusters of size <", size,">", l=2)
        
        # find gravitational-like centers
        centers = gcap_find_cluster_centers(con_binary_temp, cluster_max, size)
        log("Found centers in original structure at:", centers, l=2)
        centers_target = gcap_find_cluster_centers(con_binary_target, cluster_max, size)
        log("Found centers in target structure at:", centers_target, l=2)
        
        # calculate changes required
        changes = []
        log("Matching <", len(centers),"> centers", l=2)
        for i in range(len(centers)):
            log("Matching center <", i,">", l=3)
            # see if matching cluster is in range
            for j in range(len(centers_target)):
                if abs(centers[i][0] - centers_target[j][0]) <= size / 2 and abs(centers[i][1] - centers_target[j][1]) <= size / 2:
                    changes.append((centers[i], centers_target[j]))
                    log("Match found: <", j,">", l=3)
                    continue
                log("No match found...", l=3)
        log("Required changes:", changes, l=2)   
         
        # apply changes to both maps
        (con_temp, con_binary_temp) = gcap_apply_changes(con_temp, con_binary_temp, changes, size)
        
        # determine new cluster size and number
        if(size <= 24):
            log("Final iteration completed, terminating cluster iterations", l=2)
            flag = False
        else:
            cluster_max = cluster_max * 2
            size = int(size / 2)
            log("Iteration completed, change cluster size and number", l=2)

    log("Final comparison:", compare(con_temp, target), l=1)
    return con_temp

def gcap_iteration_array(connectome, target, steps):
    similarity_array = []
    similarity2_array = []
    similarity_array.append(similarity(connectome, target))
    similarity2_array.append(similarity2(connectome, target))
    
    # generate binary map
    con_binary = reduce_connectome_to_triangular_form(generate_normalised_connectome(connectome))
    con_binary_target = reduce_connectome_to_triangular_form(generate_normalised_connectome(target))
    
    # initial size / number of clusters
    size = int(len(connectome) / 3)
    cluster_max = 2
    
    con_binary_temp = np.copy(con_binary)
    con_temp = np.copy(connectome)
    
    # iterate over cluster sizes
    
    for i in range(steps):
        log("Start iteration with <", cluster_max,"> clusters of size <", size,">", l=2)
        
        # find gravitational-like centers
        centers = gcap_find_cluster_centers(con_binary_temp, cluster_max, size)
        log("Found centers in original structure at:", centers, l=2)
        centers_target = gcap_find_cluster_centers(con_binary_target, cluster_max, size)
        log("Found centers in target structure at:", centers_target, l=2)
        
        # calculate changes required
        changes = []
        log("Matching <", len(centers),"> centers", l=2)
        for i in range(len(centers)):
            log("Matching center <", i,">", l=3)
            # see if matching cluster is in range
            for j in range(len(centers_target)):
                if abs(centers[i][0] - centers_target[j][0]) <= size / 2 and abs(centers[i][1] - centers_target[j][1]) <= size / 2:
                    changes.append((centers[i], centers_target[j]))
                    log("Match found: <", j,">", l=3)
                    continue
                log("No match found...", l=3)
        log("Required changes:", changes, l=2)   
         
        # apply changes to both maps
        (con_temp, con_binary_temp) = gcap_apply_changes(con_temp, con_binary_temp, changes, size)
        
        # determine new cluster size and number
        cluster_max = cluster_max * 2
        size = int(size / 2)
        log("Iteration completed, change cluster size and number", l=2)
        similarity_array.append(similarity(restore_connectome_from_triangularform(con_temp), restore_connectome_from_triangularform(target)))
        similarity2_array.append(similarity2(restore_connectome_from_triangularform(con_temp), restore_connectome_from_triangularform(target)))
        
    return similarity_array, similarity2_array


def gcap_apply_changes(connectome, connectome_binary, changes, size):
    con_temp = np.copy(connectome)
    con_temp_b = np.copy(connectome_binary)
    log("Applying changes:", changes, l=2)
    for i in range(len(changes)):
        log("Removing cluster <", i, "> entries", l=3)
        y = changes[i][0][0]
        x = changes[i][0][1]
        for xs in np.arange(x - int(size / 2), (x + int(size / 2))):
                for ys in np.arange(y - int(size / 2), (y + int(size / 2))):
                    con_temp[y][x] = 0
                    con_temp_b[y][x] = 0

    for i in range(len(changes)):
        log("Adding cluster <", i, "> entries", l=3)
        y = changes[i][0][0]
        x = changes[i][0][1]
        dy = changes[i][1][0] - changes[i][0][0]
        dx = changes[i][1][1] - changes[i][0][1]
        log("Moving cluster <", i, "> by (", dx, "/", dy,")", l=3)
        for xs in np.arange(x - int(size / 2), (x + int(size / 2))):
                for ys in np.arange(y - int(size / 2), (y + int(size / 2))):
                    con_temp[y + dy][x + dx] = connectome[y][x]
                    con_temp_b[y + dy][x + dx] = connectome_binary[y][x]
    
    log("Applying changes complete", l=2)
    connectome_binary = con_temp_b
    connectome = con_temp
    return (connectome, connectome_binary)

def gcap_find_cluster_centers(binary_map, number, size):
    log("Searching for <", number,"> clusters of size <", size,">", l=3)
    cluster_centers = []
    # generate weighted map
    weight_map = np.zeros((len(binary_map), len(binary_map)))
    log("Generating weight map of size <", len(weight_map),">", l=3)
    for x in range(len(binary_map)):
        sys.stdout.write("\r      | Current x-iteration: <" + str(x) + "/" + str(len(weight_map)) + ">")
        sys.stdout.flush()
        for y in range(len(binary_map)):
            value = binary_map[y][x]
            for xs in np.arange(x - int(size / 2), (x + int(size / 2))):
                for ys in np.arange(y - int(size / 2), (y + int(size / 2))):
                   if x == xs and y == ys:
                       continue
                   else:
                       value = value + get_connectome_entry(binary_map, xs, ys) / ((x - xs) * (x - xs) + (y - ys) * (y - ys))
            weight_map[y][x] = value
    # find maxima
    log("\n")
    log("Using weight map to find cluster centers", l=3)
    for i in range(number):
        log("Searching for cluster <", i,">", l=4)
        maximum_pos = np.unravel_index(np.argmax(weight_map, axis=None), weight_map.shape)
        cluster_centers.append(maximum_pos)
        gcap_delete_cluster(weight_map, maximum_pos[1], maximum_pos[0], size)
    return cluster_centers

def gcap_delete_cluster(weight_map, x, y, size):
    for xs in np.arange(x - int(size / 2), (x + int(size / 2))):
        for ys in np.arange(y - int(size / 2), (y + int(size / 2))):
            set_connectome_entry(weight_map, xs, ys, 0)
    
def gcap_distance(x, y, xs, ys):
    return math.sqrt((x - xs) * (x - xs) + (y - ys) * (y - ys))

def gcap_compare(a, b):
    """
    Compares two connectomes based on the GCAP algorithm.
    
    Parameters
    ----------
    a : 2D array
        First connectome as a 2D matrix
    b : 2D array
        Second connectome as a 2D matrix
    
    Returns
    -------
    float
        Sum of differences as a degree of similarity
    """
    return compare(gcap_generate(a, b), b)

def generate_normalised_connectome(connectome):
    """
    Generates a binary/normalised version of the connectome, sets all negative edges to -1 and all positive edges to +1.
    
    Parameters
    ----------
    connectome : 2D array
        Connectome to be normalised
    
    Returns
    -------
    2D array
        Normalised connectome
    """
    con = np.copy(connectome)
    con[con > .0] = 1.0
    con[con < .0] = -1.0
    return con

def get_connectome_entry(connectome, x, y):
    """
    Gets entry in connectome, 0 for out-of-bounds
    
    Parameters
    ----------
    connectome : 2D array
        Connectome as a 2D array
    x : int
        x-position
    y : int
        y-position
    
    Returns
    -------
    float
        Entry at specified position or 0 for out-of-bounds
    """
    if x < 0 or y < 0 or x >= len(connectome) or y >= len(connectome):
        return 0
    else:
        return connectome[y][x]
    
def set_connectome_entry(connectome, x, y, v):
    """
    Sets entry in connectome, ignores for out-of-bounds
    
    Parameters
    ----------
    connectome : 2D array
        Connectome as a 2D array
    x : int
        x-position
    y : int
        y-position
    v : float
        New value of entry at specified position
    """
    if x < 0 or y < 0 or x >= len(connectome) or y >= len(connectome):
        return
    else:
        connectome[y][x] = v

def similarity(a, b):
    """
    Compares two connectomes based on the ratio of differences to sum of absolute edge weights.
    
    Parameters
    ----------
    a : 2D array
        First connectome as a 2D matrix
    b : 2D array
        Second connectome as a 2D matrix
    
    Returns
    -------
    float
        Coefficient of similarity, 0 = identical, 1 = exact opposite
    """
    s = np.sum(abs(a - b))
    x = np.sum(abs(a))
    y = np.sum(abs(b))
    z = x + y
    if z == 0:
        return 0
    c = s / z
    return c

def similarity2(a, b):
    """
    Compares two connectomes based on the ratio of square differences to sum of absolute edge weights.
    
    Parameters
    ----------
    a : 2D array
        First connectome as a 2D matrix
    b : 2D array
        Second connectome as a 2D matrix
    
    Returns
    -------
    float
        Coefficient of similarity, 0 = identical, 1 = exact opposite
    """
    s = np.sum((a - b) * (a - b))
    x = np.sum(a * a)
    y = np.sum(b * b)
    c = s / (x + y)
    return c

def compare(a, b):
    """
    Compares two connectomes based on the sum of absolute differences of entries.
    
    Parameters
    ----------
    a : 2D array
        First connectome as a 2D matrix
    b : 2D array
        Second connectome as a 2D matrix
    
    Returns
    -------
    float
        Sum of differences as a degree of similarity
    """
    s = np.sum(abs(a - b))
    return s

def compare2(a, b):
    """
    Compares two connectomes based on the sum of square of differences of entries.
    
    Parameters
    ----------
    a : 2D array
        First connectome as a 2D matrix
    b : 2D array
        Second connectome as a 2D matrix
    
    Returns
    -------
    float
        Sum of square of differences as a degree of similarity
    """
    s = np.sum(abs((a - b) * (a - b)))
    return s

def remove_all_but_cluster(connectome, x, y, cluster_size):
    result = np.zeros((len(connectome), len(connectome))) 
    for i in range(x - cluster_size + 1, x + cluster_size):
        for j in range(y - cluster_size + 1, y + cluster_size):
            if i >= 0 and j >= 0 and i < len(connectome) and j < len(connectome):
                result[j][i] = connectome[j][i]
    return result

def get_contrast_analysis_single(mat):
    match = []
    other = []
    for x in range(len(mat)):
        for y in range(x):
            if x % 2 != 0 and x == y + 1:
                match.append(mat[y][x])
            else:
                other.append(mat[y][x])
    std_factor = 1.96
    contrast = (np.mean(other) - std_factor * np.std(other) - std_factor * np.std(match) - np.mean(match)) / np.mean(other)
    contrast_error = (np.mean(other) - np.std(other) - np.std(match) - np.mean(match)) / np.mean(other)
    contrast_n = (np.mean(other) - np.mean(match)) / np.mean(other)
    
    if np.mean(other) == 0:
        contrast = 0.0
        contrast_error = 0.0
        contrast_n = 0.0
    return  (contrast_n, contrast_error, contrast)

def get_contrast_analysis_cross_scanner(mat):
    match = []
    other = []
    for x in range(len(mat)):
        for y in range(x + 1):
            if x == y:
                match.append(mat[y][x])
            else:
                other.append(mat[y][x])
                
        
    std_factor = 1.96
    contrast = (np.mean(other) - std_factor * np.std(other) - std_factor * np.std(match) - np.mean(match)) / np.mean(other)
    contrast_n = (np.mean(other) - np.mean(match)) / np.mean(other)
    contrast_error = (np.mean(other) - np.std(other) - np.std(match) - np.mean(match)) / np.mean(other)
    if np.mean(other) == 0:
        contrast = 0.0
        contrast_error = 0.0
        contrast_n = 0.0
    return (contrast_n, contrast_error, contrast)
    



# =====================================================================================================================
# =====================================================================================================================

# deprecated functions - can probably just delete them at some point, rewrote most of them to work generally


def plot_connectome(con):
    fig = plt.figure(figsize=(18, 10))
        
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


    
def save_norm_connectome(con, path, s):
    c = generate_normalised_connectome(con)
    fig = plt.figure(figsize=(18, 10))
        
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(c)
    ax.set_aspect('equal')
        
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()
    fig.savefig(path + "data/img/"+s+".png", dpi=100)



def plot_norm(con):
    plot_connectome(generate_normalised_connectome(con))
    
    



def compare_norm(a, b):
    return compare(generate_normalised_connectome(a), generate_normalised_connectome(b))




def translate(a, x, y, dx, dy, size):
    b = np.copy(a)
    # translate
    for i in range(x - dx, x + size - dx):
        for j in range(y - dy, y + size - dy):
            b[i][j] = a[i + dx][j + dy]
    #cleanup
    xs = x
    ys = y
    xe = x+dx
    ye = y+dy
    if(dx <= 0):
        xs = x + size + dx
        xe = x + size
    if(dy <= 0):
        ys = y + size + dy
        ye = y + size
    for i in range(xs, xe):
        for j in range(ys, ye):
            b[i][j] = 0
    
    return b

def align(a, b):
 
    # alter a to align with b
    c = generate_normalised_connectome(np.copy(a))
    d = generate_normalised_connectome(b)
    
    print(compare(c, d))
    
    max_dist = 5
    step = 20
  
    # determine clusters
    x = 0
    y = 0
    while True:
        while True:

            i_m = 0
            j_m = 0
            min_val = compare(c, d)
            for i in range(-max_dist, max_dist):
                for j in range(-max_dist, max_dist):
                    w = compare(d, translate(c, x, y, i, j, step))
                    if(w < min_val):
                        i_m = i
                        j_m = j
            c = translate(c, x, y, i_m, j_m, step)
            
            
        
            x = x + step
            if(x + step >= len(a)):
                x = 0
                break
        print(x, y)
        y = y + step
        if(y + step >= len(a)):
            y = 0
            break
    
    # minimise
    compare(c, d)
    
    
    
    print(compare(c, d))
    return c

def comparec(a, b, size):
    x = 0
    y = 0
    s = 0
    val_a = 0
    val_b = 0
    cnt = 0
    for x in range(len(a)):
        for y in range(len(a)):
            cnt = cnt + 1
            val_a = val_a + a[y][x]
            val_b = val_b + b[y][x]
            if(cnt == size):
                cnt = 0
                s = s + abs(val_a - val_b)
                val_a = 0
                val_b = 0
        cnt = 0
        s = s + abs(val_a - val_b)
        val_a = 0
        val_b = 0
            
            
    return s

def highlightarray(arr):
    tmp = np.zeros((len(arr), len(arr)))
    for x in range(len(arr)):
        min_f = np.amax(arr)
        min_s = np.amax(arr)
        i = 0
        j = 0
        p = 0
        q = 0
        for y in range(len(arr)):
            if arr[y][x] == 0:
                tmp[y][x] = -1
                continue
            if arr[y][x] < min_f:
                min_s = min_f
                p = i
                q = j
                min_f = arr[y][x]
                i = x
                j = y
            elif arr[y][x] < min_s:
                min_s = arr[y][x]
                p = x
                q = y
        tmp[j][i] = 1
        #tmp[i][j] = 0.7
        tmp[q][p] = 0.5
        #tmp[p][q] = 0.35
    plot_connectome(tmp)
    

    
def mean(G):
    count = 0
    _sum = 0
    for key in G:
        count += 1
        _sum += G[key]
    return _sum/count
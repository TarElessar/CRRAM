# -*- coding: utf-8 -*-
"""
@author: Felix Menze
"""

import crram as cr
import sys
import webbrowser
import os
import operator
import numpy as np


# =====================================================================================================================

if(len(sys.argv) == 3):
    working_dir = sys.argv[1]
    data_dir = sys.argv[2]
else:
    print("Please provide valid arguments")
    exit()


# =====================================================================================================================

# main analysis file
analysis_file = os.path.join(working_dir, "analysis.html")
if os.path.exists(analysis_file):
    f = open(analysis_file,'r+')
    f.truncate(0)
    f.close()
else:
    open(analysis_file, 'a').close()
    
statistics_file = os.path.join(working_dir, "statistics.txt")
if os.path.exists(statistics_file):
    f = open(statistics_file,'r+')
    f.truncate(0)
    f.close()
else:
    open(statistics_file, 'a').close()
    
# main src directory
src_dir = os.path.join(working_dir, "src")
if not os.path.exists(src_dir):
    os.makedirs(src_dir)
#else:
    #TODO
    #cr.delete_folder_contents(src_dir)
    
# css style sheet
css = os.path.join(working_dir, "styles.css")
if os.path.exists(css):
    f = open(css,'r+')
    f.truncate(0)
    f.close()
else:
    open(css, 'a').close()
f = open(css,'w')
f.write(cr.generate_css())
f.close()
    
# =====================================================================================================================

flag = False
flag2 = False
flag3 = False
flag4 = False
flag5 = False

#flag = True
#flag2 = True
#flag3 = True
#flag4 = True
#flag5 = True

cr.init()
patient_data_files, path_connectome_main = cr.read_path_structure(data_dir)
map_cor = cr.read_patient_data(patient_data_files)
map_same = cr.create_patient_data_map(map_cor)

# connectome basic
if not 'connectome_list' in locals() or flag:
    cr.format_connectome_data(path_connectome_main)
    connectome_list = cr.read_all_connectome_data(path_connectome_main)
    cr.plot_all(connectome_list, src_dir, 'raw')
    cr.plot_all_binary(connectome_list, src_dir, 'binary')


# single scanner
if not 'scanner_separated_list' in locals() or flag2:
    scanner_separated_list = cr.generate_scanner_separated_list(connectome_list, map_cor)
    
    #note: using this as general ordering probably
    #(comp, ordering) = cr.apply_to_scanner_specific_connectome_pairs(scanner_separated_list, lambda x,y : cr.compare(x, y))
    #cr.apply_to_scanner_specific_entries_metadata_nr(comp, lambda x, m, s : cr.save_comparison_matrix(x, ordering[m][s], src_dir, str(m) + "_" + cr.get_scanner_name(s, patient_data_files) + "_comparemapabsolute"))
    
    #best_match_per_subject = cr.apply_to_scanner_specific_entries(comp, lambda x : cr.find_best_matches_per_subject(x))
    #cr.apply_to_scanner_specific_entries_metadata_nr(best_match_per_subject, lambda x, m, s : cr.save_comparison_matrix(cr.sort_array_by_correspondence(x, ordering[m][s], map_same)[0], cr.sort_array_by_correspondence(x, ordering[m][s], map_same)[1], src_dir, str(m) + "_" + cr.get_scanner_name(s, patient_data_files) + "_comparebestmatchperseries"))
    
    #best_matches_in_array = cr.apply_to_scanner_specific_entries(comp, lambda x : cr.find_best_matches_in_array(x))
    #cr.apply_to_scanner_specific_entries_metadata_nr(best_matches_in_array, lambda x, m, s : cr.save_comparison_matrix(cr.sort_array_by_correspondence(x, ordering[m][s], map_same)[0], cr.sort_array_by_correspondence(x, ordering[m][s], map_same)[1], src_dir, str(m) + "_" + cr.get_scanner_name(s, patient_data_files) + "_comparebestmatchoverall"))

# cross scanner
if not 'cross_scanner_converted_data' in locals() or flag3:
    
    (compcross, orderingy, orderingx) = cr.apply_to_cross_scanner_pairs(scanner_separated_list, lambda x,y : cr.compare(x, y))
    cr.apply_to_entries_metadata_nr(compcross, lambda x, m : cr.save_comparison_matrix_xy(x, orderingx[m], orderingy[m], src_dir, str(m) + "_comparecrossscanner"))
# suffices to compare reduced maps? maybe  
    
if not 'same_scanner_merged_data' in locals() or flag4:
    cr.plot_all_s(scanner_separated_list, src_dir, patient_data_files, 'samescannermerged_s')
    (comp_id_merged, orderingy, orderingx) = cr.apply_to_cross_scanner_pairs(scanner_separated_list, lambda x,y : cr.compare(x, y))
    cr.apply_to_entries_metadata_nr(comp_id_merged, lambda x, m : cr.save_comparison_matrix_xy(x, orderingx[m], orderingy[m], src_dir, str(m) + "_comparesubjectsmergedcrossscanner"))
    
    (comp2_id_merged, orderingy, orderingx) = cr.apply_to_cross_scanner_pairs(scanner_separated_list, lambda x,y : cr.compare2(x, y))
    cr.apply_to_entries_metadata_nr(comp2_id_merged, lambda x, m : cr.save_comparison_matrix_xy(x, orderingx[m], orderingy[m], src_dir, str(m) + "_comparesquaredsubjectsmergedcrossscanner"))
    
    best_cross_scanner_matches = cr.apply_to_all_modality_data(comp_id_merged, lambda x : cr.find_best_matches_in_array_asym(x))
    cr.apply_to_entries_metadata_nr(best_cross_scanner_matches, lambda x, m : cr.save_comparison_matrix_xy(x, orderingx[m], orderingy[m], src_dir, str(m) + "_crossscannerbestmatch"))
    


if not 'same_scanner_merged_data' in locals() or flag5:
    # similarity comparison
    #(comp_similarity, ordering) = cr.apply_to_scanner_specific_connectome_pairs(scanner_separated_list, lambda x,y : cr.similarity(x, y))
    #cr.apply_to_scanner_specific_entries_metadata_nr(comp_similarity, lambda x, m, s : cr.save_comparison_matrix(x, ordering[m][s], src_dir, str(m) + "_" + cr.get_scanner_name(s, patient_data_files) + "_comparemapsimilarity"))
    #(comp_similarity_reduced, ordering) = cr.apply_to_scanner_specific_connectome_pairs(scanner_separated_list, lambda x,y : cr.similarity(x, y))
    #cr.apply_to_scanner_specific_entries_metadata_nr(comp_similarity_reduced, lambda x, m, s : cr.save_comparison_matrix(x, ordering[m][s], src_dir, str(m) + "_" + cr.get_scanner_name(s, patient_data_files) + "_comparemapsimilarityreduced"))
    #best_matches_in_array = cr.apply_to_scanner_specific_entries(comp_similarity, lambda x : cr.find_best_matches_in_array(x))
    #cr.apply_to_scanner_specific_entries_metadata_nr(best_matches_in_array, lambda x, m, s : cr.save_comparison_matrix(cr.sort_array_by_correspondence(x, ordering[m][s], map_same)[0], cr.sort_array_by_correspondence(x, ordering[m][s], map_same)[1], src_dir, str(m) + "_" + cr.get_scanner_name(s, patient_data_files) + "_comparebestmatchoverallsimilarity"))
    #best_matches_in_array = cr.apply_to_scanner_specific_entries(comp_similarity_reduced, lambda x : cr.find_best_matches_in_array(x))
    #cr.apply_to_scanner_specific_entries_metadata_nr(best_matches_in_array, lambda x, m, s : cr.save_comparison_matrix(cr.sort_array_by_correspondence(x, ordering[m][s], map_same)[0], cr.sort_array_by_correspondence(x, ordering[m][s], map_same)[1], src_dir, str(m) + "_" + cr.get_scanner_name(s, patient_data_files) + "_comparebestmatchoverallsimilarityreduced"))
    
    (comp_id_merged_similarity, orderingy, orderingx) = cr.apply_to_cross_scanner_pairs(scanner_separated_list, lambda x,y : cr.similarity(x, y))
    cr.apply_to_entries_metadata_nr(comp_id_merged_similarity, lambda x, m : cr.save_comparison_matrix_xy(x, orderingx[m], orderingy[m], src_dir, str(m) + "_comparesubjectsmergedcrossscannersimilarity"))
    
    best_cross_scanner_matches = cr.apply_to_all_modality_data(comp_id_merged_similarity, lambda x : cr.find_best_matches_in_array_asym(x))
    cr.apply_to_entries_metadata_nr(best_cross_scanner_matches, lambda x, m : cr.save_comparison_matrix_xy(x, orderingx[m], orderingy[m], src_dir, str(m) + "_crossscannerbestmatchsimilarity"))
    

# finish                
cr.write_meta_data(src_dir, patient_data_files, path_connectome_main, map_cor, map_same)


# analysis data, calculate from: comp_id_merged_similarity comp_similarity, getting Weber contrast

 





f = open(statistics_file,'w')
for xx in range(4):
    for yy in range(4):
        if xx == yy:
            continue
        (comp_id_merged_similarity, orderingy, orderingx) = cr.apply_to_cross_scanner_pairs_specify_pair(scanner_separated_list, xx, yy, lambda x,y : cr.similarity(x, y))
        cr.apply_to_entries_metadata_nr(comp_id_merged_similarity, lambda x, m : cr.save_comparison_matrix_xy(x, orderingx[m], orderingy[m], src_dir, str(m) + "_comparesubjectsmergedcrossscannersimilarity"))
    
        best_cross_scanner_matches = cr.apply_to_all_modality_data(comp_id_merged_similarity, lambda x : cr.find_best_matches_in_array_asym(x))
        cr.apply_to_entries_metadata_nr(best_cross_scanner_matches, lambda x, m : cr.save_comparison_matrix_xy(x, orderingx[m], orderingy[m], src_dir, str(m) + "_" + str(xx) + str(yy) + "_crossscannerbestmatchsimilarity"))
        
        for modality, mat in comp_id_merged_similarity.items():
            (contrast_n, contrast_error, contrast) = cr.get_contrast_analysis_cross_scanner(mat)
            f.write(str(xx) + ", " + str(yy) + ", " + str(contrast_n) + ", " + str(contrast_error) + ", " + str(contrast) + "\n")

f.close()

# =====================================================================================================================


f = open(analysis_file,'w')

html_bh = ("", cr.html_header())

end = cr.html_end()  
html_bh = tuple(map(operator.add, html_bh, cr.html_patient_data_table(map_same, patient_data_files, "Patient data")))
html_bh = tuple(map(operator.add, html_bh, cr.html_image_series(src_dir, "Connectomes")))
html_bh = tuple(map(operator.add, html_bh, cr.html_image_series(src_dir, "Binary Connectomes", mod='binary')))
html_bh = tuple(map(operator.add, html_bh, cr.html_image_series(src_dir, "Reduced Connectomes", mod='raw_s')))
html_bh = tuple(map(operator.add, html_bh, cr.html_image_series(src_dir, "Converted (same scanner like) Connectomes", mod='converted_s')))
html_bh = tuple(map(operator.add, html_bh, cr.html_image_series(src_dir, "Merged connectomes per scanner", mod='samescannermerged_s')))
#html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "Simple comparison map, absolute values, non-reduced maps", mod='comparemapabsolute')))
#html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "Simple comparison map, similarity coeff, non-reduced", mod='comparemapsimilarity')))
#html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "Simple comparison map, similarity coeff, reduced", mod='comparemapsimilarityreduced')))

#html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "Using simple comparison map, best match per individual series, adjacent ids same subject", mod='comparebestmatchperseries')))
#html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "Using simple comparison map, greedy algorithm for best overall matches, adjacent ids same subject", mod='comparebestmatchoverall')))

#html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "Using simple comparison map, greedy, adjacent ids same subject, similarity coeff, non-reduced", mod='comparebestmatchoverallsimilarity')))
#html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "Using simple comparison map, greedy, adjacent ids same subject, similarity coeff, reduced", mod='comparebestmatchoverallsimilarityreduced')))

#html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "dmri optimisation, hopefully", mod='_comparebestmatchoveralldmri')))

html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "cross scanner comparison, simple comparison map", mod='comparecrossscanner')))
html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "cross scanner comparison, simple comparison map, same subjects per scanner merged", mod='_comparesubjectsmergedcrossscanner')))
html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "cross scanner comparison, similarity coeff, same subjects per scanner merged", mod='_comparesubjectsmergedcrossscannersimilarity')))
html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "cross scanner comparison, difference squared  comparison map, same subjects per scanner merged", mod='_comparesquaredsubjectsmergedcrossscanner')))
#html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "cross scanner comparison, gcap algorithm", mod='_comparegcap')))






html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "cross scanner comparison, absolute differences, best match", mod='_crossscannerbestmatch')))
html_bh = tuple(map(operator.add, html_bh, cr.html_modality_scanner_series(src_dir, "cross scanner comparison, similarity coeff, best match", mod='_crossscannerbestmatchsimilarity')))


f.write(html_bh[1] + html_bh[0] + end)
f.close()

webbrowser.open_new_tab(analysis_file)
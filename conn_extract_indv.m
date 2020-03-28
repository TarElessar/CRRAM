wdir = "C:\Projects\MRI\CamCAN\data\conn\SBC_01\firstlevel\";
tdir = "C:\Projects\MRI\CamCAN\data\connectomes\fmri\";

subjects = [140905 140910 140913 140928 140931 140953 140962 140979 140982 140984 150056 150057 150060 150062 150074 150080 150082 150124 150239 150303];
subject_list = sort(subjects);

for n = 1:20
 n_strPadded = sprintf( '%03d', n ) ;
 file_name = wdir + "resultsROI_Subject" + n_strPadded + "_Condition001.mat" ;
 matObj = matfile(file_name) ;
 zvalues = matObj.Z ;
 zvalues_cut = zvalues(:,1:end-1);
 zvalues_cut(isnan(zvalues_cut)) = 0;
 
 output_file = "connectome_CBU" + int2str(subject_list(n)) + ".csv";
 output_path = tdir + output_file;
 csvwrite(output_path, zvalues_cut);
end

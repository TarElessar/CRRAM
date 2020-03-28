wdir = "C:\Projects\MRI\original_combat\data\conn\SBC_01\firstlevel\";
xdir = "C:\Projects\MRI\original_combat\data\misc\";
tdir = "C:\Projects\MRI\original_combat\data\connectomes\fmri\";
ddir = "C:\Projects\MRI\original_combat\data\connectomes\dmri\";
mdir = "C:\Projects\MRI\original_combat\data\misc\merged\";

%subjects = [140905 140910 140913 140928 140931 140953 140962 140979 140982 140984 150056 150057 150060 150062 150074 150080 150082 150124 150239 150303];
subjects = [140950 140954 140965 140966 140968 140974 140976 140977 140981 140988 140997 140998 140999 141000 141004 141005 141008 141009 141012 150001 150002 150004 150007 150008];
subject_list = sort(subjects);

content = splitlines(fileread(xdir + "hcpmmp1_ordered.txt")) ;
content_cut = content(4:end,:) ;
content_padded = arrayfun(@(x) strcat(" ", x), content_cut) ;
content_split = split(content_padded) ;
LUT = content_split(:, 2:end) ;
dim = length(LUT) ;


for n = 1:length(subjects)
disp(int2str(subject_list(n)))
n_strPadded = sprintf( '%03d', n ) ;
file_name = wdir + "resultsROI_Subject" + n_strPadded + "_Condition001.mat" ;
matObj = matfile(file_name) ;
zvalues = matObj.Z ;
names1 = matObj.names ;
names2 = matObj.names2 ;

connectome = zeros(dim, dim) ;

disp("| reading connectome...")
for idx1 = 1:length(names1)
    element1 = erase(names1(idx1), "atlas_hcp.") ;
    for idx2 = 1:length(names2)
        element2 = erase(names2(idx2), "atlas_hcp.") ;
        entry = zvalues(idx1, idx2) ;
        [val1, idx] = find(LUT==element1) ;
        [val2, idx] = find(LUT==element2) ;
        if val1 ~= 0 & val2 ~= 0
            if val1 == val2
                connectome(val1, val2) = 0 ;
            else
                connectome(val1, val2) = entry ;
                connectome(val2, val1) = entry ;
            end
        end
    end
end
 
output_file = "connectome_CBU" + int2str(subject_list(n)) + ".csv";
output_path = tdir + output_file;
csvwrite(output_path, connectome);

connectome_dmri = readmatrix(ddir + output_file) ;
df = zeros(length(connectome) * length(connectome), 2);
i = 0;
disp("| calculating merged connectome...")
for x = 1:length(connectome)
    for y = 1:length(connectome)
        i = i + 1;
        df(i,1) = connectome_dmri(x,y);
        df(i,2) = connectome(x,y);
    end
end
csvwrite(mdir + output_file, df);
disp("| formatting merged connectome...")
tmp = erase(fileread(mdir + output_file), "0,0\n") ;
fid = fopen(mdir + output_file,'w');
fprintf(fid, tmp);
fclose(fid);
end












disp('start')
working_dir='/imaging/mc04/fm03/camcan_fmri/raw/';
outdir=strcat(working_dir,'preprocessing/');
dir_ana=strcat(working_dir,'anatomical/');
dir_fun=strcat(working_dir,'functional/');
if ~exist(outdir, 'dir')
    disp('creating preprocessing directory')
    mkdir(outdir)
end
files_anatomical=dir(fullfile(dir_ana,'*mprage.nii'));
files_functional=dir(fullfile(dir_fun,'*epi.nii'));

preprocess(strcat(dir_ana, files_anatomical(1).name), strcat(dir_fun, files_functional(1).name), outdir)

function preprocess(anatomical, functional, outdir)
    disp(anatomical)
    disp(functional)
    
end
#!/bin/bash
#p=/imaging/mc04/fm03/data_multischeme/
#for d in $p* ; do
#    subject=${d#"$p"}
#    #echo "$subject"
#    sbatch --output=/imaging/mc04/fm03/JobOut/%j.out connectome_stuff.sh "$subject"
#done

#declare -a subject_list=("100639" "100699" "100726" "100729" "100730" "100731" "100732" "100733" "100737" "100738" "100739" "100740" "100741" "100743" "100759" "100760")
#for d in ${subject_list[@]} ; do
#    for i in {1..5} ; do
#    subject="CBU"${d#"$p"}"00$i"
#    echo "$subject"
#    sbatch --output=/imaging/mc04/fm03/JobOut/%j.out connectome_register.sh "$subject"
#    done
#done



for i in {10..79} ; do
subject="CBU0000$i"
echo "$subject"
sbatch --output=/imaging/mc04/fm03/JobOut/%j.out connectome_register.sh "$subject"
done

# missing subjects from previous batch - do next
#declare -a subject_list=("100639002" "100639003" "100639004" "100639005" "100699001" "100699002" "100699003" "100699004" "100699005" "100726001" "100726002" "100726003" "100743001" "100743004" "100743005")
#for d in ${subject_list[@]} ; do
#    subject="CBU$d"
#    echo "$subject"
#    sbatch --output=/imaging/mc04/fm03/JobOut/%j.out connectome_register.sh "$subject"
#done

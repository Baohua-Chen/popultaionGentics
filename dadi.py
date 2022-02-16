#!/home/bin/python3

import sys
import os
import numpy
import dadi
from datetime import datetime
import Optimize_Functions
import Models_3D
import pickle
from multiprocessing import Process
#===========================================================================
# Import data to create joint-site frequency spectrum
#===========================================================================

#**************
#pop_ids is a list which should match the populations headers of your SNPs file columns
pop_ids=['GX','ND','DQ']
proj = [78,48,28]

vcf = '../../../gt/prune/snp.prune.noxm.vcf.gz'
pop_file = '../../pop.txt'


def loadVCF():
    dd = dadi.Misc.make_data_dict_vcf(vcf, pop_file)
    fs = dadi.Spectrum.from_data_dict(dd, pop_ids=pop_ids, projections = proj, polarized = False)
    with open('sfs.pkl','wb') as f:
        pickle.dump(fs,f)

#loadVCF()
#exit()
fs=pickle.load(open('sfs.pkl','rb'))
#print some useful information about the afs or jsfs
print("\n\n============================================================================")
print("\nData for site frequency spectrum:\n")
print("Projection: {}".format(proj))
print("Sample sizes: {}".format(fs.sample_sizes))
print("Sum of SFS: {}".format(numpy.around(fs.S(), 2)))
print("\n============================================================================\n")

#================================================================================
# Calling external 3D models from the Models_3D.py script
#================================================================================
#create a prefix based on the population names to label the output files
#ex. Pop1_Pop2_Pop3
prefix = "_".join(pop_ids)

#**************
#make sure to define your extrapolation grid size (based on your projections)
pts = [50,60,70]

#**************
#Set the number of rounds here
rounds = 4

#define the lists for optional arguments
#you can change these to alter the settings of the optimization routine
reps = [10,20,30,40]
maxiters = [3,5,10,15]
folds = [3,2,2,1]

#**************
#Indicate whether your frequency spectrum object is folded (True) or unfolded (False)
fs_folded = True


p13=Process(target=Optimize_Functions.Optimize_Routine, args=(fs, pts, prefix, "split_nomig", Models_3D.split_nomig, rounds, 6,), kwargs=dict(fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, T1, T2"))
p13.start()

p14=Process(target=Optimize_Functions.Optimize_Routine, args=(fs, pts, prefix, "split_symmig_all", Models_3D.split_symmig_all, rounds, 10,), kwargs=dict(fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, mA, m1, m2, m3, T1, T2"))
p14.start()

p15=Process(target=Optimize_Functions.Optimize_Routine, args=(fs, pts, prefix, "split_symmig_adjacent", Models_3D.split_symmig_adjacent, rounds, 9,), kwargs=dict(fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, mA, m1, m2, m3, T1, T2"))
p15.start()

p1=Process(target=Optimize_Functions.Optimize_Routine, args=(fs, pts, prefix, "refugia_adj_1", Models_3D.refugia_adj_1, rounds, 9,),kwargs=dict(fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, m1, m2, T1, T2, T3"))
p1.start()

p2=Process(target=Optimize_Functions.Optimize_Routine, args=(fs, pts, prefix, "refugia_adj_2", Models_3D.refugia_adj_2, rounds, 8,),kwargs=dict(fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, m1, m2, T1, T2"))
p2.start()

Optimize_Functions.Optimize_Routine(fs, pts, prefix, "refugia_adj_3", Models_3D.refugia_adj_3, rounds, 10, fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, mA, m1, m2, T1a, T1b, T2")
p3=Process(target=Optimize_Functions.Optimize_Routine, args=(fs, pts, prefix, "refugia_adj_3", Models_3D.refugia_adj_3, rounds, 10,),kwargs=dict(fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, mA, m1, m2, T1a, T1b, T2"))
p3.start()

p4=Process(target=Optimize_Functions.Optimize_Routine, args=(fs, pts, prefix, "ancmig_adj_3", Models_3D.ancmig_adj_3, rounds, 8,), kwargs=dict(fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, mA, T1a, T1b, T2"))
p4=start()

p5=Process(target=Optimize_Functions.Optimize_Routine, args=(fs, pts, prefix, "ancmig_adj_2", Models_3D.ancmig_adj_2, rounds, 7,), kwargs=dict(fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, mA, T1, T2"))
p5.start()

p6=Process(target=Optimize_Functions.Optimize_Routine, args=(fs, pts, prefix, "ancmig_adj_1", Models_3D.ancmig_adj_1, rounds, 10,), kwargs=dict(fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nuA, nu2, nu3, mA, m1, m2, T1, T2, T3"))
p6.start()

p7=Process(target=Optimize_Functions.Optimize_Routine,args=(fs, pts, prefix, "sim_split_no_mig", Models_3D.sim_split_no_mig, rounds, 4,),kwargs=dict(reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, nu3, T1"))
p7.start()

p8=Process(target=Optimize_Functions.Optimize_Routine,args=(fs, pts, prefix, "sim_split_no_mig_size", Models_3D.sim_split_no_mig_size, rounds, 8,),kwargs=dict(fs_folded=fs_folded,reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu3a, nu1b, nu2b, nu3b, T1, T2"))
p8.start()

p9=Process(target=Optimize_Functions.Optimize_Routine,args=(fs, pts, prefix, "sim_split_sym_mig_all", Models_3D.sim_split_sym_mig_all, rounds, 7,),kwargs=dict(fs_folded=fs_folded,reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2, nu3, m1, m2, m3, T1"))
p9.start()

p10=Process(target=Optimize_Functions.Optimize_Routine,args=(fs, pts, prefix, "sim_split_sym_mig_adjacent", Models_3D.sim_split_sym_mig_adjacent, rounds, 6,),kwargs=dict(fs_folded=fs_folded,reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, nu3, m1, m2, T1"))
p10.start()

p11=Process(target=Optimize_Functions.Optimize_Routine,args=(fs, pts, prefix, "sim_split_refugia_sym_mig_all", Models_3D.sim_split_refugia_sym_mig_all, rounds, 8,),kwargs=dict(fs_folded=fs_folded,reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, nu3, m1, m2, m3, T1, T2"))
p11.start()

p12=Process(target=Optimize_Functions.Optimize_Routine,args=(fs, pts, prefix,"sim_split_refugia_sym_mig_adjacent", Models_3D.sim_split_refugia_sym_mig_adjacent, rounds, 7,),kwargs=dict(fs_folded=fs_folded,reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, nu3, m1, m2, T1, T2"))
p12.start()

Optimize_Functions.Optimize_Routine(fs, pts, prefix, "ancmig_2_size", Models_3D.ancmig_2_size, rounds, 11, fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nuA, nu2a, nu3a, nu1b, nu2b, nu3b, mA, T1, T2, T3")

Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sim_split_refugia_sym_mig_adjacent_size", Models_3D.sim_split_refugia_sym_mig_adjacent_size, rounds, 11, fs_folded=fs_folded, reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu3a, nu1b, nu2b, nu3b, m1, m2, T1, T2, T3")

p1.join()
p2.join()
p3.join()
p4.join()
p5.join()
p6.join()
p7.join()
p8.join()
p9.join()
p10.join()
p11.join()
p12.join()
p13.join()
p14.join()
p15.join()

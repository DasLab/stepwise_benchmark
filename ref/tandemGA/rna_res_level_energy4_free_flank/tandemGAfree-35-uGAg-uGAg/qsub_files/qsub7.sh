#!/bin/bash
#PBS -N _biox3_home_geniesse_src_stepwise_benchmark_new_tandemGA_rna_res_level_energy4_free_flank_tandemGAfree-35-uGAg-uGAg_SWM_7
#PBS -o /dev/null
#PBS -e /dev/null
#PBS -m n
#PBS -M nobody@stanford.edu
#PBS -l walltime=48:00:00

cd /biox3/home/geniesse/src/stepwise_benchmark/new/tandemGA/rna_res_level_energy4_free_flank/tandemGAfree-35-uGAg-uGAg

/home/geniesse/src/rosetta//main/source/bin/stepwise -s tandemGAfree-35-uGAg-uGAg_HELIX1.pdb tandemGAfree-35-uGAg-uGAg_HELIX2.pdb -native tandemGAfree-35-uGAg-uGAg_1mis_RNA_35-uGAg-uGAg.pdb -terminal_res A:1 A:16 -extra_min_res A:2 A:7 A:10 A:15 -superimpose_over_all -fasta tandemGAfree-35-uGAg-uGAg.fasta -cycles 200 -nstruct 20 -intermolecular_frequency 0.0 -save_times -score:weights stepwise/rna/rna_res_level_energy4.wts -cycles 200  -out:file:silent SWM/7/swm_rebuild.out > 7.out 2> 7.err 

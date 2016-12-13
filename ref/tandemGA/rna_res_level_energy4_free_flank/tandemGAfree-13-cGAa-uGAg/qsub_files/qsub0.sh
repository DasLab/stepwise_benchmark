#!/bin/bash
#PBS -N _biox3_home_geniesse_src_stepwise_benchmark_new_tandemGA_rna_res_level_energy4_free_flank_tandemGAfree-13-cGAa-uGAg_SWM_0
#PBS -o /dev/null
#PBS -e /dev/null
#PBS -m n
#PBS -M nobody@stanford.edu
#PBS -l walltime=48:00:00

cd /biox3/home/geniesse/src/stepwise_benchmark/new/tandemGA/rna_res_level_energy4_free_flank/tandemGAfree-13-cGAa-uGAg

/home/geniesse/src/rosetta//main/source/bin/stepwise -s tandemGAfree-13-cGAa-uGAg_HELIX1.pdb tandemGAfree-13-cGAa-uGAg_HELIX2.pdb -native tandemGAfree-13-cGAa-uGAg_1mis_RNA_13-cGAa-uGAg.pdb -terminal_res A:1 A:16 -extra_min_res A:2 A:7 A:10 A:15 -superimpose_over_all -fasta tandemGAfree-13-cGAa-uGAg.fasta -cycles 200 -nstruct 20 -intermolecular_frequency 0.0 -save_times -score:weights stepwise/rna/rna_res_level_energy4.wts -cycles 200  -out:file:silent SWM/0/swm_rebuild.out > 0.out 2> 0.err 

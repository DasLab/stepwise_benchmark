#!/bin/bash
#PBS -N _biox3_home_geniesse_src_stepwise_benchmark_new_tandemGA_rna_res_level_energy4_2k_cycles_tandemGA-06-aGAg-cGAu_SWM_7
#PBS -o /dev/null
#PBS -e /dev/null
#PBS -m n
#PBS -M nobody@stanford.edu
#PBS -l walltime=72:00:00

cd /biox3/home/geniesse/src/stepwise_benchmark/new/tandemGA/rna_res_level_energy4_2k_cycles/tandemGA-06-aGAg-cGAu

/home/geniesse/src/rosetta//main/source/bin/stepwise -s tandemGA-06-aGAg-cGAu_HELIX1.pdb tandemGA-06-aGAg-cGAu_HELIX2.pdb -native tandemGA-06-aGAg-cGAu_1mis_RNA_06-aGAg-cGAu.pdb -terminal_res A:1 A:16 -extra_min_res A:3 A:6 A:11 A:14 -superimpose_over_all -fasta tandemGA-06-aGAg-cGAu.fasta -nstruct 20 -intermolecular_frequency 0.0 -save_times -score:weights stepwise/rna/rna_res_level_energy4.wts -cycles 2000 -out:file:silent SWM/7/swm_rebuild.out > 7.out 2> 7.err 

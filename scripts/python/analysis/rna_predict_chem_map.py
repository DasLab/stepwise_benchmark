#!/usr/local/bin/python

###############################################################################

import argparse
import numpy as np
import subprocess
from glob import glob
import os
from os.path import basename, dirname, exists, isfile, isdir
import string
from sys import exit
from rdat import *

###############################################################################

parser = argparse.ArgumentParser(description='Predict DMS reactivity from pdb.')
#parser.add_argument('-target_files', nargs='+', help='List of additional target files.', default=['favorites.txt','favorites2.txt'])
parser.add_argument('-targets', nargs='+', help='List of targets.', default=['*'])
parser.add_argument('-silent_file', default='swm_rebuild.out')
parser.add_argument('-ndecoys', default=20)
parser.add_argument('-analysis_dir',default='analysis')
parser.add_argument('-path_to_rosetta_exe',default='')
parser.add_argument('-make_rna_chemical_map', action='store_true')
parser.add_argument('-plot_seqpos_error', action='store_true')
parser.add_argument('-error_seqpos', nargs='*', default=None)
args = parser.parse_args()

###############################################################################

homedir = os.getcwd()
if args.targets == ['*']:
	targets = [dir for dir in glob('*') if isdir(dir)]
else:
	targets = args.targets
silent_file = args.silent_file
ndecoys = int(args.ndecoys)
analysis_dir = args.analysis_dir
path_to_rosetta_exe = args.path_to_rosetta_exe
if len(path_to_rosetta_exe):
	assert(exists(path_to_rosetta_exe))
	path_to_rosetta_exe += '/'

###############################################################################
rdat = RDATFile()
target_mean_seqpos_reactivity = {}
rdat_headers = {}

for target_idx, target in enumerate(targets, start=1):

	### print current target
	print '\n', target

	### go into target directory
	os.chdir(target)
	print os.getcwd()

	### make analysis directory
	while not(exists(analysis_dir)):
		cmdline = ['mkdir','analysis']
		out,err = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		if not(exists(analysis_dir)):
			print 'CMDLINE:', cmdline
			print 'OUT:', out
			print 'ERROR: ', err
	assert(exists(analysis_dir))
	os.chdir(analysis_dir)
	print os.getcwd()

	### cat silent_files
	while not(exists(silent_file)):
		cmdline = ['easy_cat.py','../SWM']
		out,err = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		if not(exists(silent_file)):
			print 'CMDLINE:', cmdline
			print 'OUT:', out
			print 'ERROR:', err
	assert(exists(silent_file))

	### append target name to silent_file name
	target_silent_file = target + '_' + silent_file
	while not(exists(target_silent_file)):
		cmdline = ['cp',silent_file,target_silent_file]
		out,err = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		if not(exists(target_silent_file)):
			print 'CMDLINE:', cmdline
			print 'OUT:', out
			print 'ERROR:', err
	assert(exists(target_silent_file))

	### extract 20 lowest energy decoys
	target_pdbs = [target_silent_file + '.%d.pdb' % idx for idx in xrange(1,ndecoys+1)]
	assert(len(target_pdbs) == ndecoys)
	while not (sum([exists(f) for f in target_pdbs]) == len(target_pdbs)):
		cmdline = ['extract_lowscore_decoys.py', target_silent_file,str(ndecoys)]
		out,err = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		if not (sum([exists(f) for f in target_pdbs]) == len(target_pdbs)):
			print 'CMDLINE:', cmdline
			print 'OUT:', out
			print 'ERROR:', err
	assert(sum([exists(f) for f in target_pdbs]) == len(target_pdbs))
	print silent_file
	print target_silent_file
	print string.join(target_pdbs, '\n')


	### NOTE: might be smarter to wrap everything above in an init() function or separate
	### post-processing script.
	### NOTE: could check for DMS files before running everything above

	### call rna_predict_chem_map on 20 lowest energy pdbs for target
	rdat_files = map(lambda x: x+'.DMS.rdat', target_pdbs)
	cmdline = [path_to_rosetta_exe+'rna_predict_chem_map', '-s'] + target_pdbs
	while len(filter(lambda x: exists(x), rdat_files)) != len(rdat_files):
		out,err = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		if len(filter(lambda x: exists(x), rdat_files)) != len(rdat_files):
			print 'CMDLINE:', cmdline
			print 'OUT:', out
			print 'ERROR:', err
	assert(len(filter(lambda x: exists(x), rdat_files)) == len(rdat_files))

	target_mean_seqpos_reactivity[ target_idx ] = rdat.mean_seqpos_reactivity(rdat_files, return_sample_idx=1, verbose=True)
	rdat_headers[ target_idx ] = rdat.header
	### return to run directory
	os.chdir( homedir )


rdat_fout = basename(os.getcwd()) + '_DMS.rdat' #'TEST.DMS.rdat'
rdat.write_data(rdat_fout, target_mean_seqpos_reactivity, rdat_headers)



'''
USE:
../../../scripts/python/analysis/rna_experimental_chem_map.py -rdat_file TEST.DMS.rdat -make_rna_chemical_map -plot_seqpos_error -error_seqpo 5 13


rdat_fname = basename( os.getcwd() ).replace('rna_res_level_energy4_','')

### After data has been collected for all targets ... make plots?
if args.make_rna_chemical_map:
	pdfname = rdat_fname + '_DMS_Predictions_Chemical_Map.pdf' 
	title = pdfname.replace('_',' ').replace('.pdf','')
	make_rna_chemical_map(target_mean_seqpos_reactivity, fullpdfname=pdfname, title=title)


if args.plot_seqpos_error:
	pdfname = rdat_fname + '_Predictions_Error.pdf'
	title = pdfname.replace('_',' ').replace('.pdf','') 
	assert( args.error_seqpos )
	error_seqpos1 = int(args.error_seqpos[0])
	error_seqpos2 = int(args.error_seqpos[-1])
	plot_seqpos_error(target_mean_seqpos_reactivity, error_seqpos1, error_seqpos2, fullpdfname=pdfname, title=title)
'''
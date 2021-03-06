#!/usr/bin/python

################################################################################
### import modules
################################################################################
import os
import argparse
import subprocess as sp
import multiprocessing as mp
from os.path import exists, basename, dirname, isdir, abspath
from glob import glob
from create_stepwise_benchmark_table_util import *


################################################################################
### main function
################################################################################
def get_target_row(target, (args)):

    ############################################################################
    ### change into target_dir and find all silent files
    ############################################################################
    working_dir = os.getcwd()
    os.chdir(target)

    ############################################################################
    ### get table info
    ############################################################################
    table_row = TableRow()
    table_row.add_columns( get_title( target ) )
    table_row.add_columns( get_target_properties() )
    table_row.add_columns( get_best_of_lowest_energy_cluster_centers() )
    table_row.add_columns( get_lowest_rmsd_model() )
    table_row.add_columns( get_lowest_energy_sampled( args.opt_exp_inpaths ) )

    ############################################################################
    ### change back to working directory
    ############################################################################
    os.chdir(working_dir)
    return table_row


################################################################################
### main script
################################################################################
if __name__=='__main__':


    ############################################################################
    ### parse arguments
    ############################################################################
    parser = argparse.ArgumentParser(
        description='Create a table of lowest energies/rmsds, \
                     and best of 5 cluster center rmsds from \
                     a list of runs (one table per run).'
    )

    parser.add_argument(
        'inpaths',
        nargs='+',
        help='List of paths to target runs.'
    )
    parser.add_argument(
        '-opt_exp_inpaths',
        nargs='+',
        help='List of paths to optimized experimental target runs.',
        default=[]
    )
    parser.add_argument(
        '-t','--targets',
        nargs='+',
        help='List of targets.',
        default=[]
    )
    parser.add_argument(
        '-s','--silent_file_name',
        help='Names of final silent files.',
        default=['region_FINAL.out','swm_rebuild.out']
    )
    parser.add_argument(
        '-f','--force',
        help='Rewrite tables even if they alread exist.',
        action='store_true'
    )
    parser.add_argument(
        '-j','--nproc',
        help='Number of jobs to run in parallel',
        default=(mp.cpu_count()-1)
    )
    parser.add_argument(
        '-m','--merge_tables',
        help='Merge tables created for each inpath, into a single table.',
        action='store_true'
    )

    args = parser.parse_args()
    inpaths = sorted( args.inpaths )
    user_targets = sorted( args.targets )
    force = args.force
    nproc = int(args.nproc)
    merge_tables = args.merge_tables

    ############################################################################
    ### checks and initializations
    ############################################################################
    assert( all( exists( inpath ) for inpath in inpaths ) )
    working_dir = os.getcwd()

    ############################################################################
    ### change into inpaths and get targets
    ############################################################################
    for idx, inpath in enumerate(inpaths, start=1):

        print '\n[%d/%d] Creating Table for Run: %s' % (idx,len(inpaths),inpath)

		########################################################################
        ### continue if table exists and not args.force
        ########################################################################
        table_name = inpath.upper() + '.tab'
        if exists('/'.join([inpath, table_name])):
            print "[WARNING] Table:", table_name, "already exists!!!"
            if not force:
            	print "[HINT] run with '--force' to re-write table"
            	continue
            else:
                print "[WARNING] detected '--force' option ... re-writing table"

        #######################################################################
        ### change into inpath
        ########################################################################
        os.chdir( inpath )

        ########################################################################
        ### find all targets in inpath
        ########################################################################
        found_targets = sorted(filter(isdir, glob('*')))
        if len(user_targets):
            found_targets = filter(user_targets.count, found_targets)
        targets = filter(found_targets.count, get_target_names())
        print '\nTARGETS:\n%s\n' % ('\n'.join(targets))

        ########################################################################
        ### get table info for all targets found in inpath
        ########################################################################
        if nproc > 0:
            pool = mp.Pool(processes=nproc)

            out = [pool.apply_async(get_target_row,args=(t,args)) for t in targets]
            table_row_list = [o.get() for o in out]

            pool.close()
            pool.join()

        else:
            table_row_list = [get_target_row(t,args) for t in targets]

        ########################################################################
        ### create table for inpath
        ########################################################################
        table_name = inpath.upper() + '.tab'
        if exists( table_name ) and not force:
            print "Table:", table_name, "already exists!!!"
        else:
            table = Table( table_name )
            table.add_row( column_labels )
            table.add_row( subcolumn_labels )
            for table_row in table_row_list:
                table.add_data_row( table_row.columns() )
            table.add_row( ['AVERAGE'] + table.column_averages()[1:] )
            table.save()

        ########################################################################
        ### change back into working directory
        ########################################################################
        os.chdir( working_dir )

    ###################################################################
    ### combine tables from each inpath into one table
    ###################################################################
    if merge_tables and len(inpaths) > 1:
        print '\nMerging Tables for Runs:\n%s\n' % ('\n'.join(inpaths))
        subtable_names = [ip+'/'+ip.upper()+'.tab' for ip in inpaths]
        table_name = '_v_'.join(inpaths).upper() + '.tab'
        if exists(table_name):
            print "[WARNING] Table:", table_name, "already exists!!!"
            if not force:
            	print "[HINT] run with '--force' to re-write table"
            else:
                print "[WARNING] '--force' option detected ... re-writing table"
        if not exists( table_name ) or force:
            table = Table( table_name )
            table.merge_tables( subtable_names )
            table.save()

    ###################################################################
    ### exit
    ###################################################################
    exit(True)

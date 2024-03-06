#!/usr/bin/env python3

# Rebecca Ansorge 2021

import pandas as pd
import sys
import argparse
import datetime
import os

def main(argv):
    # define user input
    parser = argparse.ArgumentParser(description='merge bracken reports')
    parser.add_argument('-i', '--inputdir', required=True, help='set input directory containing reports')
    parser.add_argument('-o', '--outprefix', required=True, help='set path and prefix for output (e.g. MyData)')

    args = parser.parse_args()

    # set wd
    workingdir = os.chdir(args.inputdir)
    # list all files in wd and save as entries
    entries = os.listdir(workingdir)

    # create combi dataframe with column name used for merging in loop
    combi_rel = pd.DataFrame(columns = ['taxid','taxa','taxlevel'])
    combi_reads = pd.DataFrame(columns = ['taxid','taxa','taxlevel'])

    # loop over all files in wd that end with annotations
    for rep in entries:
        if rep.endswith('report'):
            print('processing dataset ==> ', rep)
            sample = pd.read_csv(rep, sep='\t', names=['rel_abund','reads','reads_lvl','taxlevel','taxid','taxa'])
            relabun = sample.loc[:,['rel_abund','taxlevel','taxid','taxa']]
            relabun.columns = [rep, 'taxlevel','taxid','taxa']
            reads = sample.loc[:,['reads','taxlevel','taxid','taxa']]
            reads.columns = [rep, 'taxlevel','taxid','taxa']
            combi_rel = pd.merge(combi_rel, relabun, how='outer', on=['taxid','taxa','taxlevel'])
            combi_reads = pd.merge(combi_reads, reads, how='outer', on=['taxid','taxa','taxlevel'])

    combi_rel = combi_rel.reindex(sorted(combi_rel.columns,reverse=True), axis=1)
    combi_reads = combi_reads.reindex(sorted(combi_reads.columns,reverse=True), axis=1)

    print(combi_rel.head())
    print(combi_reads.head())

    combi_rel.to_csv(args.outprefix + '_rel_abund.csv', index=False)
    combi_reads.to_csv(args.outprefix + '_read_numbers.csv', index=False)

    now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    # bye bye
    print(now,'\nAll done - bye bye!')

if __name__ == "__main__": main(sys.argv[1:])
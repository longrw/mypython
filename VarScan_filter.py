#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
CMD: python /haplox/users/longrw/mypython/VarScan_filter.py S010_cfdna_snv_annovar.hg19_multianno.txt S010_cfdna_indel_annovar.hg19_multianno.txt S010_cfdna_snv_annovar.hg19_multianno_filter.txt S010_cfdna_indel_annovar.hg19_multianno_filter.txt rectum_roche S010_cfdna_snv-GB18030_filter.csv S010_cfdna_indel-GB18030_filter.csv
'''

import os
import sys
import csv

def clean(snvR,indelR,snvF,indelF):
    os.system('perl /haplox/users/longrw/mypython/VarScan_filter.pl {0} {1} {2} {3}'.format(snvR,indelR,snvF,indelF))

def fetch(iput,panel,oput):
    genes = []
    csvfile = open('/haplox/ref/guolin_probe.csv', "r")
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row[panel]:
            genes.append(row[panel])
    csvfile.close()
    ks,vs = [],[]
    for line in open(iput):
        lst = line.strip().split('\t')
        if lst[4] in genes:
            csv_filter = '{0},{1},{2},{3},{4},{5},{6}'.format(lst[0], lst[1], lst[4], lst[6]+':'+lst[7], lst[8], lst[9], lst[10])
            ks.append(csv_filter)
            vs.append(lst[9])
    d = dict(zip(ks,vs))
    d_sort = sorted(d.iteritems(), key = lambda d:d[1], reverse = True)
    for key,value in d_sort:
        with open(oput, 'a') as f:
            f.write(key + '\n')

if __name__ == '__main__':
    snvR,indelR,snvF,indelF,panel,oput_snv,oput_indel = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7]
    clean(snvR,indelR,snvF,indelF)
    fetch(snvF,panel,oput_snv)
    fetch(indelF,panel,oput_indel)

#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import division
import sys
import os
import gzip
from multiprocessing import Pool
'''
CMD: python ./bpSize.py /haplox/rawfq/160517_ST-E00209_0182_AHNHF7CCXX > 160517ymkd.csv---so slowly!!!
'''
def bpsize(f):
    m, bpSize = 1, 0
    len_bps = [(n,len(line.strip())) for (n,line) in enumerate(gzip.open(f))]
    for len_bp in len_bps:
        if len_bp[0] == m:
            bpSize = bpSize + len_bp[1]
            m += 4
    print f + ',' + '%.3f' % (bpSize/1024**3)

def bpsize1(f):
    m, bpSize = 0, 0
    for line in gzip.open(f):
        m += 1
        if m % 4 == 2:
            bpSize += len(line.strip())
    print f + ',' + '%.3f' % (bpSize/1024**3)

def main():
    path = sys.argv[1]
    os.chdir(path)
    fs = filter(lambda x:x.endswith('R1_001.fastq.gz') or x.endswith('R2_001.fastq.gz'), os.listdir('./'))
    p = Pool(30)
#    p.map(bpsize, fs)
    p.map(bpsize1, fs)
    p.close()
    p.join()

if __name__ == "__main__":
    main()

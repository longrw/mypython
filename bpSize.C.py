#!/usr/bin/env python
#-*- coding:utf-8 -*-
from multiprocessing import Pool
import sys
import os
'''
CMD:python /haplox/users/longrw/mypython/bpSize.C.py /haplox/rawfq/160530_NS500713_0054_AH2YKNBGXY > 20160530sequencer.csv
'''
def bpsize(f):
    os.system("/haplox/users/longrw/mypython/count " + f)
def main():
    path = sys.argv[1]
    os.chdir(path)
    fs = filter(lambda x:x.endswith('R1_001.fastq.gz') or x.endswith('R2_001.fastq.gz') or x.endswith('R1_001.fastq') or x.endswith('R2_001.fastq'), sorted(os.listdir('./')))
    p = Pool(30)
    p.map(bpsize, fs)
    p.close()
    p.join()
if __name__ == "__main__":
    main()


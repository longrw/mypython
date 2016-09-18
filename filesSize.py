#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
command: python filesSize.py /haplox/rawfq/160424_NS500713_0049_AH2YVLBGXY > tst.csv
'''
from __future__ import division
import sys
import os
from os.path import getsize

path = sys.argv[1]
os.chdir(path)
for f1 in filter(lambda x:x.endswith('R1_001.fastq.gz') or x.endswith('R2_001.fastq.gz'), sorted(os.listdir('./'))):
    s1 = os.path.getsize(f1)/1024**3
    if s1 < 0.5:
        print f1 + ',' + '%.3fG' % s1 + ',' + 'Warning'
    elif s1 > 10:
        print f1 + ',' + '%.3fG' % s1 + ',' + 'Bigdata'
    else:
        print f1 + ',' + '%.3fG' % s1
print '-,-,-'
os.chdir('good')
for f2 in filter(lambda x:x.endswith('R1_001.good.fq') or x.endswith('R2_001.fastq.gz'), sorted(os.listdir('./'))):
    s2 = os.path.getsize(f2)/1024**3
    print f2 + ',' + '%.3fG' % s2

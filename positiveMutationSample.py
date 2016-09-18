#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
CMD:python  positiveMutationSample.py /haplox/rawout/160302/cfdna2gdna/colorectum
filter samples which contains positive mutation such as <RAS p.G12>
'''
import os
import sys

path = sys.argv[1]
os.chdir(path)
vcfFiles = filter(lambda f: f.endswith('_snp_GB18030.csv'), os.listdir('./'))
for vcfFile in vcfFiles:
    for line in open(vcfFile):
        if 'RAS' in line.strip().split(',')[2] and 'exon2' in line.strip().split(',')[3] and 'p.G12' in line.strip().split(',')[4]:
            print vcfFile + ',' + line

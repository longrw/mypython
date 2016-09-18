#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
command: python ./all_barcodes_6_Hisq.py 上机信息--20160418.CSV 20160418samplesheet.csv 20160418human.csv
'''

import os
import sys

index_seqs = [line.rstrip().split(",") for line in open("/haplox/users/longrw/pipeline/csv2sampsheetandhuman/all_Indexs.csv")]
ks,vs = [],[]
for index_seq in index_seqs:
    ks.append(index_seq[0])
    vs.append(index_seq[1])
d = dict(zip(ks,vs))

seqInfo = [line.rstrip().split(",") for line in open("/haplox/users/longrw/pipeline/csv2sampsheetandhuman/" + sys.argv[1])]
f1 = open("/haplox/users/longrw/pipeline/csv2sampsheetandhuman/" + sys.argv[2],"w")
f2 = open("/haplox/users/longrw/pipeline/csv2sampsheetandhuman/" + sys.argv[3],"w")
num = 1
for info in seqInfo:
    laneID,sampleID,sampleType,panelType,indexID,data = info[0],info[1],info[8],info[13],info[9],info[15]
    if sampleID == "/":
        name = ("S%03d" + "_" + sampleType + "_" + panelType) % num
    else:
        name = ("S%03d" + "_" + sampleID + "_" + sampleType + "_" + panelType) % num
    num += 1
    if indexID in d.keys():
        index = d[indexID][:6]
    sample = laneID + "," + name + "," + name + ",,," + indexID + "," + index + ",,,,"
    print >> f1,sample
    sample_data = name + "," + data
    print >> f2,sample_data
f1.close()
f2.close()

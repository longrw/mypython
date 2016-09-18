#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
CMD:python /haplox/users/longrw/mypython/humanVSsequencer.py 20160513human.csv /haplox/rawfq/160513_NS500713_0052_AH2YVNBGXY  20160513
compare data yield of human estimated to actual output
'''
from __future__ import division
import os
import sys


def humanVSsequencer(human, sequencer, output):
    ks, vs = [], []
    for line1 in open(human):
        ks.append(line1.strip().split(',')[0])
        vs.append(line1.strip().split(',')[1])
    d=dict(zip(ks, vs))
    f=open(output, 'w')
    for line2 in open(sequencer):
        if line2.strip().split(',')[0].endswith('001.fastq.gz') or line2.strip().split(',')[0].endswith('001.fastq'):
            k=line2.strip().split('_R')[0]
            if k in d:
                if line2.strip().split('_')[-3].startswith('L00'):
                    print >> f, line2.strip().split('_')[0] + '_' + line2.strip().split('_')[
                                            -2] + "," + str(float(d[k]) / 2) + "," + line2.strip().split(',')[1].replace('G', '')
                else:
                    print >> f, line2.strip().split('_')[0] + '_' + line2.strip().split('_')[
                                            -2] + "," + str(float(d[k]) / 2) + "," + line2.strip().split(',')[1].replace('G', '')
        else:
            continue
    f.close()

def main():
    human, path, num=sys.argv[1], sys.argv[2], sys.argv[3]
    sequencer=num + "_sequencer.csv"
    sequencer_sort=num + "_sequencer_sort.csv"
    output="humanVSsequencer_" + num + ".csv"
    if not os.path.exists(sequencer_sort):
        os.system(
            "python /haplox/users/longrw/mypython/bpSize.C.py %s > %s" % (path, sequencer))
        os.system("sort -V %s > %s" % (sequencer, sequencer_sort))
    humanVSsequencer(human, sequencer_sort, output)
    if not os.path.exists(num + '.png'):
        os.system(
            "Rscript /haplox/users/longrw/myR/humanVSsequencer_yield.R %s %s" % (output, num))

if __name__ == "__main__":
    main()

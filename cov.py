#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import division
import sys

def coverage(f):
    depths = [int(row.strip().split('\t')[-1]) for row in open(f)]
    mean_depth = '%.1f' % (sum(depths)/len(depths))
    covs = []
    covs.append(mean_depth)
    xs = [1,5,20,50,100,200,500,1000,2500,5000,7500,10000]
    for x in xs:
        cov = '%.3f' % (len([depth for depth in depths if depth > x])/len(depths))
        covs.append(cov)
    coverages = ','.join(covs)
    print f + ',' + coverages
if __name__ == '__main__':
    files = [sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]]
    map(coverage,files)

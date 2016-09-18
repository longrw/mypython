#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import division
import sys
def flagstat(gSmap,gMmap,cfSmap,cfMmap):
    gslines = [line.strip() for line in open(gSmap)]
    gmlines = [line.strip() for line in open(gMmap)]
    cfslines = [line.strip() for line in open(cfSmap)]
    cfmlines = [line.strip() for line in open(cfMmap)]

    gdnaCleanreads = gslines[0].split(' ')[0]
    gdnaMapreads = gslines[4].split(' ')[0]
    gdnaMapreads_dedup = gmlines[4].split(' ')[0]
    gdnaInfo = []
    gdnaInfo.append(gdnaCleanreads)
    gdnaMap_rate = '%.4f' % (int(gdnaMapreads)/int(gdnaCleanreads))
    gdnaInfo.append(gdnaMap_rate)
    gdnaDup_rate = '%.4f' % (1 - int(gdnaMapreads_dedup)/int(gdnaMapreads))
    gdnaInfo.append(gdnaDup_rate)

    cfdnaCleanreads = cfslines[0].split(' ')[0]
    cfdnaMapreads = cfslines[4].split(' ')[0]
    cfdnaMapreads_dedup = cfmlines[4].split(' ')[0]
    cfdnaInfo = []
    cfdnaInfo.append(cfdnaCleanreads)
    cfdnaMap_rate = '%.4f' % (int(cfdnaMapreads)/int(cfdnaCleanreads))
    cfdnaInfo.append(cfdnaMap_rate)
    cfdnaDup_rate = '%.4f' % (1 - int(cfdnaMapreads_dedup)/int(cfdnaMapreads))
    cfdnaInfo.append(cfdnaDup_rate)

    print ','.join(gdnaInfo) + ',' + ','.join(cfdnaInfo)

if __name__ == "__main__":
    gSmap,gMmap,cfSmap,cfMmap = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
    flagstat(gSmap,gMmap,cfSmap,cfMmap)

#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import division
import sys
def flagstat(gSmap,gMmap):
    gslines = [line.strip() for line in open(gSmap)]
    gmlines = [line.strip() for line in open(gMmap)]

    gdnaCleanreads = gslines[0].split(' ')[0]
    gdnaMapreads = gslines[4].split(' ')[0]
    gdnaMapreads_dedup = gmlines[4].split(' ')[0]
    gdnaInfo = []
    gdnaInfo.append(gdnaCleanreads)
    gdnaMap_rate = '%.4f' % (int(gdnaMapreads)/int(gdnaCleanreads))
    gdnaInfo.append(gdnaMap_rate)
    gdnaDup_rate = '%.4f' % (1 - int(gdnaMapreads_dedup)/int(gdnaMapreads))
    gdnaInfo.append(gdnaDup_rate)

    print ','.join(gdnaInfo)

if __name__ == "__main__":
    gSmap,gMmap = sys.argv[1],sys.argv[2]
    flagstat(gSmap,gMmap)

#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import pysam

def bam2fq(bamfile):
    f = pysam.AlignmentFile(bamfile,'rb')
    for read in f:
        if read.is_proper_pair and read.is_read1:
            pos = f.tell()
            try:
                mate = f.mate(read)
            except ValueError:
                # Invalid mate (usually post-filtered)
                continue
            finally:
                f.seek(pos)
            if read.reference_name == 'chr1' and mate.reference_name == 'chr1':
                print read.qname,'\n',mate.qname

if __name__ == "__main__":
    bamfile = sys.argv[1]
    bam2fq(bamfile)

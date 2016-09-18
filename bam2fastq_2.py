#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import pysam
import string

rule = string.maketrans("ATCGN", "TAGCN")

def aln_stat(read):
    flag = 1
    if read.is_read2:
        flag = 2
    if read.is_reverse:
        seq = read.seq.translate(rule)[::-1]
        qual = read.qual[::-1]
        return "@%s/%d\n%s\n+\n%s\n" % (read.qname, flag, seq, qual)
    else:
        return "@%s/%d\n%s\n+\n%s\n" % (read.qname, flag, read.seq, read.qual)

def bam2fq(bamfile):
    chrom = ['chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrY','chrX','chrM']
#    chrom = map(lambda x:'chr'+x, range(1,23))
    temp_len = range(5,31)

    f = pysam.AlignmentFile(bamfile,'rb')
    for read in f.fetch():
        #chromosome
        if (read.reference_name in chrom):
            with open(read.reference_name + '.fq', 'a') as f:f.write(aln_stat(read))

        #template_length
        if (abs(read.template_length) < 50):
            with open('templen_low.fq', 'a') as f:f.write(aln_stat(read))

        if (abs(read.template_length)/10 in temp_len):
            temp = ''.join(['templen',str((abs(read.template_length)/10)*10)])
            with open(temp + '.fq', 'a') as f:f.write(aln_stat(read))

        if (abs(read.template_length) > 300):
            with open('templen_high.fq', 'a') as f:f.write(aln_stat(read))

        #forward_reverse
        if read.is_reverse:
            with open('reverse.fq','a') as f:f.write(aln_stat(read))
        else:
            with open('forward.fq','a') as f:f.write(aln_stat(read))

        #chromosome + forward_reverse
        if  read.is_reverse:
            if (read.reference_name in chrom):
                with open(read.reference_name + '_reverse.fq', 'a') as f:f.write(aln_stat(read))
        else:
            if (read.reference_name in chrom):
                with open(read.reference_name + '_forward.fq', 'a') as f:f.write(aln_stat(read))
    f.close()

def main():
    bamfile = sys.argv[1]
    bam2fq(bamfile)

if __name__ == "__main__":
    main()

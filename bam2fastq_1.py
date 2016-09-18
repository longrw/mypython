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
    temp_len = range(5,31)

    f = pysam.AlignmentFile(bamfile,'rb')
    for read in f.fetch():
        #chromosome
        if (read.reference_name in chrom):
#        if (read.reference_name in chrom) and read.is_read1:
#            read1 = '@'+read.qname+':1\n'+read.seq+'\n+\n'+read.qual+'\n'
            with open(read.reference_name + '.fq', 'a') as f:f.write(aln_stat(read))
#        elif (read.reference_name in chrom) and read.is_read2:
#            read2 = '@'+read.qname+':2\n'+read.seq+'\n+\n'+read.qual+'\n'
#            with open(read.reference_name + '.fq', 'a') as f:f.write(read2)

        #template_length
        if (abs(read.template_length) < 50):#if (abs(read.template_length) < 50) and read.is_read1:
#            low1 = '@'+read.qname+':1\n'+read.seq+'\n+\n'+read.qual+'\n'
            with open('templen_low.fq', 'a') as f:f.write(aln_stat(read))
#        elif (abs(read.template_length) < 50) and read.is_read2:
#            low2 = '@'+read.qname+':2\n'+read.seq+'\n+\n'+read.qual+'\n'
#            with open('templen_low.fq', 'a') as f:f.write(low2)

        if (abs(read.template_length)/10 in temp_len):#if (abs(read.template_length)/10 in temp_len) and read.is_read1:
#            temp1 = '@'+read.qname+':1\n'+read.seq+'\n+\n'+read.qual+'\n'
            temp = ''.join(['templen',str((abs(read.template_length)/10)*10)])
            with open(temp + '.fq', 'a') as f:f.write(aln_stat(read))
#        elif (abs(read.template_length)/10 in temp_len) and read.is_read2:
#            temp = ''.join(['templen',str((abs(read.template_length)/10)*10)])
#            temp2 = '@'+read.qname+':2\n'+read.seq+'\n+\n'+read.qual+'\n'
#            with open(temp + '.fq', 'a') as f:f.write(temp2)

        if (abs(read.template_length) > 300):#if (abs(read.template_length) > 300) and read.is_read1:
#            high1 = '@'+read.qname+':1\n'+read.seq+'\n+\n'+read.qual+'\n'
            with open('templen_high.fq', 'a') as f:f.write(aln_stat(read))
#        elif (abs(read.template_length) > 300) and read.is_read2:
#            high2 = '@'+read.qname+':2\n'+read.seq+'\n+\n'+read.qual+'\n'
#            with open('templen_high.fq', 'a') as f:f.write(high2)

        #forward_reverse
        if read.is_reverse:
            with open('reverse.fq','a') as f:f.write(aln_stat(read))
#            if read.is_read1:
#                reverse1 = '@'+read.qname+':1\n'+read.seq+'\n+\n'+read.qual+'\n'
#                with open('reverse.fq','a') as f:f.write(reverse1)
#            elif read.is_read2:
#                reverse2 = '@'+read.qname+':2\n'+read.seq+'\n+\n'+read.qual+'\n'
#                with open('reverse.fq','a') as f:f.write(reverse2)
        else:
            with open('forward.fq','a') as f:f.write(aln_stat(read))
#            if read.is_read1:
#                forward1 = '@'+read.qname+':1\n'+read.seq+'\n+\n'+read.qual+'\n'
#                with open('forward.fq','a') as f:f.write(forward1)
#            elif read.is_read2:
#                forward2 = '@'+read.qname+':2\n'+read.seq+'\n+\n'+read.qual+'\n'
#                with open('forward.fq','a') as f:f.write(forward2)

        #chromosome + forward_reverse
        if  read.is_reverse:
            if (read.reference_name in chrom):#if (read.reference_name in chrom) and read.is_read1:
#                chreverse1 = '@'+read.qname+':1\n'+read.seq+'\n+\n'+read.qual+'\n'
                with open(read.reference_name + '_reverse.fq', 'a') as f:f.write(aln_stat(read))
#            elif (read.reference_name in chrom) and read.is_read2:
#                chreverse2 = '@'+read.qname+':2\n'+read.seq+'\n+\n'+read.qual+'\n'
#                with open(read.reference_name + '_reverse.fq', 'a') as f:f.write(chreverse2)
        else:
            if (read.reference_name in chrom):#if (read.reference_name in chrom) and read.is_read1:
#                chforward1 = '@'+read.qname+':1\n'+read.seq+'\n+\n'+read.qual+'\n'
                with open(read.reference_name + '_forward.fq', 'a') as f:f.write(aln_stat(read))
#            elif (read.reference_name in chrom) and read.is_read2:
#                chforward2 = '@'+read.qname+':2\n'+read.seq+'\n+\n'+read.qual+'\n'
#                with open(read.reference_name + '_forward.fq', 'a') as f:f.write(chforward2)

if __name__ == "__main__":
    bamfile = sys.argv[1]
    bam2fq(bamfile)

#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
CMD: python /haplox/users/longrw/mypython/targte_point_stat.py /haplox/users/longrw/colorectum/colorectum_target_SNV.txt S014-20160722002-1-cfdna_rg.bam S014-20160722002-1-cfdna_rg.txt
'''
import os
import sys

def target_stat_in_bam(target,iput,oput,ref):
    for line1 in open(target):
        line1_lst = line1.strip().split(',')
        position = ':'.join([line1_lst[0],line1_lst[1]])
        os.system("samtools tview -p {0} {1} {2} -d txt > {3}".format(position,iput,ref,oput))
#        print "samtools tview -p {0} {1} {2} -d txt > {3}".format(position,iput,ref,oput)
        bases = []
        n = 0
        ref_b = ''
        for line2 in open(oput):
            base = line2.strip()[:1]
            n += 1
            if n == 2:ref_b = base
            if n > 2:bases.append(base)
        A = bases.count('A')
        a = bases.count('a')
        G = bases.count('G')
        g = bases.count('g')
        C = bases.count('C')
        c = bases.count('c')
        T = bases.count('T')
        t = bases.count('t')
        ref_b_forward = bases.count('.')
        ref_b_reverse = bases.count(',')

        print '#'*100
        print 'Target point of {0} {1} {2}:'.format(line1_lst[3],position,line1_lst[2])
        print 'Depth : {0}'.format(n-2)
        print 'Refence base : {0}'.format(ref_b)
        print 'Refence forward base number : {0}  {1:.2%}'.format(ref_b_forward,float(ref_b_forward)/float(n-2))
        print 'Refence reverse base number : {0}  {1:.2%}'.format(ref_b_reverse,float(ref_b_reverse)/float(n-2))
        print 'A base number : {0}  {1:.2%}'.format(A,float(A)/float(n-2))
        print 'a base number : {0}  {1:.2%}'.format(a,float(a)/float(n-2))
        print 'G base number : {0}  {1:.2%}'.format(G,float(G)/float(n-2))
        print 'g base number : {0}  {1:.2%}'.format(g,float(g)/float(n-2))
        print 'C base number : {0}  {1:.2%}'.format(C,float(C)/float(n-2))
        print 'c base number : {0}  {1:.2%}'.format(c,float(c)/float(n-2))
        print 'T base number : {0}  {1:.2%}'.format(T,float(T)/float(n-2))
        print 't base number : {0}  {1:.2%}'.format(t,float(t)/float(n-2))
        print '#'*100

if __name__ == "__main__":
    target,iput,oput = sys.argv[1],sys.argv[2],sys.argv[3]
    ref = '/haplox/ref/GATK/ucsc.hg19/ucsc.hg19.fasta'
    target_stat_in_bam(target,iput,oput,ref)

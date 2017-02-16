#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

def searchIndex(f,output):
    if '.fastq.gz' in f:
        if 'L00' in f:
            os.system("gunzip -c %s | sed -n '/@ST-E/p' | awk -F \":\" '{print $10}' | awk -F \"+\" '{print $1}' > %s/Undetermined_Index" % (f,output))
        else:
            os.system("gunzip -c %s | sed -n '/@NB551106/p' | awk -F \":\" '{print $10}' | awk -F \"+\" '{print $1}' > %s/Undetermined_Index" % (f,output))
    elif '.fastq' in f:
        if 'L00' in f:
            os.system("sed -n '/@ST-E/p' %s | awk -F \":\" '{print $10}' | awk -F \"+\" '{print $1}' > %s/Undetermined_Index" % (f,output))
        else:
            os.system("sed -n '/@NB551106/p' %s | awk -F \":\" '{print $10}' | awk -F \"+\" '{print $1}' > %s/Undetermined_Index" % (f,output))
    os.chdir(output)
    os.system("sort -o Undetermined_Index_sort Undetermined_Index")
    os.system("uniq -c Undetermined_Index_sort > Undetermined_Index_sort_uniq")
    os.system("sort -n -r -o Undetermined_Index_sort_uniq_sort Undetermined_Index_sort_uniq")
    os.system("sed -n '1,20p' Undetermined_Index_sort_uniq_sort > %s_Undetermined_Index_top20.txt" % f.split('/')[-1])

    os.system("rm -rf Undetermined_Index Undetermined_Index_sort Undetermined_Index_sort_uniq Undetermined_Index_sort_uniq_sort ")

def main():
    f,output = sys.argv[1],sys.argv[2]
    searchIndex(f,output)

if __name__ == "__main__":
    main()

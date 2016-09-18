#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys

def searchIndex(f):
    fname = f.split('_')[-3]
    if fname[:3] == 'L00':
#        os.system("gunzip -c %s | sed -n '/@ST-E00244/p' | awk -F \":\" '{print $10}' > Undetermined_Index" % f) ##ymkd
        os.system("gunzip -c %s | sed -n '/@ST-E00169/p' | awk -F \":\" '{print $10}' | awk -F \"+\" '{print $2}' > Undetermined_Index" % f) ##yjk
    else:
        os.system("gunzip -c %s | sed -n '/@NS500713/p' | awk -F \":\" '{print $10}' | awk -F \"+\" '{print $2}' > Undetermined_Index" % f) ##nextseq500
    os.system("sort -o Undetermined_Index_sort Undetermined_Index")
    os.system("uniq -c Undetermined_Index_sort > Undetermined_Index_sort_uniq")
    os.system("sort -n -r -o Undetermined_Index_sort_uniq_sort Undetermined_Index_sort_uniq")
    if fname[:3] == 'L00':
        os.system("sed -n '1,20p' Undetermined_Index_sort_uniq_sort > Undetermined_Index_%s_top20.txt" % fname)
    else:
        os.system("sed -n '1,20p' Undetermined_Index_sort_uniq_sort > Undetermined_Index_20.txt")
    os.system("rm -rf Undetermined_Index Undetermined_Index_sort Undetermined_Index_sort_uniq Undetermined_Index_sort_uniq_sort ")

def main():
    f = sys.argv[1]
    searchIndex(f)

if __name__ == "__main__":
    main()

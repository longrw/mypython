#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys

def chemo_csv(f, out):
    for line in open(f):
        line_lst = line.strip().split('\t')
        csv = '%s,%s,%s\n' % (line_lst[3],line_lst[4],line_lst[5])
        out.write(csv)
if __name__ == '__main__':
    f = sys.argv[1]
    out = open(sys.argv[2], "w")
    chemo_csv(f,out)

#!/usr/bin/env python

import os

flst = filter(lambda x: x.endswith("_mark.txt"), os.listdir("../"))
bed = open("/haplox/users/hy/Test/bed/Colorectal_Roche_annotate.bed")

bed_stat = dict()
for line in bed:
    lst = line.strip().split("\t")
    chrn, start, gene = lst[0], lst[1], lst[-1]
    if chrn not in bed_stat:
        bed_stat[chrn] = {}
    if start not in bed_stat[chrn]:
        bed_stat[chrn][start] = gene

for f in flst:
    out = open("%s_depth.txt" % f.split("_mark.txt")[0], "w")
    for line in open("../"+f):
        lst = line.strip().split("\t")
        chrn, start = lst[0], lst[1]
        lst.insert(3, bed_stat[chrn][start])
        out.write("\t".join(lst) + "\n")
    out.close()

#!/usr/bin/env pypy

import os
import sys
import subprocess
from optparse import OptionParser


def parseCommand():
    usage = "usage: %prog -bed bed file -bam bam file -o output dir"
    parser = OptionParser(usage=usage)
    parser.add_option("-b", dest="bed", help="bed file")
    parser.add_option("-i", dest="bam", help="bam file")
    parser.add_option("-o", dest="outputdir", help="output dir")
    return parser.parse_args()


def bed_stat(bed):
    bed_info = dict()
    with open(bed, "r") as f:
        for line in f:
            lst = line.strip().split()
            chrn, start, end = lst[0], int(lst[1]), int(lst[2])
            if chrn not in bed_info:
                bed_info[chrn] = list()
            bed_info[chrn].append((start, end))
    return bed_info


def coverage(bed, bed_info):
    num_bed = 0
    with open(bed, "r") as f:
        for line in f:
            lst = line.strip().split()
            chrn, start, end = lst[0], int(lst[1]), int(lst[2])
            if chrn in bed_info:
                for i in bed_info[chrn]:
                    if i[0] <= start <= i[1] or i[0] <= end <= i[1]:
                        num_bed += 1
                        break
    return num_bed

if __name__ == "__main__":
    options, args = parseCommand()
    for i in ["bed", "bam", "outputdir"]:
        if getattr(options, i) == None:
            print "type python check_coverage.py -h for help"
            break
    else:
        bam_name = os.path.basename(options.bam).split(".bam")[0]
        output = open("%s/%s_capture_stat.txt" % (options.outputdir, bam_name), "w")
        os.system("bedtools bamtobed -i %s > %s/%s.bed" % (options.bam, options.outputdir, bam_name))
        read_num = int(subprocess.check_output("samtools flagstat %s" % options.bam, shell=True).split()[0])
        bed_info = bed_stat(options.bed)
        bed_num = coverage("%s/%s.bed" % (options.outputdir, bam_name), bed_info)
        output.write("%s capture percentage:\t%.2f%%\n" % (os.path.basename(options.bam), float(bed_num) / read_num * 100))
        output.close()
        os.system("rm %s/%s.bed" % (options.outputdir, bam_name))

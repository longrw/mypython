#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    File name: pipeline.py
    Author: Yue Han
    Date created: 4/20/2016
    Date last modified: 4/27/2016
    Python Version: 2.7
    Please put this file in rawseq folder
"""

import os
import re
from multiprocessing import Pool
import time

pattern = re.compile(r'(S\d+-|_)(.+-|_)(cfdna|ffpedna|pedna|fnadna)(.+)(lung|gene77|roche929|rectum|stomach|breast|liver)(.+)R1_001.good.fq$')

class Seq:
    def __init__(self, raw_name):
        self.rawfq_path = os.path.abspath("./")
        self.rawout_path = self.rawfq_path[:-5].replace("rawfq", "rawout")
        self.rawname = raw_name
        self.match = re.match(pattern, self.rawname).groups()
        self.data_type = self.match[2]
        self.output_path = self.rawout_path + "/" + self.match[4]

        if self.match[4] in ["lung", "rectum", "stomach", "breast", "liver"]:
            self.panel_type = self.match[4] + "_roche"
        if self.match[4] in ["gene77", "roche929"]:
            self.panel_type = self.match[4]

    def capture_analysis(self):
        if self.data_type == "cfdna":
            cfdnaIndex, cfdnaR1, cfdnaR2 = sorted(filter(lambda x: "".join([self.match[1], "cfdna"]) in x, os.listdir("./")))
            cfdna_prefix = re.match(r"(.+)(cfdna)(.+)", cfdnaIndex).group(1) + "cfdna"
            if len(filter(lambda x: self.match[1] in x, os.listdir("./"))) == 6:
                gdnaIndex, gdnaR1, gdnaR2 = sorted(filter(lambda x: "".join([self.match[1], "gdna"]) in x, os.listdir("./")))
                gdna_prefix = cfdnaIndex.split("cfdna")[0] + "gdna"
                os.system("python /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/ctdna_normal_hualiao.py -1 %s -2 %s -m %s -3 %s -4 %s -n %s -c %s -b /haplox/users/longrw/ref_data/bed/%s.bed -e /haplox/users/longrw/ref_data/bed/exon/%s.bed -o %s > %s/%s.o 2>&1" % (gdnaR1, gdnaR2, gdna_prefix, cfdnaR1, cfdnaR2, cfdna_prefix, self.panel_type, self.panel_type, self.panel_type, self.output_path, self.output_path, cfdna_prefix))

        if self.data_type in ["ffpedna", "pedna", "fnadna"]:
            dnaIndex, dnaR1, dnaR2 = sorted(filter(lambda x: "".join([self.match[1], self.data_type]) in x, os.listdir("./")))
            dna_prefix = dnaIndex.split(self.data_type)[0] + self.data_type
            os.system("python /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/ffpe_picard_dedup_gatk_hualiao.py -1 %s -2 %s -n %s -c %s -b /haplox/users/longrw/ref_data/bed/%s.bed -e /haplox/users/longrw/ref_data/bed/exon/%s.bed -o %s > %s/%s.o 2>&1" % (dnaR1, dnaR2, dna_prefix, self.panel_type, self.panel_type, self.panel_type, self.output_path, self.output_path, dna_prefix))

def all_analysis(seq):
    sample = Seq(seq)
    sample.capture_analysis()

def main():
    # deal with path
    rawseq_path = os.path.abspath("./")
    rawfq_path = rawseq_path.replace("rawseq", "rawfq")
    rawout_path = rawseq_path.replace("rawseq", "rawout")
    if not os.path.exists(rawout_path):
        os.mkdir(rawout_path)
    output_path_lst = list()
    cov_path_lst = list()
    # bcl2fastq
    time1 = time.time()
    os.system("bcl2fastq -r 72 -d 72 -p 72 -w 72 -o " + rawfq_path + " --use-bases-mask Y*n,I6,Y*n --tiles s_[2-3] --create-fastq-for-index-reads --barcode-mismatches=0")
    os.chdir(rawfq_path)
    time2 = time.time()
    os.system("python /tools/after/after.py --store_overlap=on")
    os.chdir("good")
    time3 = time.time()
    # filter files and mkdir new folders
    flst = filter(lambda x: re.match(pattern, x), os.listdir("./"))
    panel_types = set(map(lambda x: re.search(r"lung|gene77|roche929|rectum|stomach|breast|liver", x).group(), flst))
    bed_types = map(lambda x: x + "_roche" if x in ["lung", "rectum", "stomach", "breast", "liver"] else x, panel_types)
    for panel_type in panel_types:
        output_path = rawout_path + "/" + panel_type
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        output_path_lst.append(output_path)
    # parallel
    p = Pool(6)
    p.map(all_analysis, flst)
    p.close()
    p.join()
    time4 = time.time()
    print '################################ Pipeline Information ##############################################'
    print 'Rawseq path: %s\nRawfq path: %s\nRawout path: %s' % (rawseq_path,rawfq_path,rawout_path)
    print 'Bcl2fastq time used: %s' % str(time2 - time1)
    print 'After time used: %s' % str(time3 - time2)
    print 'Analysis time used: %s' % str(time4 - time3)

if __name__ == "__main__":
    main()

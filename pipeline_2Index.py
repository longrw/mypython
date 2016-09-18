#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    File name: pipeline.py
    Date created: 4/20/2016
    Date last modified: 8/25/2016
    Please put this file in rawseq folder
"""

import os
import re
from multiprocessing import Pool
import logging
from optparse import OptionParser

pattern = re.compile(r'(^S\d+)[-_](.+)[-_](cfdna|ffpedna|pedna|fnadna|saldna|tisdna)[-_](lung[-_]roche|gene77|roche929|rectum[-_]roche|stomach[-_]roche|breast[-_]roche|liver[-_]roche|pan[-_]cancer[-_]v1|genome|exons[-_]roche)(.+)(R1_001.good.fq|R1_001.fastq.gz|R1_001.fastq)$')

def parse_cmd():
    usage = 
    version = 
    parser = OptionParser(usage=usage, version=version)
    parser.add_option()#rawseq dir
    parser.add_option()#Samplesheet.csv dir
    parser.add_option()#Lane No.
    parser.add_option()#2Index fqsamplesheet.csv dir
    parser.add_option()#outdir
    return parser.parse_args()

def after(Rs):
    os.system("pypy /tools/after/after.py -1 {0} -2 {1} --store_overlap=on".format(Rs[0], Rs[1]))
    logging.info("\nAfter CMD: pypy /tools/after/after.py -1 {0} -2 {1} --store_overlap=on\n{2}".format(Rs[0], Rs[1],"#"*50))
    os.system("python /tools/after/after.py -1 {0} -2 {1} --qc_only".format(Rs[0], Rs[1]))
    logging.info("\nAfterQC CMD: python /tools/after/after.py -1 {0} -2 {1} --qc_only\n{2}".format(Rs[0], Rs[1],"#"*50))

class Seq:
    def __init__(self, raw_name):
        self.rawfq_path = os.path.abspath("./")
        self.rawout_path = self.rawfq_path.replace("rawfq", "rawout")
        self.rawname = raw_name
        self.match = re.match(pattern, self.rawname).groups()
        self.sample_type = self.match[2]
        self.output_path = self.rawout_path + "/" + self.match[0]
        self.panel_type = self.match[3]
        self.panel_type_all = self.panel_type.replace('-', '_')

    def capture_analysis(self):
        if self.sample_type == "cfdna":
            cfdnaR1 = self.rawname
            cfdnaR2 = self.rawname.replace('R1','R2')
            gdnaR1 = ''.join(filter(lambda x: re.match(r'(^S\d+)[-_]'+self.match[1]+'[-_]gdna[-_]'+self.panel_type+'(.+)(R1_001.fastq.gz|R1_001.fastq)$', x), os.listdir("./")))
            gdnaR2 = ''.join(filter(lambda x: re.match(r'(^S\d+)[-_]'+self.match[1]+'[-_]gdna[-_]'+self.panel_type+'(.+)(R2_001.fastq.gz|R2_001.fastq)$', x), os.listdir("./")))
            if os.path.exists(cfdnaR1) and os.path.exists(cfdnaR2) and os.path.exists(gdnaR1) and os.path.exists(gdnaR2):
                Rs = [(cfdnaR1, cfdnaR2), (gdnaR1, gdnaR2)]
                p = Pool()
                p.map(after, Rs)
                p.close()
                p.join()
            cfdnaR1_good = self.rawfq_path + '/good/' + cfdnaR1.split('.')[0] + '.good.fq'
            cfdnaR2_good = self.rawfq_path + '/good/' + cfdnaR2.split('.')[0] + '.good.fq'
            gdnaR1_good = self.rawfq_path + '/good/' + gdnaR1.split('.')[0] + '.good.fq'
            gdnaR2_good = self.rawfq_path + '/good/' + gdnaR2.split('.')[0] + '.good.fq'
            cfdna_prefix = self.match[0] + "_cfdna"
            gdna_prefix = cfdna_prefix.replace('cfdna', 'gdna')
            if os.path.exists(cfdnaR1_good) and os.path.exists(cfdnaR2_good) and os.path.exists(gdnaR1_good) and os.path.exists(gdnaR2_good):
                if not os.path.exists(self.output_path):
                    os.mkdir(self.output_path)
                os.system("python /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/ctdna_normal_chemo.py -1 %s -2 %s -m %s -3 %s -4 %s -n %s -c %s -b /haplox/users/longrw/ref_data/bed/%s.bed -e /haplox/users/longrw/ref_data/bed/exon/%s.bed -o %s > %s/%s.out 2>&1" % (gdnaR1_good, gdnaR2_good, gdna_prefix, cfdnaR1_good, cfdnaR2_good, cfdna_prefix, self.panel_type_all, self.panel_type_all, self.panel_type_all, self.output_path, self.output_path, cfdna_prefix))
                logging.info("\npython /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/ctdna_normal_chemo.py -1 {0} -2 {1} -m {2} -3 {3} -4 {4} -n {5} -c {6} -b /haplox/users/longrw/ref_data/bed/{7}.bed -e /haplox/users/longrw/ref_data/bed/exon/{8}.bed -o {9} > {10}/{11}.out 2>&1\n{12}".format(gdnaR1_good,gdnaR2_good,gdna_prefix,cfdnaR1_good,cfdnaR2_good,cfdna_prefix,self.panel_type_all,self.panel_type_all,self.panel_type_all,self.output_path,self.output_path,cfdna_prefix,"#"*50))

        if self.sample_type in ["ffpedna", "pedna", "fnadna", "saldna", "tisdna"]:
            dnaR1 = self.rawname
            dnaR2 = self.rawname.replace('R1','R2')
            if os.path.exists(dnaR1) and os.path.exists(dnaR2):
                after((dnaR1, dnaR2))
            dnaR1_good = self.rawfq_path + '/good/' + dnaR1.split('.')[0] + '.good.fq'
            dnaR2_good = self.rawfq_path + '/good/' + dnaR2.split('.')[0] + '.good.fq'
            dna_prefix = self.match[0]
            if os.path.exists(dnaR1_good) and os.path.exists(dnaR2_good):
                if not os.path.exists(self.output_path):
                    os.mkdir(self.output_path)
                os.system("python /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/single_mutant_pe.py -1 %s -2 %s -n %s -c %s -b /haplox/users/longrw/ref_data/bed/%s.bed -e /haplox/users/longrw/ref_data/bed/exon/%s.bed -o %s > %s/%s.out 2>&1" % (dnaR1_good, dnaR2_good, dna_prefix, self.panel_type_all, self.panel_type_all, self.panel_type_all, self.output_path, self.output_path, dna_prefix))
                logging.info("\npython /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/single_mutant_pe.py -1 {0} -2 {1} -n {2} -c {3} -b /haplox/users/longrw/ref_data/bed/{4}.bed -e /haplox/users/longrw/ref_data/bed/exon/{5}.bed -o {6} > {7}/{8}.out 2>&1\n{9}".format(dnaR1_good,dnaR2_good,dna_prefix,self.panel_type_all,self.panel_type_all,self.panel_type_all,self.output_path,self.output_path,dna_prefix,"#"*50))

def all_analysis(seq):
    sample = Seq(seq)
    sample.capture_analysis()

def main():
    log = "./pipeline_RunInfo.log"
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename=log, filemode='w')
    # deal with path
    rawseq_path = os.path.abspath("./")
    rawfq_path = rawseq_path.replace("rawseq", "rawfq")
    rawout_path = rawseq_path.replace("rawseq", "rawout")
    if not os.path.exists(rawout_path):
        os.mkdir(rawout_path)
    logging.info("\nRawseq path: {0}\nRawfq  path: {1}\nRawout path: {2}\n{3}".format(rawseq_path,rawfq_path,rawout_path,"#"*50))
    # bcl2fastq
    if 'NS500713' in rawseq_path:
        os.system("bcl2fastq -r 72 -d 72 -p 72 -w 72 -o " + rawfq_path + " --barcode-mismatches=0 --no-lane-splitting")
        logging.info("\nBcl2fastq CMD: bcl2fastq -r 72 -d 72 -p 72 -w 72 -o {0} --barcode-mismatches=0 --no-lane-splitting\n{1}".format(rawfq_path,"#"*50))
    if 'ST-E' in rawseq_path:
        os.system("bcl2fastq -r 72 -d 72 -p 72 -w 72 -o " + rawfq_path + " --tiles s_7 --barcode-mismatches=0")
        logging.info("\nBcl2fastq CMD: bcl2fastq -r 72 -d 72 -p 72 -w 72 -o {0} --tiles s_7 --barcode-mismatches=0\n{1}".format(rawfq_path,"#"*50))
    os.chdir(rawfq_path)
    double_index = '{0}/fqsamplesheet.csv'.format(rawseq_path)
    if os.path.exists(double_index):
        os.system("/haplox/users/longrw/myC/FastqSplit/fqsplit -i {0}/fqsamplesheet.csv -1 Undetermined_S0_R1_001.fastq.gz -2 Undetermined_S0_R2_001.fastq.gz -o {1}".format(rawseq_path,rawfq_path))
        logging.info("\nFastqSplit CMD: /haplox/users/longrw/myC/FastqSplit/fqsplit -i {0}/fqsamplesheet.csv -1 Undetermined_S0_R1_001.fastq.gz -2 Undetermined_S0_R2_001.fastq.gz -o {1}\n{2}".format(rawseq_path,rawfq_path,"#"*50))
    # filter files and mkdir new folders
    flst = filter(lambda x: re.match(pattern, x), os.listdir("./"))
    logging.info("\nflst ={0}\n{1}".format(flst,"#"*50))
    # parallel
    p = Pool(6)
    p.map(all_analysis, flst)
    p.close()
    p.join()
    # after again
    os.chdir(rawfq_path)
    r1_lst = filter(lambda x: re.match(r'(^S\d+)(.+)(_R1)(_001.fastq|_001.fastq.gz)', x), os.listdir("./"))
    r1_good_lst = filter(lambda x: re.match(r'(^S\d+)(.+)(_R1)(_001.good.fq|_001.good.fq.gz)', x), os.listdir("./good"))
    r1_good_lst_ID = [f.split('.')[0] for f in r1_good_lst]
    rs = []
    for r1 in r1_lst:
        if r1.split('.')[0] not in r1_good_lst_ID:
            r2 = r1.replace('R1','R2')
            rs.append((r1,r2))
    a = Pool()
    a.map(after, rs)
    a.close()
    a.join()
    # single sampleQC
#    os.system("python /haplox/users/longrw/mypython/single_sampleQC.py -1 ")
    logging.info("\n{0}".format('The great pipeline has been successful!!!\n'*3))

if __name__ == "__main__":
    main()

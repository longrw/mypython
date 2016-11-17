#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from multiprocessing import Pool
import logging
from optparse import OptionParser

pattern = re.compile(r'(^S\d+)[-_](.+)[-_](cfdna|ffpedna|pedna|fnadna|saldna|ttdna|gdnahealth|cfdnahealth|urinedna)[-_](lung[-_]roche|gene77|roche929|rectum[-_]roche|stomach[-_]roche|breast[-_]roche|liver[-_]roche|pan[-_]cancer[-_]v1|genome|exons[-_]roche)(.+)(R1_001.good.fq|R1_001.fastq.gz|R1_001.fastq)$')


def parse_cmd():
    usage = '\nCMD: python %prog <-1 rawseq_path> <-2 rawfq_path> <-3 cleanfq_path> <-4 rawout_path> <-5 file_path> <-s lane_start> <-e lane_end>'
    version = '%prog 0.1.0'
    parser = OptionParser(usage=usage, version=version)
    parser.add_option('-1', '--rawseq_path', dest='rawseq_path', default=None, help='the rawseq path')
    parser.add_option('-2', '--rawfq_path', dest='rawfq_path', default=None, help='the rawfq path')
    parser.add_option('-3', '--cleanfq_path', dest='cleanfq_path', default=None, help='the cleanfq path')
    parser.add_option('-4', '--rawout_path', dest='rawout_path', default=None, help='the rawout path')
    parser.add_option('-5', '--file_path', dest='file_path', default=None, help='the input files path')
    parser.add_option('-s', '--lane_start', dest='lane_start', default=None, help='the start lane ID')
    parser.add_option('-e', '--lane_end', dest='lane_end', default=None, help='the end lane ID')
    return parser.parse_args()


def multi_process(func, args, np=""):
    p = Pool(np)
    p.map(func, args)
    p.close()
    p.join()


def bcl2fastq(rawseq, files, rawfq, lane_s, lane_e):
    samplesheet = os.path.join(files, "SampleSheet.csv")
    if 'NS500713' in rawseq:
        os.system("bcl2fastq_v2_18 -r 72 -d 72 -p 72 -w 72 -R %s --sample-sheet %s -o %s --barcode-mismatches=0 --no-lane-splitting" % (rawseq, samplesheet, rawfq))
        logging.info("\nBcl2fastq CMD: bcl2fastq_v2_18 -r 72 -d 72 -p 72 -w 72 -R %s --sample-sheet %s -o %s --barcode-mismatches=0 --no-lane-splitting\n%s" % (rawseq, samplesheet, rawfq, "#"*50))
    if 'ST-E' in rawseq:
        if lane_s and lane_e:
            tiles = "s_[{0}-{1}]".format(lane_s, lane_e)
        else:
            tiles = "s_{0}".format(lane_s)
        os.system("bcl2fastq_v2_18 -r 72 -d 72 -p 72 -w 72 -R %s --sample-sheet %s -o %s --tiles %s --barcode-mismatches=0" % (rawseq, samplesheet, rawfq, tiles))
        logging.info("\nBcl2fastq CMD: bcl2fastq_v2_18 -r 72 -d 72 -p 72 -w 72 -R %s --sample-sheet %s -o %s --tiles %s --barcode-mismatches=0\n%s" % (rawseq, samplesheet, rawfq, tiles, "#"*50))


def fqsplit(index, inpath, outpath):
    num_S = filter(lambda x: re.match(r'(^S\d+)(.+)(_001.fastq|_001.fastq.gz)', x), os.listdir(inpath))
    if not num_S:
        undetermined_pattern = re.compile(r'Undetermined(.+)(_R1_001.fastq.gz|_R1_001.fastq)')
        undetermined_files = filter(lambda x: re.match(undetermined_pattern, x), os.listdir(inpath))
        for r1 in undetermined_files:
            r2 = r1.replace("R1", "R2")
            os.system("/haplox/users/longrw/myC/FastqSplit/fqsplit -i %s -1 %s -2 %s -o %s" % (index, r1, r2, outpath))
            logging.info("\nFastqSplit CMD: /haplox/users/longrw/myC/FastqSplit/fqsplit -i %s -1 %s -2 %s -o %s\n%s" % (index, r1, r2, rawfq, "#"*50))


def flsts_filter(pattern, directory):
    fls = filter(lambda x: re.match(pattern, x), os.listdir(directory))
    return fls


def after(Rs):
    os.system("pypy /tools/after/after.py -1 %s -2 %s -g %s --no_overlap" % (Rs[0], Rs[1], Rs[2]))
    logging.info("\nAfter CMD: pypy /tools/after/after.py -1 %s -2 %s -g %s --no_overlap\n%s" 
            % (Rs[0], Rs[1], Rs[2], "#"*50))


class Snv(object):
    def __init__(self, rawfq, raw_name):
        self.rawfq_path = rawfq
        self.rawout_path = self.rawfq_path.replace('rawfq','rawout')
        self.cleanfq_path = self.rawfq_path.replace('rawfq','cleanfq')
        self.good_path = self.cleanfq_path + "/good"
        self.rawname = raw_name
        self.match = re.match(pattern, self.rawname).groups()
        self.sample_type = self.match[2]
        self.output_path = self.rawout_path + "/" + self.match[0]
        self.panel_type = self.match[3]
        self.panel_type_all = self.panel_type.replace('-', '_')

    def cfdna2gdna_after(self):
        cfdnaR1 = self.rawname
        cfdnaR2 = self.rawname.replace('R1','R2')
        pattern_r1 = re.compile(
                r'(^S\d+)[-_]'+self.match[1]+'[-_]gdna[-_]'+self.panel_type+
                '(.+)(R1_001.fastq.gz|R1_001.fastq)$')
        gdnaR1 = ''.join(filter(lambda x: re.match(pattern_r1, x), os.listdir(self.rawfq_path)))
        pattern_r2 = re.compile(
                r'(^S\d+)[-_]'+self.match[1]+'[-_]gdna[-_]'+self.panel_type+
                '(.+)(R2_001.fastq.gz|R2_001.fastq)$')
        gdnaR2 = ''.join(filter(lambda x: re.match(pattern_r2, x), os.listdir(self.rawfq_path)))
        if (os.path.exists(cfdnaR1) and os.path.exists(cfdnaR2) 
                and os.path.exists(gdnaR1) and os.path.exists(gdnaR2)):
            Rs = [(cfdnaR1, cfdnaR2, self.good_path), (gdnaR1, gdnaR2, self.good_path)]
            multi_process(after, Rs)
        return cfdnaR1,cfdnaR2,gdnaR1,gdnaR2

    def cfdna2gdna_analysis(self):
        dna = self.cfdna2gdna_after()
        cfdnaR1_good = self.good_path + "/" + dna[0].split('.')[0] + '.good.fq'
        cfdnaR2_good = self.good_path + "/" + dna[1].split('.')[0] + '.good.fq'
        gdnaR1_good = self.good_path + "/" + dna[2].split('.')[0] + '.good.fq'
        gdnaR2_good = self.good_path + "/" + dna[3].split('.')[0] + '.good.fq'
        cfdna_prefix = self.match[0] + "_cfdna"
        gdna_prefix = cfdna_prefix.replace('cfdna', 'gdna')
        if (os.path.exists(cfdnaR1_good) and os.path.exists(cfdnaR2_good) 
                and os.path.exists(gdnaR1_good) and os.path.exists(gdnaR2_good)):
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
            os.system( "python /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/ctdna_normal_chemo.py -1 %s -2 %s -m %s -3 %s -4 %s -n %s -c %s -b /haplox/users/longrw/ref_data/bed/%s.bed -e /haplox/users/longrw/ref_data/bed/exon/%s.bed -o %s > %s/%s.out 2>&1" % (gdnaR1_good, gdnaR2_good, gdna_prefix, cfdnaR1_good, cfdnaR2_good, cfdna_prefix, self.panel_type_all, self.panel_type_all, self.panel_type_all, self.output_path, self.output_path, cfdna_prefix))
            logging.info("\npython /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/ctdna_normal_chemo.py -1 %s -2 %s -m %s -3 %s -4 %s -n %s -c %s -b /haplox/users/longrw/ref_data/bed/%s.bed -e /haplox/users/longrw/ref_data/bed/exon/%s.bed -o %s > %s/%s.out 2>&1\n%s" % (gdnaR1_good, gdnaR2_good, gdna_prefix, cfdnaR1_good, cfdnaR2_good, cfdna_prefix, self.panel_type_all, self.panel_type_all, self.panel_type_all, self.output_path, self.output_path, cfdna_prefix, "#"*50))

    def ffpe_after(self):
        dnaR1 = self.rawname
        dnaR2 = self.rawname.replace('R1','R2')
        if os.path.exists(dnaR1) and os.path.exists(dnaR2):
            after((dnaR1, dnaR2, self.good_path))
        return dnaR1,dnaR2

    def ffpe_analysis(self):
        dna = ffpe_after()
        dnaR1_good = self.good_path + "/" + dna[0].split('.')[0] + '.good.fq'
        dnaR2_good = self.good_path + "/" + dna[1].split('.')[0] + '.good.fq'
        dna_prefix = self.match[0]
        if os.path.exists(dnaR1_good) and os.path.exists(dnaR2_good):
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
            os.system("python /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/single_mutant_pe.py -1 %s -2 %s -n %s -c %s -b /haplox/users/longrw/ref_data/bed/%s.bed -e /haplox/users/longrw/ref_data/bed/exon/%s.bed -o %s > %s/%s.out 2>&1" % (dnaR1_good, dnaR2_good, dna_prefix, self.panel_type_all, self.panel_type_all, self.panel_type_all, self.output_path, self.output_path, dna_prefix))
            logging.info("\npython /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/single_mutant_pe.py -1 %s -2 %s -n %s -c %s -b /haplox/users/longrw/ref_data/bed/%s.bed -e /haplox/users/longrw/ref_data/bed/exon/%s.bed -o %s > %s/%s.out 2>&1\n%s" % (dnaR1_good, dnaR2_good, dna_prefix, self.panel_type_all, self.panel_type_all, self.panel_type_all, self.output_path, self.output_path, dna_prefix, "#"*50))

    def health_analysis(self):
        dna = ffpe_after()
        gdnahealthR1_good = self.good_path + "/" + dna[0].split('.')[0] + '.good.fq'
        gdnahealthR2_good = self.good_path + "/" + dna[1].split('.')[0] + '.good.fq'
        gdnahealth_prefix = self.match[0]
        if os.path.exists(gdnahealthR1_good) and os.path.exists(gdnahealthR2_good):
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
            germline_output = os.path.join(self.output_path, "germline")
            if not os.path.exists(germline_output):
                os.makedirs(germline_output)
            os.system("perl /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/Target_pipeline.pl -t 10 -fq1 %s -fq2 %s -outdir %s -keyname %s -L /haplox/users/longrw/ref_data/bed/%s.bed" % (gdnahealthR1_good, gdnahealthR2_good, germline_output, gdnahealth_prefix, self.panel_type_all))
            logging.info("\nperl /haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/Target_pipeline.pl -t 10 -fq1 %s -fq2 %s -outdir %s -keyname %s -L /haplox/users/longrw/ref_data/bed/%s.bed\n%s" % (gdnahealthR1_good, gdnahealthR2_good, germline_output, gdnahealth_prefix, self.panel_type_all, "#"*50))


def all_analysis((rawfq, f)):
    sample = Snv(rawfq, f)
    if sample.sample_type == "cfdna":
        sample.cfdna2gdna_analysis()
    if sample.sample_type in ["ffpedna", "pedna", "fnadna", "saldna", "ttdna", "urinedna"]:
        sample.ffpe_analysis()
    if sample.sample_type == "gdnahealth":
        sample.health_analysis()


def after_again(rawfq, cleanfq):
    good_dir = os.path.join(cleanfq, "good")
    if not os.path.exists(good_dir):
        os.makedirs(good_dir)
    pattern_r1_lst = re.compile(r'(^S\d+)(.+)(_R1)(_001.fastq|_001.fastq.gz)')
    r1_lst = filter(lambda x: re.match(pattern_r1_lst, x), os.listdir(rawfq))
    pattern_r1_good_lst = re.compile(r'(^S\d+)(.+)(_R1)(_001.good.fq|_001.good.fq.gz)')
    r1_good_lst = filter(lambda x: re.match(pattern_r1_good_lst, x), os.listdir(good_dir))
    r1_good_lst_ID = [f.split('.')[0] for f in r1_good_lst]
    rs = []
    for r1 in r1_lst:
        if r1.split('.')[0] not in r1_good_lst_ID:
            r2 = r1.replace('R1','R2')
            rs.append((r1, r2, good_dir))
    multi_process(after, rs)


def single_sampleQC(files, rawfq):
    estimated_yield = os.path.join(files, "estimated_yield.csv")
    yield_ID = os.path.basename(rawfq)
    os.system("python /haplox/users/longrw/mypython/single_sampleQC.py -1 %s -2 %s -3 %s -o %s" % (rawfq, estimated_yield, yield_ID, files))
    logging.info("\nsingle_sampleQC CMD:python /haplox/users/longrw/mypython/single_sampleQC.py -1 %s -2 %s -3 %s -o %s\n%s" % (rawfq, estimated_yield, yield_ID, files, "#"*50))


def main():
    (options, args) = parse_cmd()
    # deal with dir
    rawseq = options.rawseq_path
    if rawseq == None:
        rawseq = os.path.abspath("./")
    rawfq = options.rawfq_path
    if rawfq == None:
        rawfq = rawseq.replace("rawseq", "rawfq")
    if not os.path.exists(rawfq):
        os.makedirs(rawfq)
    rawout = options.rawout_path
    if rawout == None:
        rawout = rawseq.replace("rawseq", "rawout")
    if not os.path.exists(rawout):
        os.makedirs(rawout)
    cleanfq = options.cleanfq_path
    if cleanfq == None:
        cleanfq = rawseq.replace("rawseq", "cleanfq")
    if not os.path.exists(cleanfq):
        os.makedirs(cleanfq)
    files = options.file_path
    if files == None:
        files = rawseq
    log = os.path.join(files, "pipeline_RunInfo.log")
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', 
            datefmt='%a, %d %b %Y %H:%M:%S', filename=log, filemode='a')
    logging.info(
            "\nRawseq path: %s\nRawfq  path: %s\nCleanfq path: %s\nRawout path: %s\nRuninfo path: %s\n%s" % 
            (rawseq, rawfq, cleanfq, rawout, files, "#"*50))
    # bcl2fastq
    lane_s = options.lane_start
    lane_e = options.lane_end
    bcl2fastq(rawseq, files, rawfq, lane_s, lane_e)
    index = os.path.join(files, "fqsamplesheet.csv")
    fqsplit(index, rawfq, rawfq)
    # filter files and mkdir new folders
    os.chdir(rawfq)
    flsts = flsts_filter(pattern, rawfq)
    logging.info("\nflsts =%s\n%s" % (flsts, "#"*50))
    # parallel
    args_analysis = []
    for flst in flsts:
        args_analysis.append((rawfq, flst))
    multi_process(all_analysis, args_analysis, 6)
    # single sampleQC
    single_sampleQC(files, rawfq)
    # after again
    after_again(rawfq, cleanfq)
    logging.info("\n{0}".format('The great pipeline has been successful!!!\n'*3))


if __name__ == "__main__":
    main()
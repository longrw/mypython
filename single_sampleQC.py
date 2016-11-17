#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from multiprocessing import Pool
from optparse import OptionParser
import time

pattern = re.compile(r'(^S\d+)(.+)(_R1|_R2)(_001.fastq|_001.fastq.gz)')

def parse_cmd():
    usage = 'Quality Control for Illumina raw fastq reads data\nCMD: python %prog <-1 rawfq_path> <-2 estimated_yield> <-3 png_ID>'
    version = '%prog 1.0'
    parser = OptionParser(usage=usage, version=version)
    parser.add_option('-1', '--rawfq_path', dest = 'rawfq_path', default = None, help = 'the rawfq path')
    parser.add_option('-2', '--estimated_yield', dest = 'estimated_yield', default = None, help = 'the estimated yield data')
    parser.add_option('-3', '--png_ID', dest = 'png_ID', default = None, help = 'ID for png of estimated_VS_real_yield')
    parser.add_option('-o', '--output', dest = 'output', default = None, help = 'output dir')
    return parser.parse_args()

def single_sampleQC(f):
    f_match = re.match(pattern, f).groups()
    qc = '{0}/{1}{2}_qc.txt'.format(outpath,f_match[0],f_match[2])
    if not os.path.exists(qc):
        os.system("/haplox/users/longrw/myC/qc_Code_hy/qc {0} > {1}".format(f, qc))

def estimated_vs_real_yield(csv, outpath, png_ID):
    os.system("Rscript /haplox/users/longrw/myR/humanVSsequencer_yield.R {0} {1} {2}".format(csv, outpath, png_ID))

def q30_GC(qc_csv, png_ID):
    png_q30 = '{0}/{1}_q30.png'.format(outpath, png_ID)
    if not os.path.exists(png_q30):
        os.system("Rscript /haplox/users/longrw/myR/Q30.R {0} {1} {2}".format(qc_csv, png_q30, png_ID))

def CfdnaPattern(inpath):
    CfdnaPattern = '{0}/CfdnaPattern.txt'.format(outpath)
    fqgz = filter(lambda x: re.match(r'(^S\d+)(.+)(_001.fastq.gz)$', x), os.listdir(inpath))
    fq = filter(lambda x: re.match(r'(^S\d+)(.+)(_001.fastq)$', x), os.listdir(inpath))
    if fqgz:
        fs = '.fastq.gz'
    elif fq:
        fs = '.fastq'
    os.system("python /tools/CfdnaPattern/predict.py -q {0}/S*{1} > {2}".format(inpath, fs, CfdnaPattern))

def Undetermined_2Index(inpath):
    fs = filter(lambda x: re.match(r'Undetermined(.+)R1(.+)', x), os.listdir(inpath))
    for f in fs:
        fp = '{0}/{1}'.format(inpath, f)
        if os.path.exists(fp):
            os.system("python /haplox/users/longrw/mypython/Undetermined_2Index_top20.py {0} {1}".format(fp,outpath))

def main():
    time1 = time.time()
    (options, args) = parse_cmd()
    #dir
    global outpath
    outpath = '{0}/single_sampleQC'.format(options.output)
    if options.output == None:outpath = '{0}/single_sampleQC'.format(options.rawfq_path)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    #CfdnaPattern
    os.chdir(options.output)
    CfdnaPattern(options.rawfq_path)
    os.chdir(options.rawfq_path)
    #qc.txt
    flst = sorted(filter(lambda x: re.match(pattern, x), os.listdir('./')))
    p = Pool(30)
    p.map(single_sampleQC, flst)
    p.close()
    p.join()
    #qc.csv header: ID,read_number,base_number,base_number_Q20,base_number_Q30,Q20,Q30,A,T,C,G,N,GC_content,estimated_yield,real_yield
    os.chdir(outpath)
    fs = sorted(filter(lambda x: x.endswith('_qc.txt'), os.listdir('./')))
    qc_csv = '{0}/qc.csv'.format(outpath)
    if os.path.exists(qc_csv):
        os.remove(qc_csv)
    csv_out = open(qc_csv, 'a')
    for f in fs:
        info = []
        f_lst = f.split('_')
        ID = f_lst[0] + '_' + f_lst[1]
        info.append(ID)
        for line1 in open(f):
            x = line1.strip().split('\t')[1]
            info.append(x)
        for line2 in open(options.estimated_yield):
            line2_lst = line2.strip().split(',')
            if f_lst[0] in line2_lst[0]:
                y = float(line2_lst[1])/2
                info.append(y)
        real_yield = float(info[2])/1024**3
        info.append(real_yield)
        qc_info = ','.join(map(lambda x: str(x),info))
        csv_out.write(qc_info + '\n')
    csv_out.close()
    #qc.png
    estimated_vs_real_yield(qc_csv, outpath, options.png_ID)
    q30_GC(qc_csv, options.png_ID)
    #Undetermined_2Index
    os.chdir(options.output)
    Undetermined_2Index(options.rawfq_path)
    #time used
    time2 = time.time()
    print('Time used: {0}'.format(str(time2-time1)))

if __name__ == "__main__":
    main()

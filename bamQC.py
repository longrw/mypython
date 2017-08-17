#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
from multiprocessing import Pool

def bam(args):
    (inpath, bed, exonbed, t, ref, R1, R2, sampleID, outpath) = (args[0],
            args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8])
    sam = "%s/%s.sam" % (inpath,sampleID)
    bam_sort = "%s/%s_sort.bam" % (inpath,sampleID)
    bam_mark = "%s/%s_mark.bam" % (inpath,sampleID)
    cov_sort = "%s/%s_sort.txt" % (outpath,sampleID)
    cov_mark = "%s/%s_mark.txt" % (outpath,sampleID)
    mapq_value = "%s/%s_mapq.txt" % (outpath,sampleID)
    temp_len = "%s/%s_templen.txt" % (outpath,sampleID)
    map_sort = "%s/%s_sort.maptxt" % (outpath,sampleID)
    map_mark = "%s/%s_mark.maptxt" % (outpath,sampleID)
    stats = "%s/%s_stats.txt" % (outpath,sampleID)
    read_len = "%s/%s_readlen.txt" % (outpath,sampleID)
    AGCT_content = "%s/%s_AGCT.txt" % (outpath,sampleID)
    capture_sort = "{0}/{1}_sort_capture_stat.txt".format(outpath,sampleID)
    capture_mark = "{0}/{1}_mark_capture_stat.txt".format(outpath,sampleID)
    if not os.path.exists(bam_sort):
        os.system("bwa mem -t %s %s %s %s > %s" % (t,ref,R1,R2,sam))
        os.system("java -Xmx10g -jar /tools/GATK/picard/SortSam.jar INPUT=%s OUTPUT=%s SORT_ORDER=coordinate" % (sam,bam_sort))
        os.system("samtools index %s" % bam_sort)
    if not os.path.exists(bam_mark):
        os.system("/haplox/users/huang/mypy/data-analysis/ctdna_exome_pipeline/dedup.py -1 %s -o %s" % (bam_sort,bam_mark))
        os.system("samtools index %s" % bam_mark)
    if not os.path.exists(cov_mark):
        os.system("bedtools coverage -d -abam %s -b %s > %s" % (bam_sort,exonbed,cov_sort))
        os.system("bedtools coverage -d -abam %s -b %s > %s" % (bam_mark,exonbed,cov_mark))
    if not os.path.exists(mapq_value):
        os.system("samtools view %s | cut -f 5 > %s" % (bam_sort,mapq_value))
        os.system("samtools view %s | cut -f 9 > %s" % (bam_mark,temp_len))
    if not os.path.exists(map_mark):
        os.system("samtools flagstat %s > %s" % (bam_sort,map_sort))
        os.system("samtools flagstat %s > %s" % (bam_mark,map_mark))
    if not os.path.exists(read_len):
        os.system("samtools stats -r %s %s > %s" % (ref,bam_sort,stats))
        os.system("grep 'RL' %s | cut -f 2- > %s" % (stats,read_len))
        os.system("grep 'GCC' %s | cut -f 2- > %s" % (stats,AGCT_content))
    if not os.path.exists(capture_sort and capture_mark):
        os.system("pypy /haplox/users/longrw/mypython/check_capture_percentage.py -b {0} -i {1} -o {2}".format(bed,bam_sort,outpath))
        os.system("pypy /haplox/users/longrw/mypython/check_capture_percentage.py -b {0} -i {1} -o {2}".format(bed,bam_mark,outpath))

def cfdna2gdna():
    (inpath, bed, exonbed, t, ref, gR1, gR2, gID, cfR1, cfR2, cfID) = (sys.argv[1],
            sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],
            sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
#    bamQC_dir = "%s/BamQC" % inpath
#    if not os.path.exists(bamQC_dir):os.mkdir(bamQC_dir)
    if len(sys.argv) == 13:
        outpath = sys.argv[12]
    else:
        outpath = "{0}/BamQC".format(inpath)
    if not os.path.exists(outpath):os.mkdir(outpath)
    argss = [(inpath,bed,exonbed,t,ref,gR1,gR2,gID,outpath), (inpath,bed,exonbed,t,ref,cfR1,cfR2,cfID,outpath)]
    p = Pool()
    p.map(bam, argss)
    p.close()
    p.join()
#    bam(inpath,bed,exonbed,t,ref,gR1,gR2,gID,outpath)
#    bam(inpath,bed,exonbed,t,ref,cfR1,cfR2,cfID,outpath)
    gdna_sort_cov = "%s/%s_sort.txt" % (outpath,gID)
    gdna_mark_cov = "%s/%s_mark.txt" % (outpath,gID)
    cfdna_sort_cov = "%s/%s_sort.txt" % (outpath,cfID)
    cfdna_mark_cov = "%s/%s_mark.txt" % (outpath,cfID)
    cfdna_mapq_value = "%s/%s_mapq.txt" % (outpath,cfID)
    gdna_mapq_value = "%s/%s_mapq.txt" % (outpath,gID)
    cfdna_templen = "%s/%s_templen.txt" % (outpath,cfID)
    gdna_templen = "%s/%s_templen.txt" % (outpath,gID)
    gdna_sort_map = "%s/%s_sort.maptxt" % (outpath,gID)
    gdna_mark_map = "%s/%s_mark.maptxt" % (outpath,gID)
    cfdna_sort_map = "%s/%s_sort.maptxt" % (outpath,cfID)
    cfdna_mark_map = "%s/%s_mark.maptxt" % (outpath,cfID)
    gdna_read_content = "{0}/{1}_AGCT.txt".format(outpath,gID)
    cfdna_read_content = "{0}/{1}_AGCT.txt".format(outpath,cfID)
    cov_info = "%s/covInfo.csv" % outpath
    mapq_png = "%s/mapping_quality_distribution-MAPQ.png" % outpath
    templen_png = "%s/template_length_distribution.png" % outpath
    map_info = "%s/mapInfo.csv" % outpath
    gene_target_list = "/haplox/users/longrw/myR/files/gene_target_list.txt"
    gene_target_points = "/haplox/users/longrw/myR/files/gene_target_points.txt"
    os.system("Rscript /haplox/users/longrw/myR/cov_group_exon.R %s %s %s %s" % (exonbed,gene_target_points,gene_target_list,outpath))
    os.system("python /haplox/users/longrw/mypython/cov.py %s %s %s %s > %s" % (gdna_sort_cov,gdna_mark_cov,cfdna_sort_cov,cfdna_mark_cov,cov_info))
    os.system("Rscript /haplox/users/longrw/myR/depth_cov.R %s %s" % (outpath,cfID.split('_')[0]))
    os.system("Rscript /haplox/users/longrw/myR/mapq.R %s %s %s" % (cfdna_mapq_value,gdna_mapq_value,mapq_png))
    os.system("Rscript /haplox/users/longrw/myR/template_length.R %s %s %s" % (cfdna_templen,gdna_templen,templen_png))
    os.system("python /haplox/users/longrw/mypython/flagstat.py %s %s %s %s > %s" % (gdna_sort_map,gdna_mark_map,cfdna_sort_map,cfdna_mark_map,map_info))
    os.system("Rscript /haplox/users/longrw/myR/read_content.R {0} {1} {2}".format(outpath,gID,gdna_read_content))
    os.system("Rscript /haplox/users/longrw/myR/read_content.R {0} {1} {2}".format(outpath,cfID,cfdna_read_content))
    os.system("python /haplox/users/longrw/mypython/bamQCreport.py %s > %s/bamQCreport.html" % (outpath,outpath))

    os.system("rm -rf %s/*_mapq.txt" % outpath)
    os.system("rm -rf %s/*_templen.txt" % outpath)

def ffpe():
    (inpath,bed,exonbed,t,ref,R1,R2,sampleID) = (sys.argv[1],
            sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8])
#    bamQC_dir = "%s/BamQC" % inpath
#    if not os.path.exists(bamQC_dir):os.mkdir(bamQC_dir)
    if len(sys.argv) == 10:
        outpath = sys.argv[9]
    else:
        outpath = "{0}/BamQC".format(inpath)
    if not os.path.exists(outpath):os.mkdir(outpath)
    bam((inpath,bed,exonbed,t,ref,R1,R2,sampleID,outpath))
    cov_sort = "%s/%s_sort.txt" % (outpath,sampleID)
    cov_mark = "%s/%s_mark.txt" % (outpath,sampleID)
    mapq_value = "%s/%s_mapq.txt" % (outpath,sampleID)
    temp_len = "%s/%s_templen.txt" % (outpath,sampleID)
    map_sort = "%s/%s_sort.maptxt" % (outpath,sampleID)
    map_mark = "%s/%s_mark.maptxt" % (outpath,sampleID)
    read_content = "{0}/{1}_AGCT.txt".format(outpath,sampleID)
    cov_info = "%s/covInfo.csv" % outpath
    mapq_png = "%s/mapping_quality_distribution-MAPQ.png" % outpath
    templen_png = "%s/template_length_distribution.png" % outpath
    map_info = "%s/mapInfo.csv" % outpath
    gene_target_points = "/haplox/users/longrw/myR/files/gene_target_points.txt"
    gene_target_list = "/haplox/users/longrw/myR/files/gene_target_list.txt"
    os.system("Rscript /haplox/users/longrw/myR/cov_group_exon.R %s %s %s %s" % (exonbed,gene_target_points,gene_target_list,outpath))
    os.system("python /haplox/users/longrw/mypython/cov_ffpe.py %s %s > %s" % (cov_sort,cov_mark,cov_info))
    os.system("Rscript /haplox/users/longrw/myR/depth_cov_ffpe.R %s %s" % (outpath,sampleID))
    os.system("Rscript /haplox/users/longrw/myR/mapq_ffpe.R %s %s" % (mapq_value,mapq_png))
    os.system("Rscript /haplox/users/longrw/myR/template_length_ffpe.R %s %s" % (temp_len,templen_png))
    os.system("python /haplox/users/longrw/mypython/flagstat_ffpe.py %s %s > %s" % (map_sort,map_mark,map_info))
    os.system("Rscript /haplox/users/longrw/myR/read_content.R {0} {1} {2}".format(outpath,sampleID,read_content))
    os.system("python /haplox/users/longrw/mypython/bamQCreport_ffpe.py %s > %s/bamQCreport.html" % (outpath,outpath))

    os.system("rm -rf %s/*_mapq.txt" % outpath)
    os.system("rm -rf %s/*_templen.txt" % outpath)

if __name__ == "__main__":
    if len(sys.argv) >= 12:
        cfdna2gdna()
    else:
        ffpe()

#!/usr/bin/perl

my $in = $ARGV[0];
#print $in."\n";
#exit;
my @res = `find $in  -name "*.pileup"`;
push @res, `find $in  -name "*.sam"`;
push @res, `find $in  -name "*_mark.bam"`;
push @res, `find $in  -name "*_rg_new.bam"`;
push @res, `find $in  -name "*_baserecal.bam"`;
push @res, `find $in  -name "*_Realn.bam"`;

#my @res = `find /haplox/rawout/160401  -name "*.sam"`;
#my @res = `find /haplox/rawout/160401  -name "*_mark.bam"`;
#print @res;
#exit;
foreach $i (@res){
    `rm -f $i`;
}


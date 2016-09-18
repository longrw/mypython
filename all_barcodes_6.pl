#!/usr/bin/perl
use strict;
use warnings;

my $index_all=shift;
my $index_number=shift;#your sample index number
#my $out=shift;#samplesheet.csv
my $date_csv=shift;#output file
my %hash;

open INDEX, "< $index_all" or die $!;
while (<INDEX>){
    chomp;
    next if (/^$/);
    my @barcode=split(/,/);
    $hash{$barcode[0]}=$barcode[1];
}

open NO, "< $index_number" or die $!;
while (<NO>){
    chomp;
    next if (/^$/);
    my @date_NO=split(/,/);
    my $date=$date_NO[0];
    my $n=$date_NO[1];
    #open OUT1, ">> $out" or die $!;
    open OUT2, ">> $date_csv" or die $!;
    if (exists $hash{$n}){
        #print OUT1 "$n,$hash{$n}\n";
        #print OUT2 "$n,$hash{$n}\n";

        my @index_6=split(//,$hash{$n});
        my $m="$index_6[0]$index_6[1]$index_6[2]$index_6[3]$index_6[4]$index_6[5]";
        #print OUT1 "$n,$m\n";
        print OUT2 "$date,$date,,,$n,$m,,,,\n"
    }else{
        print OUT2 "$n,error index!\n";
    }
    close OUT2;
}
close INDEX;
close NO;


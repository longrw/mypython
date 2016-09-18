#!/usr/bin/perl
use strict;
use warnings;
use threads;
use PerlIO::gzip;
my $fq1=shift;
my $fq2=shift;
my (%hash,$a,$b,@tmp1,@tmp2,@tmp3,@tmp4,$i,$j);
my $syn1 = async {
#        open FQ1, "< $fq1" or die $!;
	open(FQ1,"gzip -dc $fq1|") or die ("can not open $fq1\n");
	while(<FQ1>){
                chomp;
		next if (/^$/);
		$a=$_;
                @tmp1=split(/:/,$a);
		@tmp2=split(//,$tmp1[9]);
		$i="$tmp2[0]$tmp2[1]$tmp2[2]$tmp2[3]$tmp2[4]$tmp2[5]";
		if(exists $hash{$i}){
			open OUT1, ">> $i\_1.fq" or die $!;
			print OUT1 "$a\n";
			$a=<FQ1>;
			chomp($a);
			print OUT1 "$a\n";
			$a=<FQ1>;
			chomp($a);
			print OUT1 "$a\n";
			$a=<FQ1>;
			chomp($a);
			print OUT1 "$a\n";
			close OUT1;					
		}else{
			$hash{$i}=0;
			open OUT1, ">> $i\_1.fq" or die $!;
                        print OUT1 "$a\n";
                        $a=<FQ1>;
                        chomp($a);
                        print OUT1 "$a\n";
                        $a=<FQ1>;
                        chomp($a);
                        print OUT1 "$a\n";
                        $a=<FQ1>;
                        chomp($a);
                        print OUT1 "$a\n";
                        close OUT1;
			}
        }
return 0;
};




my $syn2 = async {
#        open FQ2, "< $fq2" or die $!;
	open(FQ2,"gzip -dc $fq2|") or die ("can not open $fq2\n");
	while(<FQ2>){
                chomp;
                next if (/^$/);
		$b=$_;
                @tmp3=split(/:/,$b);
		@tmp4=split(//,$tmp3[9]);
		$j="$tmp4[0]$tmp4[1]$tmp4[2]$tmp4[3]$tmp4[4]$tmp4[5]";
		if(exists $hash{$j}){
			open OUT2, ">> $j\_2.fq" or die $!;
			print OUT2 "$b\n";
			$b=<FQ2>;
			chomp($b);
			print OUT2 "$b\n";
			$b=<FQ2>;
			chomp($b);
			print OUT2 "$b\n";
			$b=<FQ2>;
			chomp($b);
			print OUT2 "$b\n";
			close OUT2;					
		}else{
			$hash{$j}=0;
			open OUT2, ">> $j\_2.fq" or die $!;
                        print OUT2 "$b\n";
                        $b=<FQ2>;
                        chomp($b);
                        print OUT2 "$b\n";
                        $b=<FQ2>;
                        chomp($b);
                        print OUT2 "$b\n";
                        $b=<FQ2>;
                        chomp($b);
                        print OUT2 "$b\n";
                        close OUT2;


			}
        }
return 0;
};

if ( $syn1->join() == 0 && $syn2->join() == 0) {
        exit 0;
}

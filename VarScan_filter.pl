#!/usr/bin/perl -w
use strict;
my ($anp_anno,$indel_anno,$snp_file,$indel_file) = @ARGV;

=head1 Usage

	perl VarScan_filter.pl <snp_annovar_txt> <indel_annovar_txt> <snp_file> <indel_file>

=cut

die `pod2text $0` if (@ARGV != 4);
open FL,"/haplox/users/ZhouYQ/Database/Gene_transcript.list" or die $!;
my %genetran;
my %tran_info;
while(<FL>){
        chomp;
        my @arr = split/\t/;
        $genetran{$arr[0]} = $arr[1];
        $tran_info{$arr[0]} = $arr[2];
}
close FL;

open FL,"$anp_anno";
open FLS,">$snp_file";
my $title = <FL>;
print "$title";
my %hash;
while(<FL>){
	chomp;
	$_ =~ s/%//g;
	my @arr = split/\t/;
	my @zrr = split/\:/,$arr[-1];
	my @yrr = split/\:/,$arr[-2];
	my @xrr = split/\,/,$arr[-1];
	my $read_support = $zrr[4];
	my $normal_support = $yrr[4];
	my $tumor_depth = $zrr[2];
	my $normal_depth = $yrr[2];
	my $tumor_AF = $zrr[5];
	my $normal_AF = $yrr[5];
	$_ =~ /\;SSC=(\d+)\;/;
	my $SSC = $1;
	next unless($_ =~ /SOMATIC/ && $_ =~ /SS=2/);
	my $strand_bias1 = $xrr[-1]/$read_support;
        my $strand_bias2 = $xrr[-2]/$read_support;
        next if(($strand_bias1 < 0.1 || $strand_bias2 < 0.1) && $read_support >= 8);
	next unless($SSC > 12);
	next unless($arr[5] eq "exonic" || $arr[5] eq "splicing");
	next if($arr[8] eq "synonymous SNV" || $arr[8] eq "UNKNOWN");
	next unless($read_support >= 4 && $tumor_AF >= 0.5);
	next unless(($normal_support <= 3 && $normal_AF < 0.3) || ($normal_AF < 1 && $tumor_AF >= 5 && $read_support >= 20));
	next unless($tumor_depth >= 150 && $normal_depth >= 100);
	next unless(exists $genetran{$arr[6]});
	next if(($arr[12] ne "." && $arr[12] !~ /E-/ && $arr[12] >= 0.005) || ($arr[13] ne "." && $arr[13] !~ /E-/ && $arr[13] >= 0.005) || ($arr[14] ne "." && $arr[14] !~ /E-/ && $arr[14] >= 0.005) || ($arr[15] ne "." && $arr[15] !~ /E-/ && $arr[15] >= 0.005) || ($arr[16] ne "." && $arr[16] !~ /E-/ && $arr[16] >= 0.005));
	print "$_\n";
	my $cosmid;
        if($arr[43] =~ /ID=COSM/){
                my @crr = split/;/,$arr[43];
                $crr[0] =~ s/ID=//;
                $cosmid = $crr[0];
        }else{
                $cosmid = "NA";
        }
	if($arr[5] eq "splicing" && $arr[7] ne "."){
                my @crr = split/,/,$arr[7];
                my ($tran,$exon,$nt_change) = split/:/,$crr[0];
                for my $anno_line(@crr){
                        my @drr = split/\:/,$anno_line;
                        next unless(exists $genetran{$arr[6]} && $genetran{$arr[6]} eq $drr[0]);
                        ($tran,$exon,$nt_change) = split/\:/,$anno_line;
                }
                $exon =~ s/exon//;
                my $intron;
                if($nt_change =~ /c\.(\d+)(\-|\+)(\d+)/){
                        if($2 eq "+" && $tran_info{$arr[6]} eq "+"){
                                $intron = "intron$exon";
                        }elsif($2 eq "-" && $tran_info{$arr[6]} eq "+"){
                                $exon--;
                                $intron = "intron$exon";
                        }elsif($2 eq "+" && $tran_info{$arr[6]} eq "-"){
                                $exon--;
                                $intron = "intron$exon";
                        }elsif($2 eq "-" && $tran_info{$arr[6]} eq "-"){
                                $exon--;$exon--;
                                $intron = "intron$exon";
                        }
                }
                my $annotation = "$arr[0]\t$arr[1]\t$arr[3]\t$arr[4]\t$arr[6]\t$tran\t$intron\t$nt_change\tnil\t$tumor_AF\t$cosmid";
                print FLS "$annotation\n";
        }
	next if($arr[5] eq "splicing");
	my @crr = split/,/,$arr[9];
        my ($gene,$tran,$region,$nt_change,$aa_change) = split/:/,$crr[0];
        for my $anno(@crr){
                my @drr = split/:/,$anno;
                next unless(exists $genetran{$drr[0]} && $genetran{$drr[0]} eq $drr[1]);
                ($gene,$tran,$region,$nt_change,$aa_change) = split/:/,$anno;
        }
        my $annotation = "$arr[0]\t$arr[1]\t$arr[3]\t$arr[4]\t$gene\t$tran\t$region\t$nt_change\t$aa_change\t$tumor_AF\t$cosmid";
        print FLS "$annotation\n";
}
close FL;
close FLS;
open FL,"$indel_anno";
open FLS,">$indel_file";
<FL>;
while(<FL>){
	chomp;
        $_ =~ s/%//g;
	my @arr = split/\t/;
	my @zrr = split/\:/,$arr[-1];
        my @yrr = split/\:/,$arr[-2];
        my @xrr = split/\,/,$arr[-1];
        my $read_support = $zrr[4];
        my $normal_support = $yrr[4];
        my $tumor_depth = $zrr[2];
        my $normal_depth = $yrr[2];
        my $tumor_AF = $zrr[5];
        my $normal_AF = $yrr[5];
        $_ =~ /\;SSC=(\d+)\;/;
        my $SSC = $1;
	next unless($_ =~ /SOMATIC/ && $_ =~ /SS=2/);
	my $strand_bias1 = $xrr[-1]/$read_support;
	my $strand_bias2 = $xrr[-2]/$read_support;
	next if(($strand_bias1 < 0.1 || $strand_bias2 < 0.1) && $read_support >= 8);
        next unless($SSC >= 12);
	next unless($arr[5] eq "exonic" || $arr[5] eq "splicing");
	next unless($read_support >= 4 && $tumor_AF >= 0.5);
	next unless(($normal_support <= 1 && $normal_AF < 0.3) || ($normal_AF < 1 && $tumor_AF >= 5 && $read_support >= 20));
	next unless($tumor_depth >= 150 && $normal_depth > 100);
	next unless(exists $genetran{$arr[6]});
	next if(($arr[12] ne "." && $arr[12] !~ /E-/ && $arr[12] >= 0.005) || ($arr[13] ne "." && $arr[13] !~ /E-/ && $arr[13] >= 0.005) || ($arr[14] ne "." && $arr[14] !~ /E-/ && $arr[14] >= 0.005) || ($arr[15] ne "." && $arr[15] !~ /E-/ && $arr[15] >= 0.005) || ($arr[16] ne "." && $arr[16] !~ /E-/ && $arr[16] >= 0.005));
	print "$_\n";
	my $cosmid;
        if($arr[43] =~ /ID=COSM/){
                my @crr = split/;/,$arr[43];
                $crr[0] =~ s/ID=//;
                $cosmid = $crr[0];
        }else{
                $cosmid = "NA";
        }
        if($arr[5] eq "splicing" && $arr[7] ne "."){
                my @crr = split/,/,$arr[7];
                my ($tran,$exon,$nt_change) = split/:/,$crr[0];
                for my $anno_line(@crr){
                        my @drr = split/\:/,$anno_line;
                        next unless(exists $genetran{$arr[6]} && $genetran{$arr[6]} eq $drr[0]);
                        ($tran,$exon,$nt_change) = split/\:/,$anno_line;
                }
                $exon =~ s/exon//;
                my $intron;
                if($nt_change =~ /c\.(\d+)(\-|\+)(\d+)/){
                        if($2 eq "+" && $tran_info{$arr[6]} eq "+"){
                                $intron = "intron$exon";
                        }elsif($2 eq "-" && $tran_info{$arr[6]} eq "+"){
                                $exon--;
                                $intron = "intron$exon";
                        }elsif($2 eq "+" && $tran_info{$arr[6]} eq "-"){
                                $exon--;
                                $intron = "intron$exon";
                        }elsif($2 eq "-" && $tran_info{$arr[6]} eq "-"){
                                $exon--;$exon--;
                                $intron = "intron$exon";
                        }
                }
                my $annotation = "$arr[0]\t$arr[1]\t$arr[3]\t$arr[4]\t$arr[6]\t$tran\t$intron\t$nt_change\tnil\t$tumor_AF\t$cosmid";
                print FLS "$annotation\n";
        }
	next if($arr[5] eq "splicing");
        my @crr = split/,/,$arr[9];
        my ($gene,$tran,$region,$nt_change,$aa_change) = split/:/,$crr[0];
        for my $anno(@crr){
                my @drr = split/:/,$anno;
                next unless(exists $genetran{$drr[0]} && $genetran{$drr[0]} eq $drr[1]);
                ($gene,$tran,$region,$nt_change,$aa_change) = split/:/,$anno;
        }
        my $annotation = "$arr[0]\t$arr[1]\t$arr[3]\t$arr[4]\t$gene\t$tran\t$region\t$nt_change\t$aa_change\t$tumor_AF\t$cosmid";
        print FLS "$annotation\n";
}
close FL;
close FLS;

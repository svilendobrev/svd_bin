#!/usr/bin/perl
#line totaller - format:lines file
undef $/;       #whole file at a time
while(<>){
 $c = y/\n//;
 $cc = s/\n\n/\n\n/g;        #empty lines
 $c -= $cc;
 $ff{$ARGV} = $c;
 $n = $ARGV; $n =~ s,[/\\][^/\\]+$,,;
 $fdirs{$n} += $c;
 $tot += $c;
}
foreach $k (sort keys %ff) { printf "%5ld : $k\n", $ff{$k}; }
print "\ntot: $tot\n";
foreach $k (sort keys %fdirs) { printf "%5ld : $k\n", $fdirs{$k}; }

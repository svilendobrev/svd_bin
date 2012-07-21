#!/bin/perl

while (<>) {

if (/^MLK/) {
 $x=1; $mlk++; $mleak='';
}
$x=0 if /^(\s+main|\s*Purify Heap Analysis)/;	#stop recording on main() or 1st non-function
$mleak.=$_ if $x && !/^MLK/;

$y=1 if /\* command-line/i; $y=0 if /\* options/i;
$hdr.=$_ if $y;

$z=1 if /\* program exited/i;
if (/\* \d+ bytes potentially/i) {
  $z=0;
  print $tail if ($mlk) ;
  $mlk=0; $hdr= $tail='';
  $leaks{$mleak}++;
 }

$tail.=$_ if $z;

if ($x && $hdr ne '') { print "-------\n$hdr"; $hdr=''; }
print if $x;

}

print "\n\n========== totals: ========\n";
foreach $k (keys %leaks) {
 print "$leaks{$k} times:\n$k"; $n++;
}
print "==== $n =====\n";

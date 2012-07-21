#!/usr/bin/perl
# find which suburb is phone from - requires a table
# to include it somewhere assign $IN=phonetablefile
# and set $included=1 to not expect args
#SvD mar'99

if ($IN eq '') {
  $IN = $ARGV[0]; if ($IN =~ /^\D/) { shift; } else { $IN = $0; }
}
open(IN) || die "$! $IN";
while (<IN>) {
 if (/^#%%%%/) { $on++; next; }
 next if !$on;
 s/^#//g; chop;
 ($patrn,@name) = split(/ +/);
 print "!dup $_" if defined $pat{$patrn};
 $pat{$patrn} = join(' ',@name);
}
#print "$#pat loaded $IN\n";

sub phone {
  local($f) = @_;
  local($n) = 0;
  foreach $p (keys %pat) {
    if ($f =~ /^$p/) { $n++; print "\n$f: $p:" if !$nodbg; print "{ $pat{$p} }"; }
  }
  if (!$n) {
  foreach $p (keys %pat) {
    if ($f =~/^$p*/) { $n++; print "\n$f: $p:" if !$nodbg; print "{ $pat{$p} }"; }
  } }
}
if (!$included) {
  die "give-me phonenum\n" if $#ARGV<0;
  &phone($ARGV[0]);
}
1;      #ret value

#in form of: simple regexp's;
# supply minimum required start digits
# sorry, no globbing (e.g. 123* is here, but 1234 is there)
#%%%%%%%%%%%%%%
#300            aaabk           all that start with 300
#3101           bjkjka
#311[01]        iopiopp         all that start with 3110 or 3111
#316[01]        iopiopp
#32[025-8]      bjkjka          all that start with 320 or 322 or 325 ... 328
#321            pppp
#323[0-24-9]    qqqqq
#4233           ioio
#424[0-79]      iopiopp
#4248           qwqwqw

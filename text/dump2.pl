#!/usr/bin/perl
$BIT7=0;
$X=8;
$D='~';
$IN1 = shift;
$IN2 = shift;
open(IN1) || die "$! $IN1";
open(IN2) || die "$! $IN2";
while (($l1= read(IN1,$bu1, $X))>0 | ($l2= read(IN2,$bu2, $X))>0) {
   next if $bu1 eq $bu2;

   for ($i=0; $i<$l1; $i++) {
        printf( "%s%02x", (substr($bu1,$i,1) eq substr($bu2,$i,1) ? ' ': $D), ord(substr($bu1,$i,1))); }
   for (; $i<$X; $i++) { print "   "; }
   $bf = $bu1;
   $bf =~ y/\x80-\xFF/./ if $BIT7; $bf =~ y/\x00-\x1F/./; printf " | %8.8s",$bf;
   print " # ";
   for ($i=0; $i<$l2; $i++) {
        printf( "%s%02x", (substr($bu1,$i,1) eq substr($bu2,$i,1) ? ' ': $D), ord(substr($bu2,$i,1))); }
   for (; $i<$X; $i++) { print "   "; }
   $bu2=~ y/\x80-\xFF/./ if $BIT7; $bu2=~ y/\x00-\x1F/./; print " | $bu2\n";
}

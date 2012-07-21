#!/usr/bin/perl
#$Id: cmp2.pl,v 1.2 2006-12-06 12:26:12 sdobrev Exp $

$X=8;
$D='>';
$IN1 = shift;
$IN2 = shift;
open(IN1) || die "$! $IN1";
open(IN2) || die "$! $IN2";
binmode(IN1);
binmode(IN2);

sub makeline {
    local($bu1, $bu2, $ofs) = @_;
    local($l1) = length($bu1);
    local($l2) = length($bu2);
    local($line) = sprintf( "%07x ", $ofs);
    for ($i=0; $i<$l1; $i++) { $line.= sprintf( "%s%02x", ((substr($bu1,$i,1) eq substr($bu2,$i,1)) ? ' ': $D), ord(substr($bu1,$i))); }
    for (; $i<$X; $i++) { $line.= "   "; }
    $bf = $bu1;
    $bf =~ y/\000-\037/./; $line.= sprintf( "| %8.8s", $bf);
    $line.= " # ";
    for ($i=0; $i<$l2; $i++) { $line.= sprintf( "%s%02x", ((substr($bu1,$i,1) eq substr($bu2,$i,1)) ? ' ': $D), ord(substr($bu2,$i))); }
    for (; $i<$X; $i++) { $line.= "   "; }
    $bu2 =~ y/\000-\037/./; $line.= "| $bu2\n";
    $line;
}

$last_b1 = $last_b2 = '';
$ofs=0;
$ofsdiff=-1;
while (($l1= read(IN1,$bu1, $X))>0 | ($l2= read(IN2,$bu2, $X))>0) {
    $lastdiff = $diff;
    $diff = ($bu1 ne $bu2);
    if ($diff) {
        print ' '.&makeline( $last_b1, $last_b2, $ofs-$X)
                if $ofs && $ofsdiff>=0 && $ofsdiff!=$ofs-$X;    #context-prev
        print '>'.&makeline( $bu1, $bu2, $ofs);
        $ofsdiff = $ofs;
    }
    if (!$diff && $lastdiff) {  #context-next
        print ' '.&makeline( $bu1, $bu2, $ofs);
        $lastdiff=0;
    }
    $ofs += $X;
    $last_b1 = $bu1;
    $last_b2 = $bu2;
}
if ($lastdiff) {    #context-last
    print ' '.&makeline( $l1, $l2);
}
# vim:ts=4:sw=4:expandtab

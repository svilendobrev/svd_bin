#!/usr/bin/perl 
$IN="global.dat";
open(IN) or die "$! $IN";
$f=join("|",@ARGV); 
print $f.'\n'; 
while (<IN>) {
 $k[$n++]=$_; if ($n==3) { print @k if $k[1]!~m,($f),; $n=0;}
}

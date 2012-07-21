#!/usr/bin/perl

$HTML = 0;
if ($ARGV[0] =~ /^-htm/i) { shift; $HTML=-1; }

# remove the ^0x40 for html %XX
@hx=(0,1,2,3,4,5,6,7,8,9, 'a','b','c','d','e','f', 'A','B','C','D','E','F');
for ($i=0; $i<16+6; $i++) {
 for ($j=0; $j<16+6; $j++) {
	$r = (16*($i>=16?$i-6:$i)+ ($j>=16?$j-6:$j) );
  $tx_rtf{$hx[$i].$hx[$j]} = sprintf("%c", $r ^ 0x40);
  $tx_htm{$hx[$i].$hx[$j]} = sprintf("%c", $r);
}}
#foreach $k (sort keys %tx) { print "$k=$tx{$k}\n"; }

while (<>) {
 s/\\pard *\{ *//go;
 s/\\par *\}* */\n     /go;
 s/\\[^']+[{; ]//go;
 s/\\[^']+\\/\\/go;
 s/\\[^']+\n/\n/go; chop;
 if ($HTML>=0) { $HTML = ($ARGV =~ /.html?/i); }
 %tx = $HTML ? %tx_htm : %tx_rtf;
# print $HTML, 'a', $tx{"33"}, "b\n";
#s/\\'([\da-fA-F]+)/sprintf("%c",0x40 ^ hex $1)/ego;
 s/(\\'|%)([0-9a-fA-F]+)/$tx{$2}/ge;      # html decoding too
 print;
}

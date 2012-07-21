#!/usr/bin/perl
$IN = shift;
open(IN) || die "$! $IN";
while (($l = read(IN,$buf, 16))>0) {
   printf "%05x: ", $ofs; $ofs += $l;
   for ($i=0; $i<$l; $i++) {
  	 printf( "%02x ", ord(substr($buf,$i)));
   }
   for (; $i<16; $i++) {
	 print "   ";
   }
   print "| ";
	$buf =~ y/\000-\037/./;
	print "$buf\n";
}

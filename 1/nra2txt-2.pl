#!/usr/bin/perl
#dump nero-burning-rome .nra files. const hdr + records of varsize fields

$IN = shift;
open(IN) || die "$! $IN";
binmode(IN);

$l = read(IN,$buf, 0x30 );      #hdr
while (1) {
   $l = read(IN,$buf, 8 ); last if $l<=0;   #EVAW..

   $l = read(IN,$buf, 4 ); last if $l<=0;
   $szpath = ord( substr($buf, 0,1 ));
   $l = read(IN,$path, $szpath ); last if $l<=0;
   $l = read(IN,$buf, 1 ); last if $l<=0;

   $l = read(IN,$buf, 4 ); last if $l<=0;
   $szfile = ord( substr($buf, 0,1 ));
   $l = read(IN,$file, $szfile ); last if $l<=0;
   $l = read(IN,$buf, 1 ); last if $l<=0;

   $l = read(IN,$buf, 0x221 ); last if $l<=0;

   $l = read(IN,$buf, 4 ); last if $l<=0;
   $szname = ord( substr($buf, 0,1 ));
   $l = read(IN,$name, $szname ); last if $l<=0;
   $l = read(IN,$buf, 1 ); last if $l<=0;

   $l = read(IN,$buf, 4 ); last if $l<=0;
   $sznamu = ord( substr($buf, 0,1 ));
   $l = read(IN,$namu, $sznamu ); last if $l<=0;
   $l = read(IN,$buf, 1 ); last if $l<=0;

   $l = read(IN,$buf, 0x43 ); last if $l<=0;

   $l = read(IN,$filt, 4); last if $l<=0;   #ENON, EDAF, ...
   $l = read(IN,$buf, 1 ); last if $l<=0;
   $sz = ord( substr($buf, 0,1 ));
   $l = read(IN,$buf, $sz -1 ); last if $l<=0;

#  for ($i=0; $i<$l; $i++) { printf( "%02x ", ord(substr($buf,$i))); }
#  for (; $i<16; $i++) { print "   "; }
#  print "| "; $buf =~ y/\000-\037/./; print "$buf\n";

   $file =~ s/\.wav//;
   $n++;
   print (($filt ne "ENON") ? '*' : ' ');
   printf "%2d. ", $n;
   print "$file\n";
}

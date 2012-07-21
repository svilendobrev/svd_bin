#!/bin/perl
##give the set of newsclassifieds-loaded html files to this   #(hack) svd'99
while (<>) {
 $on++ if /ADVERTS BEGIN/;
 $on=0 if /\"bot\"\>/;
 next if m/<P ALIGN=/;
 next if m|/nc20/editorial/pubs/|;
 s/<IMG SRC=\"[^\"]*\" ALT=//i;
 s/BORDER=0 HEIGHT=17>//i;
 s/<font[^>]*>//i;
 s|</font>||i;
 s|</p>||gi;
 print if $on;
}

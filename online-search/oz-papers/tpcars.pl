#!/bin/perl -n
#tradepost's filter

$on1++ if /results\?/;
$on++ if $on1 && / *<table>/i;
if ($on && m/<td/i) {
   s|^[ \t]+||gi;
   s|</*table>||gi;
   s|<td[^>]*>||gi;
   s|<IMG[^>]*>||gi;
   s|<font[^>]*>||gi;
   s|</font>||gi; s|</td>||gi; s|<br>||gi;
   s|<b>|\n  |gi; s|</b>||gi;
   s|<i><a href[^>]*>.+</i>||gi;
#  s|^<a href[^>]*>||gi;
#  s|</a>||i;         #1st only
#  s|</a>|**</a>|i;   #2nd only
#all:
   s|<a href[^>]*>||gi; s|</a>||gi;
   print;
}
$on=$on1=0 if $on && m|</table>|i;

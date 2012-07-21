#!/usr/bin/perl
## (c) SvD '99
# given a file with gcc warnings-messages to avoid, this will filter them out

#$DBG=1;
$IN=shift;
open(IN) || die "$!; avoidance file:$IN";
(@avoid) = <IN>;
close(IN);

while (<>) {
   $inxx = /^In file included from/ || /: In (method|function) / || /: At top level:/ ;
   if ($inxx && $x ne '' && !$infile) { print "a1-: $infile " if $DBG; print $x; $x=''; }
   $infile += $inxx;	#count nesting as one (see above)
   $x .= $_;# if $infile;
   next if $inxx;
   if (/^[^: ]+:\d+:/) {
     $infile = 0;
     $av=0; foreach $a (@avoid) {
       next if $a =~ /^#/;
       $a=~s/\s+$//; #print "$a--\n" if $DBG;
       last if ($av = /$a/);
     }
     if (!$av) { print "a2-: " if $DBG; print $x; }
     $x = '';
#    print "---\n";
   }
}
if ($x ne '') { print "a3-: " if $DBG; print $x; $x=''; }

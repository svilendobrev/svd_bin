#!/usr/bin/perl
#svd'99
##finds rules that are hanging, i.e. not connected in the grammar
## and subrules (RHS parts) that are not defined

die      "BNFcheck inputfile[s]"
        ."\n - the rule LHS should be on separate line, like"
        ."\n\taa ::="
        ."\n\t  b | c"
        ."\n - if file name conatins 'keyw' somewhere (case-insensitive),"
        ."\n\tit is treated as whitespace separated list of keywords (terminals)\n"
 if $#ARGV<0;

while (<>) {
 if ($ARGV =~ /keyw/i) {
        $keywords .= $_;
 } else {
        if (/::=/) {
          s/[ \t]*::=[ \t\n]*$//;
          $rul{$_} = 1;
        } else {
          $a[$i++]=$_;
        }
 }
}

$keywords =~ s/(\S+)/ $1 /g;    #separate by spaces
$keywords =~ s/\s+/ /g;         #by One space
foreach $word (split(' ', $keywords)) {
  $kw{$word} = 0 if $word !~ /^\s*$/;
}
#print $keywords;

foreach $x (keys %rul) {
  $used=0;
  for ($j=0; $j<=$#a; $j++) {
   next if $a[$j]=~/::=/;
   $used++ if $a[$j]=~/$x/;
  }
  print "not used: $x\n" if !$used;
}
print "\n";

for ($j=0; $j<=$#a; $j++) {
  $_=$a[$j];
  next if /::=/ || /^----/ || /NOTE:/i;
  foreach $wrd (split(/[^\$\w]+/)) {
    $wrd =~ s/\s*//g;
    next if $wrd eq '';
    if (!defined $rul{$wrd}) {
        if (defined $kw{$wrd}) {
                $kw{$wrd}++;
        } else {
                print "not def: $wrd\n" if !$notdef{$wrd}++;
        }
    }
  }
}

if ($#kw) {
 print "\n--keywords not used: \n";
 foreach $wrd (sort keys %kw) {
        print "$wrd\n" if !$kw{$wrd};
 }
 print "\n--keywords used: \n";
 foreach $wrd (sort keys %kw) {
        print "$wrd \t: $kw{$wrd}\n" if $kw{$wrd};
 }
}

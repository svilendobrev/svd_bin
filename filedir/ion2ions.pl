#!/usr/bin/perl
## svd 2'2k
## split single tree descr.ion into path's ones

$IONname = "descript.iom";
die
 "$0 [-options] file[s]"
."\n\tsplit single combined(tree) descript.ion into directory's ones"
."\n\t to combine back, use recursls.pl -f (for flat)"
."\n -doit  : actualy do the overwriting; else just prints for test"
."\n -nfilename : filename to use as $IONname (default)"
."\n"  if $#ARGV <0;

while ($ARGV[0] =~ /^-/) {
   if ($ARGV[0] =~ s/^-doit//) { shift; $DOIT++; }
    elsif
      ($ARGV[0] =~ s/^-n//) { $IONname = shift; print STDERR "*using $IONname\n"; }
}

while (<>) {
  next if /^\s*$/;                              #skip empty lines
  s/^\s+//;
  s/^(\S+)//; $fname = $1; s/^\s+//;
  next if /^\s*$/;                              #skip empty descr lines
  $fname =~ s,(.*[\\/])?([^/\\]+)[/\\]*$,$2,;        #strip tail slash
##s,^(.*[\\/])?(\S+)[/\\]*,$2,; $fname=$2;   #strip tail slash and extract  path
  $path = $1;
# printf "%-20.20s %-20.20s \n"    , $path, $fname;
##print  $_;
  $path  = "./".$path;
  $file{$path} .=  "$fname  \t$_";
}

foreach $path (keys %file) {
  print "---- $path\n";
  if ($DOIT) {
     open(P,">$path/$IONname") || die "$! $path";
     print P $file{$path};
     close(P);
   } else {
     print   $file{$path};
   }
}

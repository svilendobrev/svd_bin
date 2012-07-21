#!/usr/bin/perl
# SvD'1999
# recursive ls into tree-form; alphabet.sort; dir 1st;
# reading descript.ion files if any
# prints name, date, size, total size /total recursive size

$ROUNDshift=10; $ROUND=(1<<$ROUNDshift)-1;
$TRESHOLD=4096;
$IONname = "DESCRIPT.ION";
$LVL=0;
die
 "$0 -options [path]"
."\n -xexcludepattern"
."\n -0  : nolevel0files"
."\n -q  : totals only; if twice: finals only"
."\n -f  : flat find-like tree; no sums/dates"
."\n -nfilename : filename to use as $IONname (default)"
."\n" if $ARGV[0] =~ /^-[h?]/;

while ($ARGV[0] =~ /^-/) {
   if ($ARGV[0] =~ s/^-x//) { $EXCLUDE = shift; print STDERR "*exclude $EXCLUDE\n"; }
    elsif
      ($ARGV[0] =~ s/^-n//) { $IONname = shift; print STDERR "*using   $IONname\n"; }
    elsif
      ($ARGV[0] =~ s/^-0//) { shift; $NOLVL0_FILES++; print STDERR "*exclude level 0 files\n"; }
    elsif
      ($ARGV[0] =~ s/^-q//) { shift; $QUIET++; }
    elsif
      ($ARGV[0] =~ s/^-f//) { shift; $FLAT++; }
    else { last; }
}

sub getdir {
  local($cwd)= $_[0];
  opendir(D,$cwd) || die "$! $cwd";
  local(@dir) = readdir(D); closedir(D);
  local($totsize) =0;
  local($totalsz) =0;   #recursive

  local(%ion);
  local($fname);
  open(ION, "$cwd/$IONname"); # || print "---- cant open $cwd/$IONname : $!\n";
  while(<ION>) {
     s/^\s+//; s/\s+$//;
     s/^(\S+)//; $fname = $1; #print "-$fname-";
     s/^\s+//;
     $fname =~ y/a-z/A-Z/;                #case insensitive
     $ion{$fname} = $_;
   }
  close(ION);
  local($OFS) = (' 'x$LVL);

  foreach $e (sort @dir) {              #dirs only
     next if $e =~ /^\.\.?$/      #skip . and .. ONLY
          || $e =~ /$IONname/i;
     $cur = "$cwd/$e"; $cur =~ s|^\./||;        #kill starting ./
     next if $EXCLUDE ne '' && "$cur/" =~ m|$EXCLUDE|;  #add a slash at the eodirname
     (@statx) = stat($cur);

     $mode = ($statx[2] & 0xF000)==0x3000;
        #printf "--$e $cur: $mode,  %x\n", $statx[2];
     next if !$mode;
        if ($FLAT) { printf "%-40s", "$cur/" if $QUIET<1; } else {
           printf "%-40.40s| ", "$OFS+$cur" if $QUIET<1;
         }

     $e =~ y/a-z/A-Z/;                #case insensitive
     print $ion{$e} if defined($ion{$e}) && $QUIET<1;
     print "\n" if $QUIET<1;

        $LVL++; die "too deep" if $LVL>50;
        $totalsz += &getdir($cur);
        $LVL--;
   }


  if (!$NOLVL0_FILES || $LVL) {
  foreach $e (sort @dir) {              #files only
     next if $e =~ /^\.\.?$/      #skip . and .. ONLY
          || $e =~ /$IONname/i;
     $cur = "$cwd/$e"; $cur =~ s|^\./||;        #kill starting ./
     next if $EXCLUDE ne '' && $cur =~ m|$EXCLUDE|;
     (@statx) = stat($cur);
     $mode = ($statx[2] & 0xF000)==0x3000;
     next if $mode;
     if ($FLAT) { printf "%-39s ", $cur if $QUIET<1; } else {
        $size = $statx[7];
        (@tm) = gmtime($statx[9]);
        printf "%-20.20s %02d.%02d.%04d", $OFS.$e, $tm[3],1+$tm[4], 1900+$tm[5]  if $QUIET<1;
        $totsize+=$size;
        if ($size >= $TRESHOLD) { $size+=$ROUND; $size>>=$ROUNDshift; $size .="k  "; }
        printf "%8s | ", $size if $QUIET<1;
      }
     $e =~ y/a-z/A-Z/;                #case insensitive
     print $ion{$e} if defined($ion{$e}) && $QUIET<1;
     print "\n" if $QUIET<1;
   }
  }
  $totalsz+=$totsize;
# print ('  'x$LVL);
  if (!$FLAT) {
    if ($QUIET<1) { print "$OFS- total " } else { printf "%-20.20s", $cwd; }
    printf " =%8dk", ($totsize+$ROUND)>>$ROUNDshift;
    printf " / %dk", ($totalsz+$ROUND)>>$ROUNDshift if $totsize!=$totalsz;
   }
    print "\n";
  $totalsz;
}

do getdir( $ARGV[0] eq '' ? '.':$ARGV[0] );

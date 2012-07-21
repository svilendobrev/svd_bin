#!/usr/bin/perl
#$Id: chall.pl,v 1.3 2006-01-10 12:28:17 sdobrev Exp $
# SvD'99   changeall.pl, version 2:
# overwriting input files, reading one whole file at a time, hence may
# have memory size limitations AND ^ and $ are not start/end of line but file!
die
 "usage: changeall [-b[inary]] perl-expr-to-apply   files...."
."\n read whole files and OVERWRITES them if matching"
."\n perl_expr's can be almost anything (in quotes)"
."\n  (warning: ^ and $ ARE NOT start and end of line, but of file!)"
."\n -binary    write LF as LF, not CRLF"
."\n -utf8 i/o"
."\n -utf8all expr & i/o"
."\n -loop      apply over and over until no matches"
."\n  ask(strYes,strNo) func available - use as s/whatever/ask(\"..\",$&)/ge"
."\n example: changeall 's/(\d+)/0\\\$1/g' *.c"
."\n      will prefix all numbers with a 0"
 if $#ARGV<1;
use Encode;

shift if ($BIN      = ($ARGV[0] =~ /^--?b(inary)?$/ ));
shift if ($UTF      = ($ARGV[0] =~ /^--?utf8$/      ));
shift if ($UTFall   = ($ARGV[0] =~ /^--?utf8all$/   ));
shift if ($LOOP     = ($ARGV[0] =~ /^--?loop$/      ));

$rexp = shift;
undef $/;       #whole file each time
print "applying --$rexp-- ...\n";
if ($UTFall) {
    print "utf8 expr\n";
    $rexp = encode("UTF-8", decode("cp1251", $rexp));
    $UTF = 1;
    print "applying --$rexp-- ...\n";
}
if ($UTF) {
    print "utf8 i/o\n";
    use open ':encoding(utf8)';
}
#'$k="Кат"; $q=decode("cp1251", $k); $u=encode("UTF-8", $q); s/Cat/$u/'

sub ask {       #ask(yes,no), if no, ret noarg, else ret yesarg
   local($yes) = $_[0]; # the / / below will kill these !
   local($no ) = $_[1];
   local($yn,$r);
   print "$no -> $yes ...?";
   read(STDIN,$yn,2);   #yn+newline - cant make it unbuffered
   $yn =~ s/\s+$//;
   $r = ($yn =~ /^n/i) ? $no : $yes;
   print "$yn: $r\n";
   $r;
}

while (<>) {
  close ARGV;   #if u don't close it, it will come again with wrong contents
  print $ARGV;
  $a = $_;
  $n = 0;
  do {
     $m = 0+eval( "$rexp" );
     $n+=$m;
  } until !$m || !$LOOP;
  #$n = 0+eval( "$rexp" );
  if ($n || $DBG) {
      print "\r> $ARGV :$n             \n";
  } else { print "            \r"; }
  if ($n && $a ne $_) {
    $OUT = ">$ARGV"; open(OUT) || die "$! $OUT";
    binmode(OUT) if $BIN;
    print OUT; close OUT;
  }
}
print "                            \n";
# vim:ts=4:sw=4:expandtab

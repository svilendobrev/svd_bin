#!/usr/bin/perl
# SvD'99   changeall.pl, version 1:
# using tmp directory, reading line by line (no memory size limitations)

$tmp = shift;
die
 "usage: changeall  tmp_prefix  reg-expr  files...."
."\n       will copy/change ALL files into tmp_prefixFilename"
."\n     tmp_prefix can be dir or prefix (avoid overwriting input files :)"
."\n     reg_expr's can contain anything (in quotes)"
."\n example: changeall tmp_dir/ 's/func1\s*\(([^,]+),([^)]+)\)/func2(\$2,\$1)/g' *.c"
."\n      will use func2 with rotated arguments (1st arg's of func1 put as last)"
  if $#ARGV<1 || $tmp eq '' || $tmp eq "./";
$regexp = shift;

print "changing --$regexp-- ...\n";
while (<>) {
  if ($OO ne $ARGV) {
    if ($OO ne '') { close OUT; print " :$n\n"; }
    $OUT=">$tmp$ARGV"; open(OUT) || die "$! $OUT";
    $OO=$ARGV; print "$OO --$OUT";
    $n = 0;     #reset counter
  }
  $n+= eval( $regexp.'o'); print OUT;
}
if ($OO ne '') { close OUT; print " :$n\n"; }

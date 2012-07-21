#!/bin/perl
# parse output table(s) from trace_doc (MIF parser)
# sort them a->b then b->a

while ($TAB= shift) {
 open(TAB) || die "$! $TAB";
 while (<TAB>) { chop; next if /^\s*$/;
  ($sect,$no, $base, $where, $what) = split /\f/;
  next if $base eq '-' || $where eq "Table";	#table ?
  $trace{ join("\f", $base, $where, $what) } = join("\f", $where, $what, $base );
 }
 close(TAB);

 $inname=$TAB; $inname =~ s/(_rtmx.*)*.tab//;
 $wher = '-';
 foreach $_ (sort keys %trace) {
  ($base, $where, $what) = split /\f/;
  print "\nTrace $inname to $where\n---\n" if $where ne $wher; $wher=$where;
  print "$base \t $what\n";
 }
 print "===\n";

 $wher = '-';
 foreach $_ (sort values %trace) {
  ($where, $what, $base) = split /\f/;
  print "\nTrace $where to $inname\n---\n" if $where ne $wher; $wher=$where;
  print "$what \t $base\n";
 }
 print "===\n";
 undef %trace;
}

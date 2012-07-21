#!/usr/bin/perl
$x=shift; die "rename  regexp_to_apply_s/a/b/  file[s]" if $x eq '';
while ($o=$_=shift) {
  if (eval($x)) { print "$o -> $_\n"; rename($o,$_); }
}

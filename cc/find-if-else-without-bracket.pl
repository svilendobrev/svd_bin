if ($ARGV ne $O) {
 $O=$ARGV; $.=1;
}

if ($iff && /^\s*else/) {
  print "$ARGV:$.:---\t$_";
  $iff=0;
}
if ( /if\s*\(.+\)/ && !/{\s*$/ ) {
 $iff=1;
  print "$ARGV:$.:\t$_" if $iff;
}

#undef $/;
#while (<>) {
# if ($ARGV ne $O) {
#   $O=$ARGV; $.=0;
# }
# print "$ARGV:$.:\t$_" if /if\s*\(.+\)/ && !/{\s*$/;
#}

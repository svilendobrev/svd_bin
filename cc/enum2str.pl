#!/usr/bin/perl
## parses c/c++ file for given enums and makes string arrays of the tags
$enumname = shift;
die "enum2str enumnamepattern [-skip=pattern] files\n"
   ."   will ignore c++ comments;\n"
   ."   use \\s* as pattern to get any enum\n"
        if $enumname eq '';

if ($ARGV[0] =~ s/^-skip=//) {       # skip pattern
  $skip = shift;
}
while (<>) {
  next if m,^\s*//,;    #c++ comment
  if (s/enum ($enumname\w*)//) {
        $on++;
        $i=0;
        print "const char * str$1\[\] = {\n";
   }
  next if !$on;
  s/^.*\{//;    #kill enum name and open bracket
  s|//.*\s*$||; #kill c++ comments
if (0) {
  s/^\s*/\"/;
  s/\s*,\s*/\", \"/g;
  if (!s/\s*}\s*;*\s*$/\" };/) { s/\s*$/\"/; }
  s/\"\"//g;
  print; print "\n";
} else {
  s/=[^,]+//;
  foreach $k (split(/[ \t,]/)) {
        $k =~ s/^\s+//; $k =~ s/\s+$//;         #kill lead/trail space
        next if $k=~ /^\s*$/ || $k =~ /$skip/;
        if ($k=~ /\}/) {
                print " };\n"; last; }
        print $i ? ", " : " \t" ; $i++;
        print "\n \t" if ($i & 0xF)==8;
        print "\"$k\"";
  }
}
  $on=0 if /\}/;
}

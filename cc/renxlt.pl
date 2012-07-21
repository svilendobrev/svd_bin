#!/usr/bin/perl
#try to parse   oldfile  newfile  xlat table,
#  and rename acordingly, and generate s/old/new/ regexps
while (<>) {
   last if /^####/;
   chop;
   ($from,$to) = split(/ +/);
   next if $to eq '' || $from eq '';
   rename( $from   ,  $to   );
   rename("$from,v", "$to,v");
   $from =~ s/\./\\./g;
   $to   =~ s/\./\\./g;
   $prl .= "s/$from/$to/g\n";
}
print $prl;

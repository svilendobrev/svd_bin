#!/usr/bin/perl
## svd 8'2k

shift if ($ifdef = ($ARGV[0] =~ /^-ifdef/));
$MY  = shift if !$ifdef; $PFX = shift;

die "outdep.pl -ifdef              prefixpattern1[,..]  [makefiles]"
die "outdep.pl myname[,myname2..]  prefixpattern1[,..]  [makefiles]"
."\n  input/output dependencies builder - list of import/export goodies"
."\n   -ifdef   : take all in between #ifdef OUTDEP ... #endif OUTDEP"
."\n              myname  is the left side name of any assignment, upto first _"
."\n   otherwise: take only ^(myname|myname2|..)\w+.. = ..., everywhere"
."\n  The right side args of assignments, if starting with prefixpattern,"
."\n  are prefixed with P_myname/"
."\n"
."\n  include the result in other makefiles that want to use this dir's goodies"
."\n example: makefile: "
."\n   APP_LIB = \$J/uap.lib  #this is some app"
."\n   KBD_LIBS= \$J/ukb0.obj \$J/ukb.lib"
."\n   UU_LIBS = \$(KBD_LIBS) \$(APP_LIB)"
."\n run: outdep.pl APP,KBD,UU '$$J' makefile > out.dep"
."\n result:"
."\n   APP_LIB = \$P_APP/\$J/uap.lib #this is some app"
."\n   KBD_LIBS= \$P_KBD/\$J/ukb0.obj \$P_KBD/\$J/ukb.lib"
."\n   UU_LIBS = \$(KBD_LIBS) \$(APP_LIB)"

."\n" if $#ARGV <0 || $MY eq '' && !$ifdef
	;

binmode(STDOUT); ## if $BIN; noCRLF's

$MY  =~ s/^\s+//; $MY  =~ s/\s+$//; $MY  =~ y/,/|/;
$PFX =~ s/^\s+//; $PFX =~ s/\s+$//; $PFX =~ y/,/|/;

$MYMY = "($MY)\\w*\\s*=";

# print STDERR "outdep $ARGV[0] > lhs: $MYMY --rhs: $PFX --\n";

while (<>) {
# if ($ifdef) {
	$a=0 if /^#endif/;   #\s+OUTDEP
#   if ($a) {
	if ($a && s,^([0-9a-zA-Z]+)_\w*\s*=\s*, ,
	|| !$ifdef && s,^$MYMY, ,) {    #put one space after the =
##       if (s,^$MYMY, , && ($a || !$ifdef)) {    #put one space after the =
	print $&;
	$my = $1;
	s/(#.*)//;               #strip comments
	s/\s+$//;
	s,\s+($PFX), \$(P_$my)/$1,g if $PFX ne '';
	print "$_\n";
	} else { print if $a; }
#    }
	$a += $ifdef && /^#ifdef\s+OUTDEP/;
#  } else {
#    if ( s,^$MYMY, , ) {        #put one space at start
#        print $&;
#        $my = $1;
###      $c = s/(#.*)// ? $1 : "";       #skip comments
#        s,\s+($PFX), \$(P_$my)/$1,g if $PFX ne '';
#        print "$_\n";
#    }
#  }
}

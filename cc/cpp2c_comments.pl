$dir = shift;
print "using directory: $dir\n";
undef $/;	#whole file at once
while (<>) {
 s,//(.+)(\n|/\*),/*xx $1 */$2,g;
 $ARGV=~s,(\.+/+)+,,g;
 $NAME=">$dir/$ARGV";
 print "saving to $NAME\n";
 open(NAME) || die "$! $NAME";
 print NAME $_;
 close NAME;
}

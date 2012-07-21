#!/usr/bin/perl
$off=0;
$bf='';
while (<>) {
	if ($off && s,^(> )*http://mail.yahoo.com,,) { $off=0; next; }
	if (s/^(> )*Do You Yahoo!\?//) {
		$off=1;
		$bf =~ s/^(> )*_+\s*//;
	}
	next if $off;
	if ($bf ne '') { print $bf; $bf=''; }
	$bf = $_;
}
print $bf if $bf ne '';

#__________________________________________________
#Do You Yahoo!?
#..bullshit-here..
#http://mail.yahoo.com

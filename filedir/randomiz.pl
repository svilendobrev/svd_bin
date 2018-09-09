#!/usr/bin/perl

srand();
opendir(D,".");
@a = readdir(D);

foreach $p (@a) {
   (@statx) = stat($p);
   $mode = $statx[2];
   next if (($mode & ~0xFFF)==0x4000); # directory

    $ext = $p; $ext =~ s/^.*\.//;
    next if $ext =~ /pl/;
    $r = rand();
    $nm = substr($r,2,8);
    rename( $p, "$nm.$ext" );
}

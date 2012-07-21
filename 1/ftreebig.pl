#!/usr/bin/perl

$dot = ".";
$dotdot = "..";
$bar = "|";
$dash = "_";
$nestlevel = 0;
$curnestlevel = 0;

sub list_dirs {
        return if ($curnestlevel > $nestlevel && $nestlevel != 0) ;
        $curnestlevel++;
        local ($curdir, $prevstr, $lastflag) = @_;
        local ($nextstr);
        local ($fullpath);
        local ($file);
        local ($tempdir) = $curdir;
        local ($len, $newlen);
        local (@pathlist);
        local ($islast);
        local ($jun, $size);

        $tempdir =~ /(.*)\//;
        $len =length($1);
        #$newlen = $len-length($prevstr)-1;
        $newlen = 5;
        $nextstr = $prevstr . " " . $bar . $dash x $newlen ;
        $tempdir =~ s/(.*)\//"" x $len /e ;
        if ($firsttime > 0) { $nextstr = " "; $firsttime = 0;}
        print "$nextstr$tempdir";
        $makefilecheck && -f $curdir && (($jun,$jun,$jun,$jun,$jun,$jun,$jun,$size) = stat ($curdir) ) && (print " *($size) \n")&& ($curnestlevel--) && return;
        chdir($curdir) ||  print "   ***** Unable to read / cd $chdir";
        print "\n";

        $curdir =~ s/\/$//;
        local(@filesarray) = `ls -a`;
        if ($curdir =~ /^\./ ) {
                chdir($directory);
        }
        FILE:
        for $file (@filesarray) { chop($file);
                if ($file ne $dot && $file ne $dotdot) {
                        $fullpath = $curdir . "/" . $file;
                        #$makefilecheck && -f $fullpath && print "$nextstr$file\n";
                        -d $fullpath && push(@pathlist,$fullpath);
                        $makefilecheck && -f $fullpath && push(@pathlist,$fullpath);
                }
        }

        $nextstr =~ s/$dash/ /g;
        $lastflag != 1 || $nextstr =~ s/\|(\ *)$/ $1/;

        $islast=0;
        for $file (@pathlist) {
                if ($file eq $pathlist[$#pathlist] )  {$islast = 1;}
                &list_dirs($file,$nextstr,$islast) ;
        }
        #$islast != 1 || print "$nextstr\n";
        $curnestlevel--;
}

@ARGV gt 0 || die "Usage: ftree [-f] [-l nestlevel] <dir name>\n";
$makefilecheck=0;

while ($ARGV[0] =~ /^-/ ) {
        $ARGV[0] =~ /^-f/  && ($makefilecheck=1) &&  shift @ARGV && next;
        if ($ARGV[0] eq "-l") {
                shift @ARGV;
                @ARGV gt 1 || die "Usage: tree [-f] [-l nestlevel] <dir name>\n";
                $nestlevel = shift @ARGV;
                $nestlevel=~ /[0-9]*/ || die "Usage: tree [-f] [-l nestlevel] <dir name>\nnestlevel should be a number\n";
                next;
        }
        die "Usage: tree [-f] [-l nestlevel] <dir name>\nUnable to open directory
        $ARGV[0]\n";
}
-d $ARGV[0] || die "Usage: tree [-f] [-l nestlevel] <dir name>\nUnable to open directory $ARGV[0]\n";
$directory = `pwd`;
chop($directory);

if (!($ARGV[0] =~ /^[\.\/].*/)) {
        $ARGV[0] = "./" . $ARGV[0];
}
$firsttime=1;
&list_dirs($ARGV[0],"",1);


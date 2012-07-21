#!/usr/bin/perl
#dump nero-burning-rome .nra files. const hdr + records of varsize fields

die "$0 [-] *.nra\n".
    " -  dumps all to stdout, else *.nra -> *.t\n" if $#ARGV<0;

sub framesplit {
     local( $frames) = $_[0];
     local( $sm, $ss, $sf);
     $sm = int( int( $frames/75)/60);
     $ss = int( $frames/75) %60;
     $sf =      $frames%75;
     ($sm, $ss, $sf);
}

sub readstr_sz {
    local( $what) = $_[0];
    local( $dosz) = $_[1];
    local( $doprn)  = $#_>=2 && $_[2];
    $sz = readint( "$what sz" );
    if ($sz>0) {
        $l = read(IN,$str, $sz );  die "$what"   if $l<$sz;
        skip(1);
    } else {
        $str = '';
        skip(1) if $dosz;
    }
    print "$what/$sz: '$str'\n" if $doprn;
    $str;
}
sub readstr {
    local( $what) = $_[0];
    local( $prn)  = $#_>=1 && $_[1];
    readstr_sz( $what, 0, $prn);
}
sub readstr1 {
    local( $what) = $_[0];
    local( $prn)  = $#_>=1 && $_[1];
    readstr_sz( $what, 1, $prn);
}

sub readid {
    local( $what) = $_[0];
    local( $prn)  = $#_>=1 && $_[1];
    $l = read(IN,$str, 4);    die "readid"   if $l!=4;
    print "$what: $str\n" if $prn;
    $str;
}
sub skip {
    local( $n) = $_[0];
    local( $prn)  = $#_>=1 && $_[1];
    $l = read(IN,$buf, $n );    die "skip $n"   if $l!=$n;
}
sub readint {
    local( $what) = $_[0];
    local( $prn)  = $#_>=1 && $_[1];
    $l = read(IN,$buf, 4 );    die "$what"   if $l<=0;
    $sz = unpack( "l", $buf);
    print "$what: $sz\n" if $prn;
    $sz;
}
sub readframe {
    local( $what) = $_[0];
    local( $prn)  = $#_>=1 && $_[1];
    $f = readint( $what, 0);
    if ($prn) {
        ($sm,$ss,$sf) = framesplit( $f);
        print "$sm:$ss:$sf \n";
    }
    $f;
}
sub fram {
    ($m,$s,$f) = framesplit( $_[0]);
    sprintf("%2d:%02d:%02d", $m,$s,$f);
}

while ($#ARGV>=0) {
  $IN = shift;
  if ($IN eq "-") {
     $use_stdout = 1;
     next;
  }
  open(IN) || die "$! $IN";
  binmode(IN);
  print ":$IN\n";
  if ($use_stdout) { $OUT = "-"; }
  else { $OUT = $IN.'.t'; }
  print $OUT."\n";
  die "IN==OUT" if $OUT eq $IN ;
  $OUT = ">$OUT";
  open( OUT ) or die "$! $OUT";

#header
  $l = read(IN,$buf, 1 ); die  if $l<=0;
  $sznero = unpack( "c", $buf);
  $l = read(IN,$nero, $sznero ); die  if $l<=0;
  #print $nero."\n";
  $szhdr = readint( "szhdr");
  skip( $szhdr+0x30-0x12-8 );
  $ii = readint( "ii");
  print "$ii \n";

  $i=0;
  while ($i<$ii) {
     $type = readid( "type" );  #EVAW, GULP
     skip(4);
     $path = readstr( "path" );

     if ($type eq "EVAW") {     #old format
        $file = readstr( "file" );
        skip( 5);
        $frame_from = readframe( "frame_from"); #?
        $frame_to   = readframe( "frame_to");   #?

        $frame_pause = readframe( "frame_pause");
        skip( 0x221-0xD-4 );

        $name = readstr( "name");
        $namu = readstr( "namu");
        skip( 0x28 );

        $frame_start = readframe( "frame_start");
        $frame_end   = readframe( "frame_end");
        skip( 0x13 );

        $filt = readid( "filt"); #ENON, EDAF, ...
        $l = read(IN,$buf, 1 ); die    if $l<=0;
        $sz = ord( substr($buf, 0,1 ));
        $l = read(IN,$buf, $sz -1 ); die    if $l<=0;

     } elsif ($type eq "GULP") {
        skip(5);
        $file = readstr( "file" );
        $cdtext1 = readstr1( "cdtext1" );
        $cdtext2 = readstr1( "cdtext2" );
        skip( 0x12-4);
        $frame_from  = readframe( "frame_from");
        $frame_to    = readframe( "frame_to");
        $ignore      = readint( "ignore");

        $frame_pause = readframe( "frame_pause");
        $frame_end   = readframe( "frame_end");
        $frame_start = readframe( "frame_start");

        skip( 6);

        $filt = readid( 'filt'); #ENON, EDAF, ...
        skip( 0x10);
        $xx = readint('xx');
        skip( 5 + ($xx==1) );

        $name = readstr1( "name");
     }


  #  for ($i=0; $i<$l; $i++) { printf( "%02x ", ord(substr($buf,$i))); }
  #  for (; $i<16; $i++) { print "   "; }
  #  print "| "; $buf =~ y/\000-\037/./; print "$buf\n";

     $file =~ s/\.wav//;
     $i++;
     print OUT (($filt ne "ENON") ? '*' : ' ');
     printf OUT  "%2d. ", $i;
     print OUT "$file";

     #print fram( $frame_from),  ' ', fram( $frame_to), "\n";
     #print fram( $frame_start), ' ', fram( $frame_end), "\n";

     $frame_len = $frame_end - $frame_start;
     ($lm,$ls,$lf) = framesplit(  $frame_len );
     ($pm,$ps,$pf) = framesplit(  $frame_pause);

     $ft = $frame_to - $frame_from;
     die "wrong frames $ft, $frame_len" if $frame_to-$frame_from != $frame_len;

     printf OUT " \t%2d:%02d", $lm,$ls; #:$lf
     printf OUT " /p%d", $pm*60+$ps; #:$pf
     printf OUT "  [%s - %s]", fram($frame_start), fram( $frame_end);
     printf OUT " \t<- [%s - %s]", fram($frame_from), fram( $frame_to)
            if $frame_from || $frame_to != $frame_len;
     print OUT "  $cdtext1  $cdtext2";

     print OUT "\n";
  }
  close( OUT) if !$use_stdout;
  close( IN);
}

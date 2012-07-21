$ADR = shift;
$IN = shift; $IN = "g.map" if $IN eq '';
die "use: map4G {seg:address or unused[#] or size[#]} [file.map]; # sorts by size" if $ADR eq '';

sub type { substr( $_[0],13,1);}        #given the array-member
sub what { substr( $_[0], 15); }        #given the array-member
sub addr { substr( $_[0],5,8); }        #given the key-of-array
sub target {    #given input $ADR, set numberaddr and ret searchable key
   ($adr1,$numadr) = split(':', $ADR);
   join(':', ('0'x (4-length($adr1)) ).$adr1, ('0'x (8-length($numadr)) ).$numadr);
}

open(IN) || die "can't open $IN\n";
while (<IN>) {
    chop;
    $adr = substr( $_, 0, 13);
    $typ = substr( $_, 13, 1);
    next if $typ ne ' ' && $typ ne '+' && $typ ne '*' || substr($_,4,2) ne ":0";
    $_ =~ s/near //g;
    $rec{$adr} = $_;
}
close IN;
$SORT = ($ADR =~ s/#$//);       #last # if any

if ($ADR eq 'unused' || $ADR eq 'size') {
   $lastk = 'z';
   for $k (sort keys %rec) {
       if ($lastk ne 'z' && $ast{$lastk}==-1) {
          $ast{$lastk} = hex(&addr($k)) - hex(&addr($lastk));
        }
       if ($ADR eq 'size' || &type($rec{$k}) eq '*') {
          $ast{$k} = -1;
          $lastk = $k;
        }
    }
   if ($SORT) {
      for $k (sort keys %ast) {
         $h = sprintf( "%08X", $ast{$k} );
         $szsort{ $h.'#'.$k } = 1;
       }
      for $szs (sort keys %szsort) {
         ($sz,$k) = split('#',$szs);
         $r = $rec{$k};
         printf "$k [x%s]%s %s\n", $sz, &type($r), &what($r);
       }
    } else {
      for $k (sort keys %ast) {
         $r = $rec{$k};
         printf "$k [x%06X]%s %s\n", $ast{$k}, &type($r), &what($r);
       }
    }

} else {
   $keyadr = &target($ADR);        #set $numadr

   $lastk = 'z';
   for $k (sort keys %rec) {
       last if $k gt $keyadr;
       $lastk = $k;                #last le
   }
   die "not found" if $lastk eq 'z';
   $r = $rec{$lastk};
   $ofs = hex($numadr) - hex(&addr( $lastk));
   printf "$r\n:ofs: x%X\n",$ofs;
}

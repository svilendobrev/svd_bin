$ADR = shift;
$IN = shift; $IN = "g.map" if $IN eq '';
die "use: mapGld {address or unused[#] or size[#]} [file.map]; # sorts by size" if $ADR eq '';

sub type { ' '; }                     #given the array-member
sub what { substr($_[0],9); }         #given the array-member
sub addr { $_[0]; }                   #given the key-of-array
sub target {    #given input $ADR, set numberaddr and ret $adr as searchable key
   $numadr = $ADR;
   ('0'x (8-length($numadr)) ).$numadr;
}

open(IN) || die "can't open $IN\n";
while (<IN>) {
    s/\s+$//;
# map format:
#......
#Linker script and memory map
#.....
#.segname        startofs         size
# *(.segname)
# .segname       startofs         size  objectfilename
#                startofs               funcname
#....
#OUTPUT(exename exetype)
#e.g.:
#.text           0x000018a8    0x2f758
# *(.text)
# .text          0x000018bc      0x4b8 C:/DJGPP/lib/crt0.o
#                0x00001aa8                __exit

    if (/^Linker script and memory map/) { $in=1; next; }
    next if !$in || /^\s*$/;
    if (s/^OUTPUT\(//) { $exenametype = $_; print; print " -exe\n"; last; }
    if (s/^(\.\w+)\s+0x[\da-f]+\s+0x[\da-f]+//) {
       $in=2; $segname=$1; next; }        #ignore whole segments
    next if $in<2 || /^ \*\(\.?\w+\)/;                     #skip *(.text)
    if (s/^ \.\w+\s+0x[\da-f]+\s+0x[\da-f]+//) { $objname=$_; next }

    $adr = substr( $_, 18, 8);
    $rec{$adr} = $adr.":".$segname.":".substr($_, 38)." \t:".substr($_,0,6)." ".substr($objname,-20);
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

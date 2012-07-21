$IN = shift;
die "$0 file.map [hex-address-to-find]\n"
 ."\tstrange addresses (data/stack seg, or 16bit code) might be wrong"
 ."\twithout address will show whole address-sorted map"
 if $IN eq '';
$ADR= $#ARGV<0 ? -1 : hex(shift);

open(IN) || die "$! $IN";
while (<IN>) {
  $on++ if /Publics by Value/i;
  next if !$on || /^\s+$/;

  if ($ADR<0) { print; }
   else {
        ($seg,$ofs) = split(/:/); next if $ofs eq '';
        $x = hex( $ofs );
         #some things are at FFFFxxxx, which signed, is <0; but unsigned as here, is too big
        $x = ($x - 0xFFFFFFFF) -1 if $x > 0x7FFFFFFF;
        if ($x>$ADR) { printf("at offs x%lX in::: $prev",$ADR-$xprev); last; }
        $prev=$_; $xprev=$x;
   }
}

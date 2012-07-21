# parser/filter for newspaper like small ads (cars, houses, etc...)
# define the arrays below and then include this file
# will show things and try to figure out where they are if a phone is given
#SvD apr'99

#@fin=( ... ); #what to search for; simple regexpr.
#@nif=( ... ); #what to avoid     ; simple regexpr.

foreach $f (@fin) { $fn .= $f."|"; } chop $fn; $fn = "($fn)";
foreach $f (@nif) { $nf .= $f."|"; } chop $nf; $nf = "($nf)" if $nf ne '';

$nodbg=1;
$included=1;    #for phonecod.pl
$IN = "/bin/locphone.tbl";
do "/bin/phonecod.pl";

$Q=8;   #up to 8 lines per item
while (<>) {
  if ($n) {
    s/<br>//gi;
    if (/^\n/) { $n=0; } else { s/\n//gi if (($Q-$n)&1);
       print; $n--;
       (@match) = /(8\d\d+) *(\d+)/;
       &phone($match[0].$match[1]) if $#match>=0;
    }
    next;
   }
  if (m!$fn!io && ($nf eq '' || !m!$nf!io)) {
    s/<br>//gi;
    s/\n//gi; print "\n\n$_"; $n=$Q; $p=1;
   } elsif ($p) {
     if (m|</a><br>|i) {
        s/\n//gi;
        ($a,$d) = split(/:/);
        $p=0; print $d;
      }
   }
}

###########
#example for houses in som suburbs:
# @fin=(
#  "up-*down *hill",
#  "cloakka",
#  "north *suburb",
# "~~~~");        #always supply one never matched line
#
# @nif=(
#  "4 *b\.* *r"   #4 bed rooms are too big, don't u think
# );
#
# do "/me/pl/findit.pl";

###########
#example for cars:
# @fin=(
#  "coron+a",   #toyotas
#  "corol+a",
# # "tercel"
#  "seca",
#  "mazda",
# #"626",
# # "leon", #subaru
#  "pulsar", #nissan
# # "laser", #ford
# # "colt", #mitsubi
# # "sigma", #mitsubi
# # "civic", #honda
# #"citroen",
# # "peugeo",
#   "renaul",
#
# "~~~~");
# @nif=(
#  "121","323","929","mx5","rx7", "astina", #mazdas
#  "4 *spe*d", "197[0-9]", "198[0-9]", "'7[0-9][^0-9]", " 7[0-9][^0-9]"
# );
#
# do "/me/pl/findit.pl";

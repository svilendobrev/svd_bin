#!/usr/bin/perl
#$Id: cyr2lat.pl,v 1.2 2007-05-06 16:18:19 sdobrev Exp $

%zvuchene_map = (
" ¡¢£¤¥", "abvgde",
"¦",  "zh",
"§¨©ª«¬­®¯°±²³´µ¶", "zijklmnoprstufhc",
"·",  "ch",
"¸",  "sh",
"¹",  "sht",
"¼",  "",
"º",  "y",
"¾",  "yu",
"¿",  "ya",
"½",  "e",
"»",  "i",
);

%zvuchene_qw_map = (
" ¡¢£¤¥", "abwgde",
"¦",  "[j]",
"§¨©ª«¬­®¯°±²³´µ¶", "ziiklmnoprstufhc",
"·",  "ch",
"¸",  "sh",
"¹",  "sht",
"¼",  "",
"º",  "y",
"¾",  "[ji]u",
"¿",  "[ji]a",
"½",  "e",
"»",  "i",
"¢",  "v",
);


%qwerty_keyboard_map = (        #fonetic
" ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶", "abwgdevzijklmnoprstufhc",
"·",  "`",
"¸",  "\\[",
"¹",  "\\]",
"¼",  "",
"º",  "y",
"¾",  "\\\\",
"¿",  "q",
"½",  "@",
"»",  "^",
);

%qwerty_keyboard_map_yu = (        #fonetic
" ¡¢£¤¥¦§¨",
 "abvgde`zi",
"ª«¬­®¯°±²³´µ¶",
"klmnoprstufhc",
#"©","j",
"-", "j",
"·",  "~",
"¸",  "\\{",
"¹",  "\\}",
"¼",  "",
"º",  "y",
"¾",  "\\\\",
"¿",  "q",
"½",  "@",
"»",  "^",
);

%desi_map = (        #digito-fonetic
" ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶", "abvgdejziiklmnoprstufhc",
"·",  "4",
"¸",  "6",
"¹",  "6t",
"¼",  "",
"º",  "y",
"¾",  "iu",
"¿",  "ia",
"½",  "@",
"»",  "^",
);

if ($ARGV[0] =~ /^-/) { $LAT2CYR= ($ARGV[0] =~ /-lat2cyr/i); shift; }

 %map = %zvuchene_map;
#  %map = %zvuchene_qw_map;
# %map = %desi_map;
# %map = %qwerty_keyboard_map_yu;

##init
 $p1 = $q1 = '';        #collect direct translations
 foreach $p (keys %map) { $q = $map{$p};
    if ($LAT2CYR) {
      $p1u = $p; $q1u = $q;
      $p1u =~ y/\240-\377/\200-\237/;     #bglow2up bg
      $q1u =~ y/a-z/A-Z/;                 #latlow2up
      undef $map{$p};
      if (length($p)==1) {      #razmeni lat s bg
         $map{$q} = $p;
         $map{$q1u} = $p1u if ($q1u ne $q) ;
      } else {                  #zalepi malki i golemi
         $p1 .= $q.$q1u;
         $q1 .= $p.$p1u;
      }
    } else {
      $p1u = $p2l = $p2u = $p;
      $p1u =~ y/\240-\377/\200-\237/;     #bglow2up bg
      $p2l =~ y/\240-\377/\340-\377/;     #bglow2low win
      $p2u =~ y/\240-\377/\300-\337/;     #bglow2up win
      $qu = $q; $qu =~ y/a-z/A-Z/;
      if (length($p)==1) {
        $map{$p2l} = $q;
        $map{$p2u} = $map{$p1u} = $qu;
      } else {
        undef $map{$p};
        $p1 .= $p.$p1u.$p2l.$p2u;
        $q1 .= $q.$qu.$q.$qu;
      }
    }
 }

sub low {
  local($a) = $_[0];
  local($b) = $_[1];
  $b =~ y/A-Z/a-z/;
  $a.$b;
}

sub tx {
  foreach $p (reverse sort keys %map) { $q = $map{$p};
     next if $p1 =~ /$p/;       #bez povtariashti se edinichni
     eval( "s/$p/$q/g" );
  }
  eval( "y/$p1/$q1/" ) if $p1 ne '';
	#ABcde->Abcde; syshtoto trebe i za lat2cyr
  s/([A-Z])([A-Z])(?=[a-z])/&low($1,$2)/ge;
}

while (<>) {
    &tx( );
    print;
}
# vim:ts=4:sw=4:expandtab

#!/usr/bin/perl
#translate local URLs in a html file into different remote URLs
#svd may'99
#classification depends on the 1st letter of the file/url and is made
#as per the sites table (associative array).
#the 1st pair and the last pair are mandatory

%sites = (            ##what starts with : goes to
  "#",      ""               #label marker    :   remain unchanged
, "[a-i]",  ""               #a-i             :   remain unchanged
, "[j-k]",  "URLhere/"       #j-k             : go to URLhere/
, "l"    ,  "URLthere/"      #l               : go to URLthere/
, "."    ,  "URL3/"          #everything else : go to URL3/
#fill yours in same style
);


sub xchg {
   local($file) = $_[0];                        #get the url/filename
   if ($file !~ /^(http:|ftp:|www\.|news:|mailto:)/ ) {  #if it does not start with these
     foreach $k (keys %sites) {         #search in the list above to match the 1st character
#      print "$k:$file\n";
       if ($file =~ /^$k/i) {           #lower/uppercase does not matter
         $file = $sites{$k}.$file;      #insert what is there BEFORE the filename
         last;
        }
      }
    }
   $file;
}

undef $/;
$TMPDIR = "_temp";
mkdir($TMPDIR,0777);

while (<>) {
  print "$ARGV\n";
        #body background; img src; frame src; a href; frame action ?
  s!(background|<a href| src)(=")([^"]+)(")!sprintf("$1$2%s$4",&xchg($3))!ige;
  $OUT = ">$TMPDIR/$ARGV";
  open (OUT) || die "$! $OUT";
  print OUT;
  close OUT;
}

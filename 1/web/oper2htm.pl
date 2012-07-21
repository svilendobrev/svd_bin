#!/usr/bin/perl
#opera-boomarks2htm SvD '99
# things/folders with names starting with ! are NOT shown
# use to hide private stuff

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time()); $mon++; $year+=1900; $yday++;
print "<html><body>autolinks by oper2htm.pl<BR> $mday.$mon.$year <BR>\n";
$hide=0;
$hidedeeper=9999;

# separate urls or whole folders+subfolders,
#  which names start with "!" are skipped
sub printer {
  if ($folder<=$hidedeeper && ($lastwasfolder || $url ne '')) {
    $name =~ s/ +$//;
    $skip = 0+($name =~ /^!/);
    if ($lastwasfolder) {
       $hide = $skip;
       $hidedeeper = $skip ? $folder : 9999;
       print "<b>-- $name</b>" if !$hide;
     } else {
       $skip = $hide if !$skip;
       print (($url =~ m!^(file:|.:[/\\]|[/\\])!i) ? "$url: $name" : "<A href=\"$url\">$name</a>") if !$skip;
     }
    if (!$skip) {
      print "; $alias" if $alias ne '';
      print ": $desc"  if $desc  ne '';
      print "<br>\n";
      print "<ul>\n" if $lastwasfolder;
    }
  }
};

  $folder=0;

while (<>) { chop;
   if (/^[#-]/) {
       &printer;
       $name=$desc=$alias=$url='';
    }
   if (/^#FOLDER/) { $folder++; $lastwasfolder++; next; }
   elsif (/^#/) { $lastwasfolder=0; next; }
   elsif (/^\-/) { print "</ul>\n" if $folder<$hidedeeper; $folder--; next; }

   if (s/^[ \t]*NAME=//) { $name = $_; }
   elsif (s/^[ \t]*URL=//) { $url = $_; }
   elsif (s/^[ \t]*DESCRIPTION=//) { $desc = $_; }
   elsif (s/^[ \t]*SHORT NAME=//) { $alias = $_; }
}
do printer;
print "<BR>-------eof\n";
#SvD 02'99

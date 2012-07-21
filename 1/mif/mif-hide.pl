#!/usr/bin/perl
# sd'99  - may not work correctly, not prooftested
if ($ARGV[0] eq '-') {
  $P++; shift(@ARGV);
}

$DEL =-1;       #remove the conditional AND the contents of it
$KEEP=+1;       #remove the conditional BUT leave the contents
                #everything else is not touched!

%w = (          #use only $DEL or $KEEP !!!
#,   'Hidden', -1
   'Deleted'  , $DEL
,  'Inserted' , $KEEP
);

$top=9999;
$bot=0;

while (<>) {
 $x=$_;
 if (/^ *<ConditionCatalog/) {
   $catalog++ ;
 } elsif (/> # end of ConditionCatalog/) {
   $catalog = 0;
   die "missing condition\n" if $found != 0+%w;
 } elsif ($catalog) {
   if (/<CTag/) {
     s/^ *<CTag .//; s/.>.*\n*$//;
     $found++ if $w{$_} ne '';
   }
 } else {
  $delta  = s/^ *<//;
  $delta -= s/ *>//;
  $stack[$level] = $x if ($delta >0);
  $level += $delta;


  $skipit=0;

  if    (/^Conditional/) { $incond++; $skipit=1; }
  elsif (/^ *# end of Conditional/) { $incond=0; $skipit= !!$todo; }
  elsif ($incond) {
    if (/^InCondition ./) {
      $s = $_; $s =~ s/^InCondition .//; $s =~ s/. *\n*$//;
      $todo=0;
      foreach $k (keys %w) {
        if ($s eq $k) {
          $todo = $w{$k};
          $skipit=1;    #for either del or keep, this current line should disappear
         last;
      } }
      $bot= $level-1;
        print "##MATC $todo $top $bot $s#\n" if $P && $todo;
    }
##### restore that skipped line before the actual line
    if (!$todo) {       print "##adx\t\t ." if $P;
      print $stack[$level-1]; }
   }
  elsif (/^Unconditional/) {
    for ($i=$top;$i<$bot;$i++) {        print "##add\t\t ." if $P;
      print $stack[$i]; } #print skipped hierarchy
    $top=9999;
    $skipit |= $todo;
    $todo=0;
##### will be skipped if was single conditional
##### (but remain if were several in a sequence OR not matched)
  }

  if ($skipit) {        print "##skip1\t\t .$x" if $P;
    next;
  }


##### if cond falls through the hierarchy, remember the outmost level
  if ($todo<0) {
     if ($delta >= 0) {
        $skipit=1;
     } else {
        $skipit = $level>=$bot;
        $top = $level;  #remember last level we exit to
     }
  }

#  $skipit = $matched &&  $todo<0 &&
#               ($delta >=0 || $level>=$bot); #else will print closing >'s
if (1+0) {
  if ($skipit) {        print "##sk2 $todo $top $bot\t.$x" if $P;
##### remember things like uniqID, pgftag etc...
     $stack[$level-1] .= $x if (/^PgfTag / || /^Unique /);
     next;
  } else {
    for ($i=$top; $i<$bot; $i++) {      print "##adz $todo $top $bot\t " if $P;
      print $stack[$i]; } #print skipped hierarchy
    $top=9999;
  }
}
 }

# !! should print the hierarchy on the way out to level 0 if stripping switched on inside
# !! should remember the hierarchy, and print it if was stripped and unconditional found;
# eg <ParaLine
# ...
#  <Unconditional>
#  ...
        if ($P) {
          for ($i=0;$i<6;$i++) { $a=$stack[$i]; $a=~s/\n//; $a=~s/^[ \t]*<* *//; printf "%5.5s ",$i<$level?$a:" "; }
          print " $level \t$top\t$bot\t.";
        }
 print $x;
}


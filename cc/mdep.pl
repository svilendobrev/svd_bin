#!/usr/bin/perl
# makedep(endency)
# this one (c) SvD 10'99/2k1/2k4
# v.1.1
# use as u like, keeping the above (c) in

#absolute paths: those begin with
$SLASH   = 1;   # slash (back or forth) is root
$DRIVE   = 1;   # c: or mysrv:
$TILDE   = 0;   # ~name or ~/ddd

$UPCASE  = 0;   # ..\paRt/time == ../ParT\TimE  = ../PART/TIME
$NOSYSTEMS = 0; # dont parse #include <...>
$NOSIMLIFY = 0; # dont simplify ././x and a/../b/../c/d
$OPENSTRICT = 0; # add inaccessible #include files as-is

sub skip_coz_system {
   $_[0] =~ s/^<// && $NOSYSTEMS;
}
sub avoid_paths {
   local( $a) = $_[0];
   local( $p);
   foreach $p (@_pathsX) {              #$p is a reference!
      if ($a =~ /^$p/) {
                print STDERR "$pfx avoid $a matching $p;\n" if $DBG;
         return 1;
      }
    }
   0;
}

sub simplifyappend {
   local( $p) = $_[0];
   local( $a) = $_[1];
   if (!$NOSIMPLIFY) {
      $simplified =0;
      do {
         $simpled =0;
          ###try simplify appending ./ and ../
          # p/q/ + ./x  -> p/q/x
         $simpled++ if $a =~ s,^\.(/+|$),,;
          # p/q/ + ../x -> p/x
         if ($p =~ m,^\w+/$,           # just plain name there
           && $a =~ s,^\.\.(/+|$),,
         ) { $p =~ s,^\w+/+$,,; $simpled++; }
         $simplified += $simpled;
       } while ($simpled);
        print STDERR "$pfx .simplified $_[0] + $_[1] = $p$a;\n" if $DBG && $simplified;
    }
   $p.$a;
}

sub open_full {
   local( $a) = $_[0];
   local( $parentpath);
   local( $akey);
   local( $p);
   $a =~ tr|a-z\\|A-Z/| if $UPCASE;
   $OPENED = 0;
   ($parentpath) = ( $_[1] =~ m,(.*[\\/]),,);    # get path
                print STDERR "$pfx path extracted from $_[1]: $parentpath\n" if $DBG;
   $akey = "$parentpath\n$a";
   $IN = $_fullnameof{$akey};
   return $IN if $IN ne '';
   $is_abs = $SLASH && $a =~ m|^[/\\]|  #starting slash
          || $TILDE && $a =~ m|^~|      #starting tilde
          || $DRIVE && $a =~ m|^\w+:|   #drivename:
    ;
        #from parent's perspective - NOT from initial dir
   $IN0 = $IN = $is_abs ? $a : &simplifyappend( $parentpath,$a);
   if (open(IN)) { $OPENED++; }
    elsif ( !$is_abs ) {
                print STDERR "$pfx try paths:\n" if $DBG;
      foreach $p ($parentpath,@_paths) {              #$p is a reference!
                print STDERR "$pfx try $p;\n" if $DBG;
         $IN = &simplifyappend( $p,$a );
         if (open(IN)) { $OPENED++; last; }
       }
    }
   $IN = $IN0 if !$OPENED;
   $_fullnameof{$akey} = $IN if $OPENED; #cache failures too? remove the if
                 $akey =~ s/\n/ + /;
                 print STDERR "$pfx cache $akey == $IN;\n" if $OPENED && $DBG;
   $IN;
}

sub isincomment {
   local($x) = $_[0];
        #simplest possible:
   $off += m|^[^"'/\\]*/\*|;       #... /*     ... should be SIMPLE
   $off =0 if m|\*/|;              #any found
   $off;
}
########################
#1. ... /* ...
#2. " /* \" */ "
#3. ".." /*
#4. ".." ... /*
#5. '"/*"'
# combine.... oh dear. forget. too complicated
#        #eat a string: ^..".."
#  if ($x =~ s/^[^"]*"//) {    #all up and the quote open
#     while ($x =~ s/^[^\\"]+//) {     #all up to 1st backslash or quoteclose
#            $x =~ s/^\\"//; }         #kill \" if stopped on it
#     $x =~ s/^[^"]*"//;               #all up and the quote close
#   }
############

$l = 0;

sub process {
   local( $target) = $_[0];
   local( $a) = $_[1];
   local( $f,$full);
   local( @flist, $p, $fl);
   local( $found) =0;
   local( $off  ) =0;

   $l++; die if $l>200;
                print STDERR '='x$l," $target wants $a\n" if $DBG;
   local( $pfx) = '-'x($l+1);

   if (&skip_coz_system($a)) {
                print STDERR "$pfx skipped - system\n" if $DBG;
    } else {
      &open_full($a, $target);            #->IN;OPENED
      if (!&avoid_paths($IN) && $_depends{$target} !~ /\n$IN\n/ ) {
         $dependant = "\n$IN\n" ;
         if (defined $_depends{$IN} ) {          #already processed
            $_depends{$target} .= $dependant ;
                        print STDERR "$pfx cached $IN\n" if $DBG;
#                       print STDERR "$pfx dep($target,$dependant)\n" if $DBG;
          } else {
            if (!$OPENED) { ## && !open(IN)) {
               $_depends{$target} .= $dependant if !$OPENSTRICT ;
               print STDERR "    !! cant find/open $a from $target\n";
             } else { $f=0;
#                       print STDERR "$pfx dep($target,$dependant)\n" if $DBG;
               $_depends{$target} .= $dependant ;
               while (<IN>) {                    #collect all #inc's in current file
                 s/^\s+//; s/\s+$//;             #kill lead/tail spc
                 next if &isincomment($_);
                 next if !s/^#\s*include\s*//;
                 if ($system = /^</) {
                    s/([^>]+)>[\s\S]*/$1/;       #including starting < as flag
                  } elsif (s/^"//) {
                    s/([^"]+)"[\s\S]*/$1/;
                  } else {
                    print STDERR "!! file $IN:$.: unknown syntax: include $_; ignoring\n";
                    next;
                  }
                 $flist[$f++] = $_;
                        print STDERR "$pfx add $_\n" if $DBG;
               }
               close(IN); $OPENED=0;
               $full = $IN;
               $_depends{$IN} = '';
               foreach $f (@flist) { &process($full,$f); }
             }
          }
       } else {
                print STDERR "$pfx avoided-paths or already there\n" if $DBG;
       }
      close(IN) if $OPENED;
    }
                print STDERR '='x$l," done   $a\n" if $DBG;
   $l--;
}

sub depflat {
   local(@dp) = split(/\n+/,$_depends{$_[0]});
   local($f);
   $xxx++;
   foreach $f (@dp) {
      if ($f ne '') {
         $q = $f; $q =~ s/\\/\\\\/g;
         if ($res !~ m, $q ,) { $res .= "$f "; &depflat($f); }
         die "recursion" if $xxx>100;
       }
    }
   $xxx--;
}

############
die "makedep.pl [-flags] [-Ipath2include] [-Xpath2exclude] file[s]"
 ."\n\t-s[ystem]: avoid system includes e.g. <a.h>"
 ."\n\t-u[pcase]: turn all to upcase and \\ to / (unix is case sensitive)"
 ."\n\t-o[penstrict]: add only files that are accessible"
 ."\n\t-nosimplify: dont fix a/./ b and a/ ../b/c; may do many times same file"
#."\n\t-2/|| -2\\ : turn all slashes into / or \\ respectively"
 ."\n\t-r[egexp]=Exprs: before print of result(\$_), eval(Exprs) over it"
 ."\n\t-d[ebug] : print traces"
 ."\n\t-EIenvvar: look into envvar for include paths"
 ."\n\t-EXenvvar: look into envvar for exclude paths"
 ."\n include paths: where to search"
 ."\n exclude paths: matching files are not added to dep (still checked for access)"
 ."\n all paths (-I,-X, envvars in -EI,-EX, prefixes-as-is -x) can be  :  separated lists (default)"
 ."\n if next char after the option is  ; or :  it becomes the path separator."
 ."\n order of search: if absolute: as-is; else: 1.parent's path; 2.paths"
 ."\nexample: mdep.pl -s -I..;. -Imy '-r=s/\\.c :/.o :/;s,^,\$(OBJ)/,' this.c oh/*.c"
 ."\n" if $#ARGV<0;

foreach $t (@ARGV) {
   $FORINCLUDE='';
   if ($_NEXTOPTISINCLUDE ne '') {
      $FORINCLUDE = $_NEXTOPTISINCLUDE;
      $_NEXTOPTISINCLUDE='';
    } else {
      if ($t =~ /-d(ebug)?$/)    { $DBG       =1; next; }
      if ($t =~ /-s(ystem)?$/)   { $NOSYSTEMS =1; $state .= "NOSYSTEMS "; next; }
      if ($t =~ /-u(pcase)?$/)   { $UPCASE    =1; $state .= "UPCASE ";    next; }
      if ($t =~ s/-r(egexp)?=//) { $REGEXP  .= $t; next; }
      if ($t =~ /-o(penstrict)?$/) { $OPENSTRICT =1; $state .= "OPENSTRICT "; next; }
      if ($t =~ /-nosimplify$/)  { $NOSIMPLIFY=1; $state .= "NOSIMPLIFY "; next; }
    # if ($t =~ m,-2/$,)         { $TO_FSLASH =1; $state .= "\\2/ "; next; }
      $t =~ tr|a-z\\|A-Z/| if $UPCASE;
      if ($t =~ s/^-E([IX])//) { $t = "-$1$ENV{$t}"; }
      if ($t =~ s/^-([IXx])//) { $IX = $1;
         $SEP = ':'; # default
         $t =~ s/^://;
         $SEP = ';' if $t =~ s/^;//;
         if ($t eq '') { $_NEXTOPTISINCLUDE = $IX; next; }
         $FORINCLUDE = $IX;
       }
    }
   binmode(STDOUT); ## if $BIN; noCRLF's

   if ($FORINCLUDE ne '') {
      (@pths) = split( $SEP, $t );
      foreach $t (@pths) {
         next if $t =~ /^\s*$/;          #empty
         $t .= '/' if ( !(
                        $SLASH && $t =~ m|[/\\]$|     #ending slash
                     || $DRIVE && $t =~ m|\w+:$|      #bare drivename:
                     || $FORINCLUDE eq 'x'
                    ));
         if ($FORINCLUDE eq 'I') {
            push(@_paths,  $t) if !grep( m|^$t$| , @_paths);
         } else {
            push(@_pathsX, $t) if !grep( m|^$t$| , @_pathsX);
         }
       }
      next;
    }
        print  STDERR " *state: $state \n REGEXP=$REGEXP \n" if $DBG;
        printf STDERR " *pathsINCL: %s\n", join(' ',@_paths)  if $DBG && $#_paths>=0;
        printf STDERR " *pathsEXCL: %s\n", join(' ',@_pathsX) if $DBG && $#_pathsX>=0;
   $t = &simplifyappend( '',$t);
   &process(' ',$t);
   $res=" ";
   &depflat( $t);
   if ($res !~ /^\s*$/) {        #not empty
      $_ = "$t :$res\n";
#     $_ =~ y,\\,/, if $TO_FSLASH;
      eval( "$REGEXP" ) if $REGEXP ne '';        # "\$y =~ ..."
      print;
   }
}

#$,="\n";print %_depends;

#####
#documentation: near to correct ;)
# struct: file {included_as, fullname}
#
# process(target, in)                   #target depends on in
#   get_fullname(in, PATHS);            #cache links name->fullname
#   if shall-be-added && !added-yet
#      target.dep.add(in_full)
#      if (shall_be-processed)
#         if ! already_processed && opened-ok {
#            parse-inside:{
#              inclist = get-all-inc's(in_full);
#              close(in_full)
#              foreach in inclist
#                 process(in_full,inc);
#            }
#   close(in_full) if still open

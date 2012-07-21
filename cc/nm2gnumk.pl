#!/usr/bin/perl -n
# (c) SvD '99-2k
# makefile syntax convertor: MS nmake to gnumake

 #crlf
binmode(STDOUT); s/\r\n/\n/;    #these both are required

$off++ if /^#ifdef NMAKE/;      #allow ignoring NMAKE specific stuff
$_ = "#NMAKE ".$_ if $off;
$off=0 if /^#endif NMAKE/;

if (!/^\s*#/) {  #comment

 # $** = all dependents = $^ (or $+ - which does not ignore repeated ones)
s/\$\*\*/\$^/g;
 # $* : target without extension; ok for static rules (a.x:b); may be wrong for nonstatic ones(%.x:%.c)
 # $<, $@ should be ok

 # cmd'line's starting white space
s/^  +/\t/;                     #assume more than 2 spaces mean tab:
                                # gnu wants the commands to start with TAB, not just white space

#### !stuff:

 # !elseif      - "if a .. elseif b endif" goes into "if a endif if b endif" - not ealy the same
 # what happens to the separate else clause? sorry
#s/!elseif/endif\n!if/i;
 #hence, this willbe unresolved
s/!elseif/--else!if/i;

s/!(endif|else|include)/$x=$1,$x=~y:A-Z:a-z:,$x/ie;        #remove the ! and go lowcase
##the above is the hard include
##soft include (only if exists) is gnu:-include, while nmake: if exists() ...

#s/!ifdef\s+(\w+)/ifneq "\$($1)" ""/i;
#s/!ifndef\s+(\w+)/ifeq "\$($1)" ""/i;
s/!(ifn?def)\s+(\w+)/$1 $2/i;

 # !if a==b
s/!if +("[^"]*") *== *("[^"]*")/ifeq $1 $2/i;   #or ifeq ($1,$2)
 # !if a!=b
s/!if +("[^"]*") *!= *("[^"]*")/ifneq $1 $2/i;

#######
 # !if exist(file)   # not vey sue if this below woks, anyway how you check fo (non)existing file?
#sub ifex() {   #$1=else; $2=!; both could be empty
#  local($x) = "if";
#  $x = "endif\n$x" if $_[0] =~ /^else$/i;
#  $x .= "n" if $_[1] ne '!';
#  $x .= 'eq "" "$(wildcard ';
#}
#if ( s/!(else)?if (!?)exists?\(/&ifex($1,$2)/ie

#if ( s/!if *exists?\(/ifneq "" "\$(wildcard/
#  || s/!if *!exists?\(/ifeq "" "\$(wildcard/
# ) { s/\)([^\)]*)$/)"$1/; }     #replace LAST ) on the line with )"

# !if exist(file) !include file !endif -> -include file (soft include)
if ($ifexis) {
  s/^/-/ if /^include/i;
  $ifexis = 0  if s/^(endif)/#$1/i;
}
#if ( s/^(!if *exists?\s*\(\s*)(\S+)/#$1$2/i ) {
if ( /^!if *exists?\s*\(/i ) {
  $ifexis++;#= $2;
  $_='#'.$_;
}


#######
### rules: a/b.c and a\b.c ae not the same!
 # {path}.c{path}.o     ##also swap them
 # { path  } . ext     { path  } .   ext
s,\{([^}]*)}\.([^.{]+)\{([^}]*)}\.([^.{ :]+) *:,$3/%.$4 : $1/%.$2,;
 # {path}.c.o
 #   path    . ext     .   ext
s,\{([^}]*)}\.([^.{]+)\.([^.{ :]+) *:,%.$3 : $1/%.$2,;
 # .c{path}.o
 # . ext     { path  } .   ext
s,\.([^.{]+)\{([^}]*)}\.([^.{ :]+) *:,$2/%.$3 : %.$1,;

 #^\ meaning this is not a line wrapping, but backslash - replace with forward shash
s,\^\\,/,;

 #var = xxx $(var) yyy   ->  var+= or var:=......; coz in gnu  = is flat!
if ( s/^(\s*)(\w+)(\s*)([:+])=\s*// ) {
        $x=$2; $y=$1.$2.$3.$4; $i=$4;
        if ($i eq '') { #normal assign only (if gnumakefiles are reprocessed)
              #look for single letter $X & longer $(XXX); also $(XXX:...)
           $i = (length($x)==1 && s/^\$$x// || s,^\$\($x\),,)  ? '+' :
                (length($x)==1 && /\$$x/ || /\$\($x\W/ )  ? ':' : '';
          }
        s/\s*$//;
        $_ = "$y$i= $_\n";

 s,\$(J|\(Jx\))\\,\$$1/,g;      # special case : revert slashes on $J/ $Jx/ ~~~
} else {
 s,\\,/,g if !/^\t/ ;           # revert slashes unless in a command/assignment
}

if (/^\t/ && s/@?<<\s*$//) {    # s/@?<<\s*$/"/)
  $inheredoc++;
}
if ($inheredoc) {               # (s/^<<.*/"/)
  if (s/^<<.*//) { $inheredoc =0; } else { s/\n$/ /; };
}

###########
print "-----" if /^!/;          #other ! things?
# u may use #ifdef's (commented ifdefs), which make wont get, but unifdef utility can

}   #comment
print;

#other things that wont work:
# x::y (additional dependencies) - may work as-is, may not
#       ... (additional rules)
# elseif
# if x && y, o any aithmetic
# @<< << tmpfiles replaced with whatever is inbetween, newlines go into spaces
# << << not touched

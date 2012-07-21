#!/usr/bin/perl -n
# this is a stupid script.
# dont put comments on lines with aliases with args, plz
# !#:2* and "..."'...' (concat'ed) not supported

# !! bash2.0 needs ending ; before } in func defs

binmode(STDOUT);
s/\r\n/\n/;
if (/\\!#?/ && !/^\s*#/) {         #not comment & has args
    s/^\s*al (\S+)\s+["']/$1() \t{ /;        #decl & remove start quote
    s/["']\s*(#[^"']*)?$/; } \1/;              #end quote+comment -> }+comment
    s/"?\\!#?:\*"?/"\$@"/g;     #replace args \!#:* or \!:*
    s/"?\\!#?:(\d)"?/"\$$1"/g;  #replace args \!#:* or \!:*
    die "-------at line $.:$_" if /\\!#/;
#   $_ .= "; }\n";
    $_ .= "\n";
}
print;
# vim:ts=4:sw=4:expandtab

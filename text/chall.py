#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

import sys, re
patrn,subst= sys.argv[1:3]
print( f'--{patrn}----{subst}--')
for a in sys.argv[3:]:
    t = open( a).read()
    t2,n = re.subn( patrn,subst, t)
    if n and t2 != t:
        print( ' >', a, ':', n)
        with open( a, 'w') as o:
            o.write( t2)
''' TODO
 re.flags
 "usage: changeall [-options] perl-expr-to-apply   files...."
."+\n read whole files and OVERWRITES them if matching"
."+\n perl_expr's can be almost anything (in quotes)"
."\n  (warning: ^ and $ ARE NOT start and end of line, but of file!)"
."\n -binary    write LF as LF, not CRLF"
."\n -pPREFIX   dont overwrite, outname=PREFIX+filename"
."\n -sSUFFIX   dont overwrite, outname=filename+SUFFIX"
~."\n -utf8 i/o"
~."\n -utf8all expr & i/o"
."\n -loop      apply over and over until no matches"
."\n  ask(strYes,strNo) func available - use as s/whatever/ask(\"..\",$&)/ge"

'''
# vim:ts=4:sw=4:expandtab

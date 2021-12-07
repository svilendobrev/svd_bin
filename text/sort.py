#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
'sensible replacement of /bin/sort.. with field-start being blank-to-nonblank, not the opposite..'

import sys
field = 0
ifile = None
for a in sys.argv[1:]:
    if field is None:   #taker
        field = int( a) -1
        assert field >= 0
        continue
    if a == '-k':
        field = None    #taker
        continue
    ifile = a
    break

import re
f = open( ifile) if ifile else sys.stdin
a = [ re.split( r'(\s+)', x) for x in f.readlines() ]
b = sorted( a, key = lambda x: x[ 2*field:] )
for y in b: print( *y, sep='',end='')

# vim:ts=4:sw=4:expandtab

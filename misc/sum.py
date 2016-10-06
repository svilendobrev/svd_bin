#!/usr/bin/env python
#$Id: sum.py,v 1.2 2006-09-27 12:54:13 sdobrev Exp $
from __future__ import print_function

import sys
s=0

def around(x): return round(x,5)

try:
    f = open( sys.argv[1] )
except IndexError:
    f = sys.stdin

for line in f:
    lr = line.strip().split('#',1)
    x = lr[0].strip()
    if not x:
        continue
    if x=='eof': break
    if '=' in x:
        if s: print( around(s), '=', x.split('=',1)[-1], '\n')
        s = 0
    else:
        e = around(eval(x))
        print( ':',x,'\t=',e, ':', ''.join( lr[1:]))
        s+= e
if s: print( around(s) )

# vim:ts=4:sw=4:expandtab

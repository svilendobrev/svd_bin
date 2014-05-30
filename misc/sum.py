#!/usr/bin/env python
#$Id: sum.py,v 1.2 2006-09-27 12:54:13 sdobrev Exp $
from __future__ import print_function

import sys
s=0
n=0

try:
    f = file( sys.argv[1] )
except IndexError:
    f = sys.stdin

for line in f:
    lr = line.strip().split('#',2)
    x = lr[0].strip()
    if not x:
        continue
    if x=='eof': break
    if '=' in x:
        if n: print( s)
        s = 0
        n=0
    else:
        e = eval(x)
        print( ':',x,'=',e, lr[-1])
        s+= e
        n+=1
if n: print( s)

# vim:ts=4:sw=4:expandtab

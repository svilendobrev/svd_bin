#!/usr/bin/env python
#$Id: sum.py,v 1.2 2006-09-27 12:54:13 sdobrev Exp $
from __future__ import print_function

import sys,os
ss=s=0
ROUND = os.environ.get('ROUND', '')
try: ROUND=int(ROUND)
except: ROUND=3
def around(x):
    if not ROUND: return int(x)
    return round(x,ROUND)

HASH= os.environ.get('HASH', '')

NAME1= os.environ.get('NAME1', '')

try:
    f = open( sys.argv[1] )
except IndexError:
    f = sys.stdin

for line in f:
    lr = line.strip()
    if not lr: continue
    lr = lr.split( '#' if HASH else None)
    x = lr.pop(0).strip()
    if not x or x[0] == '#': continue
    if x=='eof': break
    if '==' in x:
        if ss: print( around(ss), '=', x.split('=',1)[-1], '\n')
        ss = 0
    elif '=' in x:
        if s: print( around(s), '=', x.split('=',1)[-1], '\n')
        s = 0
    else:
        if NAME1:
            name = x
            x = lr[0]
            lr[0] = name
        r = ' '.join( lr)
        e = around(eval(x))
        print( ':',x.ljust(15),'=', e, ':', r)
        s+= e
        ss+= e
if s: print( around(s) )

# vim:ts=4:sw=4:expandtab

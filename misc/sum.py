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
try:
    f = open( sys.argv[1] )
except IndexError:
    f = sys.stdin

for line in f:
    lr = line.strip().split( '#' if HASH else None, 1)
    x = lr[0].strip()
    if not x:
        continue
    if x=='eof': break
    if '==' in x:
        if ss: print( around(ss), '=', x.split('=',1)[-1], '\n')
        ss = 0
    elif '=' in x:
        if s: print( around(s), '=', x.split('=',1)[-1], '\n')
        s = 0
    else:
        e = around(eval(x))
        print( ':',x.ljust(15),'=', e, ':', ''.join( lr[1:]))
        s+= e
        ss+= e
if s: print( around(s) )

# vim:ts=4:sw=4:expandtab

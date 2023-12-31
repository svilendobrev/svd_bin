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
    line = line.strip()
    if not line or line[0] == '#': continue
    lr = line.split( '#' if HASH else None)
    x = lr.pop(0).strip()
    if not x or x[0] == '#': continue
    if x == 'eof': break
    if '==' == x[:2]:
        if s: print( '=', around(s) )
        if ss: print( '==', around(ss), ':', line.split('=',1)[-1].strip(), '\n')
        ss = s = 0
    elif '=' == x[0]:
        if s: print( '=', around(s), ':', line.split('=',1)[-1].strip(), '\n')
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
if s and s!=ss: print( '=', around(s) )
if ss: print( '==', around(ss) )

# vim:ts=4:sw=4:expandtab

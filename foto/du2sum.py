#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''use: du -a -k | this.py k
sums size of j2jrecompressed images and the original
'''
from __future__ import print_function #,unicode_literals
import os.path, sys
from collections import defaultdict
sums = defaultdict( lambda : defaultdict( int) )
sumstotal = defaultdict( int )
counts = defaultdict( int)

unit = sys.argv and sys.argv[1]
if unit not in 'kmb': unit = ''

import re
for l in sys.stdin:
    l = l.strip()
    if not l: continue
    size,name = l.split(None,1)
    size = int(size)
    if not size: continue
    if os.path.islink( name): continue
    name,ext = os.path.splitext( name)
    if ext.lower() != '.jpg': continue
    path,name = os.path.split( name)
    m = re.search( '.jpg.r(medium|high|low|veryhigh)(\d*)', name)
    if m:
        kind = m.group(1)+m.group(2)
        name = name[ :m.start() ]
    else: kind = 'total'
    sums[ '/'+path+'/'+name ][ kind ] += size
    sums[ path][ kind ] += size
    sumstotal[ kind] += size
    counts[ kind] += 1

total = sumstotal['total']
for k,v in sorted( sumstotal.items()):
    print( f'{k:10}{v:-10,}', unit, total and f'{v/total:.2f}', 'n=', counts[k], )
#print( counts)
#import pprint
#pprint.pprint( sumstotal)

for k,v in sorted( sums.items()):
    if k[0] != '/': continue
    if len( v) <=3:
        print( k[1:], v)

# vim:ts=4:sw=4:expandtab

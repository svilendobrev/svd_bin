#!/usr/bin/env python
# -*- coding: utf-8 -*-

tx = '''
/comptrucktype  /trucks
'''

import sys
files = sys.argv[1:]
fa = [open(a).readlines() for a in files]
fb = [ [x.split() for x in y] for y in fa]
zz = [0] * len( files)

__tx = [ x.split() for x in tx.strip().split('\n') ]
def _tx( x):
    for (f,t) in __tx:
        x = x.replace(f,t)
    return x

mm={}
for i,y in enumerate( fb):
    for x in y:
        mm.setdefault( _tx( x[1]), list( zz) )[ i] = int(x[0])

#dd = dict( (k,(v[1]-v[0]) if len(v)==2 else v[0]) for k,v in mm.items() if len(v)<2 or v[0]!=v[1])
dd = dict( (k,(v[1]-v[0])) for k,v in mm.items() if v[0]!=v[1])

from pprint import pprint
pprint(dd)

print( sum(dd.values()))

# vim:ts=4:sw=4:expandtab

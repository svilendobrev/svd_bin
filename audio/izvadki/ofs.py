#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,re
renum = re.compile( '^ *([\d.]+)? *- *([\d.]+)?')
ofs = float( sys.argv[1])

def repl( m):
    r = ''
    o = 0
    for i,g in enumerate( m.groups(), 1):
        s,e = m.start(i), m.end(i)
        if s<0: continue
        r += m.string[ o: s]
        v = float( g) - ofs
        if int(v)==v:v = int(v)
        r += str( v)
        o = e #m.string[m.start(g):m.end(g)]
    r += m.string[ o: ]
    return r

for a in sys.stdin:
    a = a.rstrip()
    print renum.sub( repl, a, 1 )

# vim:ts=4:sw=4:expandtab

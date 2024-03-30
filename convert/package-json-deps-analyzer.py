#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

'''
given list of ./*/package.json paths, produce usage map of dependencies' package vs list of projects
'''

import sys,json, traceback, pprint, collections
VERBOSE = 0
usage = {}
for a in sys.stdin: #list of ./*/package.json paths..
    a = a.strip()
    if VERBOSE: print( '===', a)
    try:
        p = json.load( open(a))
    except:
        print( '????', a)
        traceback.print_exc()
        continue
    d = p.get( 'dependencies')
    if VERBOSE: pprint.pprint( d)
    #a = a.replace( '-private/', '/')
    a = a.replace( '/package.json','')
    if a[:2] == './': a = a[2:]
    for k in d or ():
        usage.setdefault( k, []).append( a)

if VERBOSE: print( '====='*4)
for k,v in sorted( usage.items()):
    v = [ p.split('/')[-1]
            for p in v
            if p.split('/')[1].replace( '-private', '') not in usage
            and p.split('/')[0] != 'gh'
               #'-private/' not in p
               # or p.replace( '-private/', '/').replace( 'mydir', 'gh') not in v
               # and p.replace( '-private/', '/').replace( './mydir/', '') not in usage
        ]
    if v:
        print( k.ljust( 35), *v)

# vim:ts=4:sw=4:expandtab

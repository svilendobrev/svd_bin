#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
join = os.path.join

from svd_util import optz
optz.help( 'apply moves-around-dirs/deletes from template/ into .')
optz.bool( 'real', '-y', )
optz.list( 'exclude', help= 'dirs', default= [] )
optz.list( 'ignore' , help= 'file-names', default= [])
optz.bool( 'dup2ignore' , help= 'ignore duplicates')
optz,args = optz.get()
none = not optz.real

template = args[0].rstrip('/')

from collections import defaultdict
tree = {}
paths = set()

try: os.mkdir( 'del')
except Exception as e: print( e)

optz.exclude = [ a.rstrip('/') for a in optz.exclude ]
errdup = set()
for path, dirs, files in os.walk( template ):
    subpath = path[ len(template): ].lstrip('/').split( '/')
    p = join( *subpath[:] )
    if p in optz.exclude:
        dirs[:] = []
        continue
    paths.add( p)
    dirs.sort()
    files.sort()
    for name in files:
        if name in optz.ignore: continue
        if name in tree:
            print( '=', name, path, tree[ name])
            errdup.add( name)
        #assert name not in tree, (name, path, tree[ name])
        if 0:
            tp = tree.setdefault( name, [])
            tp.append( p )
            if len(tp)>1:
                lcur = os.path.getsize( join( path, name) )
                lprev = os.path.getsize( join( template, tp[-2], name) )
                assert lcur==lprev, (lcur, lprev)
        else:
            tree[ name] = p
        #print( pp,name)

errdup = sorted( errdup)
if optz.dup2ignore:
    optz.ignore += errdup
else:
    assert not errdup, errdup

if not none:
    for p in paths:
        try: os.makedirs( p)
        except : pass

for path, dirs, files in os.walk( '.' ):
    if path == '.':
        try: dirs.remove( template )
        except: pass
    else:
        subpath = path.split( '/')
        p = join( *subpath[1:] )
        if p in optz.exclude:
            dirs[:] = []
            continue
    dirs.sort()
    files.sort()
    for name in files:
        if name in optz.ignore: continue
        if name not in tree:
            print( 'deleted', name)
        target = tree.get( name, 'del' )
        if not target:
            if '.' == path: continue
        else:
            if join( '.', target) == join( path):
                continue
        a = join( path, name )
        b = join( target, name)
        print( a, '>', b)
        if not none: os.rename( a,b)

if none: print( '-y to apply for real')

# vim:ts=4:sw=4:expandtab

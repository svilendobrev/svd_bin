#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function #,unicode_literals
'apply moves-around-dirs/deletes from template/ into .'

import os
join = os.path.join

from svd_util import optz
optz.bool( 'real', '-y', )
optz.append( 'exclude', help='dirs', default= [] )
optz.append( 'ignore' , help='file-names', default= [])
optz,args = optz.get()
none = not optz.real

template = args[0].rstrip('/')

tree = {}
paths = set()

try: os.mkdir( 'del')
except Exception as e: print( e)

optz.exclude = [ a.rstrip('/') for a in optz.exclude ]

for path, dirs, files in os.walk( template ):
    subpath = path[ len(template): ].lstrip('/').split( '/')
    p = join( *subpath[:] )
    if p in optz.exclude:
        dirs[:] = []
        continue
    paths.add( p)
    for name in files:
        if name in optz.ignore: continue
        assert name not in tree, (name, path)
        tree[ name] = p
        #print( pp,name)

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

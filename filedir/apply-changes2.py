#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
join = os.path.join

from svd_util import optz
optz.help( 'apply moves-around-dirs/deletes from template/ into .')
optz.bool( 'real', '-y', )
optz.text( 'exclude', '-x', help= 'regexp',)
optz.list( 'ignore' , '-i', help= 'file/dir-names', default= [])
optz.bool( 'nosymlinks' ,   help= 'ignore symlinks')
optz.bool( 'alsodirs' , help= 'check moving of dirs too')
optz.bool( 'onlydirs' , help= 'check moving of dirs ONLY')
optz.bool( 'dup2ignore' , help= 'ignore duplicates')
optz.text( 'deldir' , default='del', help= 'folder to move deleted items into [%default]')
optz.bool( 'nodelete' , help= 'dont delete, only move')
optz,args = optz.get()
none = not optz.real

template = args[0].rstrip('/')

from collections import defaultdict
tree = {}
paths = set()

try: os.mkdir( 'del')
except Exception as e: print( e)

#optz.exclude = [ a.rstrip('/') for a in optz.exclude ]
exclude = None
if optz.exclude:
    import re
    print( 'excluding:', optz.exclude)
    exclude = re.compile( optz.exclude)
errdup = set()

#TODO ignore path==optz.deldir if optz.alsodirs
if optz.ignore:
    print( 'ignoring:', *optz.ignore)

def ignore( path, name):
    pathname = join( path, name)
    return exclude and exclude.search( pathname) or name in optz.ignore or optz.nosymlinks and os.path.islink( pathname)

def dirsfiles( path, dirs, files):
    #dirs0 = dirs[:]
    dirs = sorted( name for name in dirs if not ignore( path, name) )
    #files0 = files[:]
    files = sorted( name for name in files if not ignore( path, name) )
    return dirs,files

for path, dirs, files in os.walk( template, followlinks= False ):
    subpath = path[ len(template): ].lstrip('/').split( '/')
    p = join( *subpath[:] )
    if 0:   #XXX
     if exclude and exclude.search( p):
        if 0: print( 'pexclude', p)
        dirs[:] = []
        continue

    paths.add( p)
    #dirs, files = dirsfiles( path, dirs, files)   #no-no XXX ..2: walk all, but tree-index only non-ignorables
    if optz.alsodirs or optz.onlydirs:
        for name in dirs:
            if ignore( path, name): continue    #XXX only index non-ignorables

            if name in tree:
                print( '=', name+'/', path, tree[ name])
                errdup.add( name)
            tree[ name] = p

    if not optz.onlydirs:
      for name in files:
        if ignore( path, name): continue    #XXX only index non-ignorables

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

if 0: #not none:
    for p in paths:
        try: os.makedirs( p)
        except : pass

for path, dirs, files in os.walk( '.', topdown= False):
    if path == '.':
        try: dirs.remove( template )
        except: pass
    else:
        subpath = path.split( '/')
        p = join( *subpath[1:] )
        if 0:   #XXX
         if exclude and exclude.search( p):
            if 0: print( '2pexclude', p)
            dirs[:] = []
            continue

    subpath = path.split( '/')
    anymatch = set(subpath) & set(tree)

    #dirs, files = dirsfiles( path, dirs, files)
    for name in bool(not optz.onlydirs) * files + bool(optz.alsodirs or optz.onlydirs) * dirs:
        if ignore( path, name): continue    #XXX only lookup non-ignorables

        target = tree.get( name, optz.deldir )
        if not target:
            if '.' == path: continue
        else:
            if join( '.', target) == join( path):
                continue

        #TODO if path/name -> target/name comes from  path -> target : continue
        if 0 and anymatch: #any( p in tree for p in subpath):   #XXX
            print( '!ignoring existing file/dir in tree for', name, target, anymatch , subpath )#, p, tree[p])
            continue
        deleting = name not in tree
        if 10 and deleting:
            if optz.nodelete:
                print( 'not-deleting', name)
                continue
            print( 'deleting', name)

        a = join( path, name )
        b = join( target, name)
        print( deleting and '-del' or '', a, ' '* (10 - len(a) % 10), '>', b)
        if not none:
            os.makedirs( target, exist_ok= True)
            os.rename( a,b)

if none: print( '-y to apply for real')

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os,sys, re

class DictAttr( dict):
    def __init__( me, *a, **k):
        dict.__init__( me, *a, **k)
        me.__dict__ = me
    def __hash__( me): return hash( (me.path, me.size) )

import optparse
oparser = optparse.OptionParser( '%prog [options] dir1 dir2' )
def optany( name, *short, **k):
    return oparser.add_option( dest=name, *(list(short)+['--'+name.replace('_','-')] ), **k)
def optbool( name, *short, **k):
    return optany( name, action='store_true', *short, **k)
optbool( 'nosize', default= bool( os.environ.get( 'NOSIZE')), help= 'ignore size diffs')
optbool( 'byname',  help= 'sort by name, not dir')
optbool( 'convert', help= 'show moves/deletes needed to convert dir1 to dir2, by-name')
optany(  'exclude', '-x',   help= 'regexp to exclude/ignore files')
optany(  'wexclude', '-w',  help= 'space-separated-list of patterns to be |-joined into exclude regex')
optbool( 'same',            help= 'show same/similar things instead of differences')
optbool( 'nosymlink',       help= 'dont follow symlink dirs = no dereference')
optbool( 'symtext', '-t',   help= 'compare symlinks as text, no dereference')
optbool( 'timestamps'   ,   help= 'compare timestamps too')
optbool( 'nodirs'       ,   help= 'do not show dirs')
optbool( 'noexcluded_count', help= 'do not show excluded counts')
optbool( 'nocount',         help= 'do not show counts any')
optz,args = oparser.parse_args()
if len(args)<2:
    oparser.error('compare what?')

#import locale
#fenc = locale.getpreferredencoding()
##eutf.e_utf_stdout() and 'utf-8' or

ignore = None
if optz.wexclude:
    assert not optz.exclude
    optz.exclude = '('+'|'.join( optz.wexclude.split())+')'
if optz.exclude:
    print( 'excluding:', optz.exclude)
    ignore = re.compile( optz.exclude)

def outsymlink( fp,f):
    link = os.readlink( fp)
    return DictAttr( size= '<>', path= fp.ljust(20) + ' -> ' + link, name= f)

from os.path import join, getsize, islink, dirname

#if optz.timestamps:
#    os.stat_float_times( False)
# XXX fat* has time-resolution of 2s !  so odd-second times will be always newer..

def files( root):
    c = os.getcwd()
    os.chdir( root )
    o = []
    odirs = {}
    def dirify( fp, item =None):
        levels = fp.split('/')
        if levels: levels.pop()
        while levels:
            dir = odirs.get( '/'.join( levels))
            if dir:
                if item:
                    dir.files.append( item )
                dir.files_all_count += 1
            levels.pop()

    for root, dirs, files in os.walk( '.', followlinks= not optz.nosymlink):
        for f in sorted( files):
            fp = join( root, f)
            if ignore and ignore.search( fp):
                dirify( fp)
                continue
            #fp = fp.decode( fenc)
            if optz.symtext and islink( fp):
                item = outsymlink( fp,f)
            else:
                sz = '##'
                if not optz.nosize:
                    try: sz = getsize( fp)
                    except Exception as e: print( e)
                if optz.timestamps:
                    sz = (sz, os.stat( fp).st_mtime)
                item = DictAttr( size= sz, path= fp, name= f)
            o.append( item)
            dirify( fp, item)
        dd = []
        for f in sorted( dirs):
            fp = join( root, f)
            if ignore and ignore.search( fp):
                dirify( fp)
                continue
            if optz.symtext and islink( fp):
                item = outsymlink( fp,f)
                o.append( item)
            else:
                dd.append(f)
                item = DictAttr( size= '/', path= fp, name= f, dir= True, files= [], files_all_count= 0)
                o.append( item)
                odirs[ fp ] = item
            dirify( fp, item)
        dirs[:] = dd

    os.chdir( c)
    if optz.convert:
        r = {}
        for x in o:
            r.setdefault( x.name, set() ).add( x)
#
#            else:
#                print( '''
#!!!! %s repeats:
# %s
# %s
#'''.strip() % (x.name, x.path, r[ x.name ].path) )
#        assert len( r) == len(o)
        return r

    return o, odirs

def item_as_text( x):
    r = DictAttr( x)
    r.count = ''
    n_all = x.get('files_all_count')
    if n_all:
        n_files = len( x.files)
        r.count = f' :: {n_files}'
        if not optz.noexcluded_count:
            n_diff = n_all - n_files
            if n_diff: r.count += f' +{n_diff}'
    if x.get('dir'):
        r.name +='/'
        r.path +='/'
    r.dir = dirname( x.path)
    return r

def textify( o):
    if optz.byname:
        o.sort( key= lambda x: (x.name,x.path,x.size) )
        format = '%(name)16s %(size)16s %(dir)s'
    else:
        o.sort( key= lambda x: (x.path,x.size) )
        format = '%(size)16s %(path)s'
    if not optz.nocount: format+= '%(count)s'
    return [ format % item_as_text( x) for x in o ]

a1   = args[0]
a2   = args[1]

#print '<', a1
#print '>', a2

import difflib
f1,f2 = files( a1), files( a2)
if not optz.convert:
    def parent_dir_missing( f, dirs, dirs_other):
        for p,d in dirs.items():
            if p not in dirs_other:
                for x in d.files:
                    x.parent_dir_missing = True
        return textify( [x for x in f if not x.get('parent_dir_missing')])
    f1,dirs1 = f1
    f2,dirs2 = f2
    #from pprint import pprint
    #pprint( sorted(dirs1))
    #pprint( sorted(dirs2))
    f1 = parent_dir_missing( f1, dirs1, dirs2)
    f2 = parent_dir_missing( f2, dirs2, dirs1)

    if optz.same:
        for l in difflib.ndiff( f1,f2):
            if l.startswith('  '): print( l)
    else:
        diff = difflib.unified_diff
        for l in diff( f1,f2, a1,a2, lineterm=''):
            try:
                print( l)
            except: print( repr(l))
else:
    ypaths = set()
    for name,x in sorted( f1.items()): #, key= lambda i: i[0].path):
        y = f2.get( name)
        if not y:               #deleted
            for i in x:
                print( 'rm', i.path )
        elif y == x: continue   #same
        else:
            xy = x & y
            #yy = y
            #xx = x
            y = y - xy
            x = x - xy
            if 1 == len( x) == len( y): #remains one diff = move
                x = list(x)[0]
                y = list(y)[0]
                ypath = dirname( y.path)
                #os.makedirs( ypath, exist_ok= True)
                if ypath not in ypaths:
                    print( 'mkdir -p', ypath )
                    ypaths.add( ypath )
                print( 'mv', x.path, y.path )
            else:
                if y <= x:      #remains subset = deleted
                    for i in x - y:
                        print( 'rm', i.path )
                else:
                    print( '#??? repeats', name)
                    for i in x:
                        print( '# ?-', i.path, i.size )
                    for i in y:
                        print( '# ?+', i.path, i.size )

    for name,y in sorted( f2.items()):
        if name not in f1:
            for i in y:
                print( '#??? add', i.path )


# vim:ts=4:sw=4:expandtab

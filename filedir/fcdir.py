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
optbool( 'convert', help= 'show moves/deletes to convert dir1 to dir2, by-name')
optany(  'exclude', '-x',   help= 'regexp to exclude/ignore files')
optbool( 'same',            help= 'show same/similar things instead of differences')
optbool( 'nosymlink',       help= 'dont follow symlink dirs = no dereference')
optbool( 'symtext', '-t',   help= 'compare symlinks as text, no dereference')
optz,args = oparser.parse_args()
if len(args)<2:
    oparser.error('compare what?')

#import locale
#fenc = locale.getpreferredencoding()
##eutf.e_utf_stdout() and 'utf-8' or

ignore = None
if optz.exclude:
    print( 'excluding:', optz.exclude)
    ignore = re.compile( optz.exclude)

def outsymlink( fp,f):
    link = os.readlink( fp)
    return DictAttr( size= '<>', path= fp.ljust(20) + ' -> ' + link, name= f)

from os.path import join, getsize, islink, dirname

def files( root):
    c = os.getcwd()
    os.chdir( root )
    o = []
    for root, dirs, files in os.walk( '.', followlinks= not optz.nosymlink):
        for f in files:
            fp = join( root, f)
            if ignore and ignore.search( fp): continue
            #fp = fp.decode( fenc)
            if optz.symtext and islink( fp):
                item = outsymlink( fp,f)
            else:
                sz = '##'
                if not optz.nosize:
                    try: sz = getsize( fp)
                    except Exception as e: print( e)
                item = DictAttr( size= sz, path= fp, name= f)
            o.append( item)
        dd = []
        for f in dirs:
            fp = join( root, f)
            if optz.symtext and islink( fp):
                item = outsymlink( fp,f)
                o.append( item)
            else: dd.append(f)
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

    if optz.byname:
        o.sort( key= lambda x: (x.name,x.path,x.size) )
        o = [ '%(name)16s %(size)16s %(path)s' % dict( x, path= dirname( x.path))
                for x in o ]
    else:
        o.sort( key= lambda x: (x.path,x.size) )
        o = [ '%(size)16s %(path)s' % x for x in o ]
    return o

a1   = args[0]
a2   = args[1]

#print '<', a1
#print '>', a2

import difflib
f1,f2 = files( a1), files( a2)
if not optz.convert:
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os,sys, re

import optparse
oparser = optparse.OptionParser( '%prog [options] dir1 dir2' )
def optany( name, *short, **k):
    return oparser.add_option( dest=name, *(list(short)+['--'+name.replace('_','-')] ), **k)
def optbool( name, *short, **k):
    return optany( name, action='store_true', *short, **k)
optbool( 'nosize', default= bool( os.environ.get( 'NOSIZE')), help= 'ignore size diffs')
optany(  'exclude', '-x',   help= 'regexp to exclude/ignore files')
optbool( 'same',            help= 'show same/similar things instead of differences')
optbool( 'nosymlink',       help= 'dont follow symlink dirs = no dereference')
optbool( 'symtext', '-t',   help= 'compare symlinks as text, no dereference')
optz,args = oparser.parse_args()
if len(args)<2:
    oparser.error('compare what?')

import locale
fenc = locale.getpreferredencoding()
#eutf.e_utf_stdout() and 'utf-8' or

ignore = None
if optz.exclude:
    print( 'excluding:', optz.exclude)
    ignore = re.compile( optz.exclude)

def outsymlink( fp):
    link = os.readlink( fp)
    return '<>', fp.ljust(20) + ' -> ' + link

from os.path import join, getsize, islink
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
                item = outsymlink( fp)
            elif not optz.nosize:
                try:
                    sz = getsize( fp)
                except Exception as e:
                    print( e)
                    sz = '##'
                item = sz,fp #'%16s ' % sz + fp
            o.append( item)
        dd = []
        for f in dirs:
            fp = join( root, f)
            if optz.symtext and islink( fp):
                item = outsymlink( fp)
                o.append( item)
            else: dd.append(f)
        dirs[:] = dd

    os.chdir( c)
    if optz.nosize:
        o.sort()
    else:
        o.sort( key= lambda x: x[1])
        o = [ '%16s %s' % szfp for szfp in o ]
    return o

a1   = args[0]
a2   = args[1]

#print '<', a1
#print '>', a2

import difflib
f1,f2 = files(a1), files( a2)
if optz.same:
    for l in difflib.ndiff( f1,f2):
        if l.startswith('  '): print( l)
else:
    diff = difflib.unified_diff
    for l in diff( f1,f2, a1,a2, lineterm=''):
        print( l)

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
#$Id$
# -*- coding: utf-8 -*-
import os,sys, re

import optparse
oparser = optparse.OptionParser( '%prog [options] dir1 dir2' )
def optany( name, *short, **k):
    return oparser.add_option( dest=name, *(list(short)+['--'+name.replace('_','-')] ), **k)
def optbool( name, *short, **k):
    return optany( name, action='store_true', *short, **k)
optbool( 'nosize', default= bool( os.environ.get( 'NOSIZE')), help= 'ignore size diffs')
optany(  'exclude', '-x', help= 'regexp to exclude/ignore files')
optbool( 'same',   help= 'show same/similar things instead of differences')
optbool( 'nosymlink', help= 'dont follow symlink dirs')
options,args = oparser.parse_args()
if len(args)<2:
    oparser.error('compare what?')

import locale
fenc = locale.getpreferredencoding()
#eutf.e_utf_stdout() and 'utf-8' or

ignore = None
if options.exclude:
    print 'excluding:', options.exclude
    ignore = re.compile( options.exclude)

from os.path import join, getsize
def files( root):
    c = os.getcwd()
    os.chdir( root )
    o = []
    for root, dirs, files in os.walk( '.', followlinks= not options.nosymlink):
        for f in files:
            fp = join( root, f)
            if ignore and ignore.search( fp): continue
            #fp = fp.decode( fenc)
            if not options.nosize:
                try:
                    sz = getsize( fp)
                except Exception, e:
                    print e
                    sz = '##'
                fp = sz,fp #'%16s ' % sz + fp
            o.append( fp)
    os.chdir( c)
    if options.nosize:
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
if options.same:
    for l in difflib.ndiff( f1,f2):
        if l.startswith('  '): print l
else:
    diff = difflib.unified_diff
    for l in diff( f1,f2, a1,a2, lineterm=''):
        print l

# vim:ts=4:sw=4:expandtab

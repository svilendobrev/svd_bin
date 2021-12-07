#!/usr/bin/env python
from __future__ import print_function

from svd_util import optz
import os
from os.path import *
issymlink = islink

optz.description( 'move/link real-source-of-symlink into elsewhere')
optz.bool( 'mv', help='do move, default is (hard)link')
#optz.bool( 'cp', help='do copy, default is (hard)link')
optz.bool( 'fake',    '-n', help='do nothing')
optz.bool( 'deldest', '-f', help='delete destname before acting')
optz.bool( 'quiet', '-q', )
optz.bool( 'srcname', help='use link-target-name instead of link-name itself')
optz.bool( 'dellink', help='delete symlink after acting')
optz.bool( 'absshow', help='only show abs resolved paths')
optz,args = optz.get()
optz.verbose = not optz.quiet

if not optz.absshow:
    if len(args)==1:
        raise RuntimeError( 'last arg must be target dir/filename')
    dest = args.pop()
    destdir = os.path.isdir( dest )
    if len(args)>2 and not destdir:
        raise RuntimeError( 'last arg must be dir')
func = os.link
if optz.mv: func = os.rename
#elif optz.cp: func = copytree  TODO from cp_filtered.py

for a in args:
    if not issymlink( a):
        #if optz.verbose:
        print( '... non-symlink', a)
        continue
    f = realpath(a)
    if optz.absshow:
        print( a, '->', f)
        continue
    if destdir:
        destname = basename( f if optz.srcname else a )
        destfull = join( dest, destname)
    else:
        destfull = dest

    if exists( destfull) and not issymlink( destfull) and f == realpath( destfull):
        if optz.verbose: print( '-same', a)
        continue
    if optz.deldest and exists( destfull):
        if optz.verbose: print( 'del', destfull)
        if not optz.fake: os.remove( destfull)
    if optz.verbose: print( func.__name__, f, destfull)
    if not optz.fake:
        func( f, destfull)
        if optz.dellink and realpath( a) != realpath( destfull): #not just arrived from moving
            os.remove( a)
            ''' if realpath... because of edge case:
            link-name (a) is same as (pointed-to) destname, and target dir stays same
              x/somename -> ../../somename
            this also needs --deldest
            '''
# vim:ts=4:sw=4:expandtab

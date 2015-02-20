#!/usr/bin/env python
from __future__ import print_function

from svd_util import optz
import os
from os.path import *
issymlink = islink

optz.description( 'move/link real-target-of-symlink into elsewhere')
optz.bool( 'mv', help='do move, default is (hard)link')
optz.bool( 'fake',   '-n', help='do nothing')
optz.bool( 'delete', '-f', help='delete before acting')
optz.bool( 'quiet', '-q', )
optz,args = optz.get()
optz.verbose = not optz.quiet
if len(args)==1:
    raise RuntimeError( 'last arg must be target dir/filename')
dest = args.pop()
destdir = os.path.isdir( dest )
if len(args)>2 and not destdir:
    raise RuntimeError( 'last arg must be dir')

func = optz.mv and os.rename or os.link
for a in args:
    if not issymlink( a):
        #if optz.verbose:
        print( '... non-symlink', a)
        continue
    f = realpath(a)
    if destdir:
        destname = basename( a )
        destfull = join( dest, destname)
    else:
        destfull = dest

    if exists( destfull) and not issymlink( destfull) and f == realpath( destfull):
        if optz.verbose: print( '-same', a)
        continue
    if optz.delete and exists( destfull):
        if optz.verbose: print( 'del', destfull)
        if not optz.fake: os.remove( destfull)
    if optz.verbose: print( func.__name__, f, destfull)
    if not optz.fake: func( f, destfull)

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import os, sys

def opt( *xx):
    for x in xx:
        if x in sys.argv: return sys.argv.remove( x ) or True
    return None

follow_symlinks = opt( '-L', '--follow', '--dereference')

#on FAT or FAT32 file systems, st_mtime has 2-second resolution, and st_atime has only 1-day resolution.
#so odd times will always appear newer than the FAT-copy
#hence: make them all even

def evenit(f):
    st = os.stat( f, follow_symlinks= follow_symlinks)
    mtime = st.st_mtime
    mtime_even = 2 * (mtime // 2)
    #mtime &= ~1
    if mtime_even != mtime:
        print( f, mtime, mtime_even)
        os.utime( f, ( mtime_even, mtime_even), follow_symlinks= follow_symlinks)

#paths will be walked down

for f in sys.argv[1:]:
    if not os.path.isdir( f):
        evenit( f)
        continue
    for root, dirs, files in os.walk( f, followlinks= follow_symlinks):
        for x in files:
            evenit( os.path.join( root, x))

# vim:ts=4:sw=4:expandtab

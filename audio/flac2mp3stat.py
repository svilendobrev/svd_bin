#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys
import glob
def aset( ext):
    return set( a[:-len(ext)] for a in glob.glob( pfx+'/hb*/*'+ext))
for pfx in sys.argv[1:] or ['.']:
    flacs= aset( '.flac')
    if not flacs: continue
    mp3s = aset( '.mp3')
    print( f'{pfx}\t: flacs: {len(flacs)} \t mp3s: {len(mp3s)} = {100*len(mp3s)/len(flacs):.0f}%')

# vim:ts=4:sw=4:expandtab

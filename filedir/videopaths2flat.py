#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys,os,re
from svd_util import optz

optz.help( 'find all video files under argument[s] and symlink as flat-filenames into . (replacing / with :)')
optz.bool( 'real', '-y', help='do it')
optz.bool( 'follow_symlinks', )
optz.str(  'exclude', help= 'regexp to exclude filepaths')
optz,argz = optz.get()

print( 'dirs:', argz)
ignore = None
if optz.exclude:
    print( 'excluding:', optz.exclude)
    ignore = re.compile( optz.exclude)

exts = 'mov mkv mp4 avi 3gp'.lower().split()
def walk( roots, followlinks =optz.follow_symlinks, exts =exts):
    for root in roots:
        for path,dirs,files in os.walk( root, followlinks= followlinks):
            for f in files:
                fpath = os.path.join( path, f)
                if ignore and ignore.search( fp): continue
                #'name', '.ext'
                if os.path.splitext(f)[-1][1:].lower() in exts:
                    yield fpath

def do( afrom, bto):
    print( afrom, ':>', bto)
    if optz.real: os.symlink( afrom, bto)


del_dir= '''
    snimki
    video
    видео
    telefoni-tableti
    nashi
    наши-цифрови
'''.split()
replace_as_dot= '''
    .mp4..
    .mov..
'''.split()
for a in walk( argz):
    a = a.strip()
    b = a.replace('//','/')
    for p in del_dir:
        b = b.replace( '/'+p+'/','/')
    b = b.replace('/',':')
    for p in replace_as_dot:
        b = b.replace( p,'.')
    b = ':'+b.strip(':.')
    do( a, b)

# vim:ts=4:sw=4:expandtab

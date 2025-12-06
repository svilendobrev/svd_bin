#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
''' joflac [separator-piece1 [separator-piece2..]]
    separator-piece = име на файл в текущата директория, който започва нова част
        или (уникална) част от такова име за да не се пише цялото (напр. 05)
'''

import sys, subprocess, os, re
doit = 0
try: sys.argv.remove('-n')
except: doit=1

def call( *args, **ka):
    print( args)
    if doit:
        return subprocess.run( *args, **ka)

parts = [[]]
for f in sorted( os.listdir()):
    if not f.endswith(('.mp3','.flac', '.ogg', '.aac')): continue
    if f in sys.argv: parts.append([])
    elif sys.argv:
        for a in sys.argv:
            if a in f:
                parts.append([])
                break
    parts[-1].append( f)

names = [ chr(x) for x in range(ord('a'),ord('z')+1)] #'abcdefgh'
outs = []
for pp,name in zip( parts, names):
    out = name+'.wav'
    outs.append( name)
    r = call( [ 'sox', *pp, out, 'stat' ], text=True, stdout= subprocess.PIPE, stderr=subprocess.STDOUT )
    if r:
        for l in r.stdout.splitlines():
            if l.startswith( ('sox', 'Length')):
                print( ' >', re.sub( r'\.\d+', '', l ).replace( '(seconds):', 's: >>>>>' ))
    #if pp[0].endswith('mp3'):
    #    call( 'mpg123 -q --no-control -w'.split() + [ out, *pp ])
    #else:
    #    call( 'shntool join -o wav -a'.split() + [ name, *pp ])

call( 'make -f ~/src/bin/audio/makefile Q=4'.split() + [ o+'.mp3' for o in outs])

# vim:ts=4:sw=4:expandtab

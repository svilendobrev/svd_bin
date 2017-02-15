#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys, subprocess, argparse
ap = argparse.ArgumentParser( description= '''\
 изтрива .wav файлове (входящи), за които има еквивалентни .flac ;
 т.е. такива със същото име (или с добавени междинни .wav или .out,
 като междинен .org във входящото име се игнорира)
 и със същата продължителност +/- 0.4с
''', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
def apbool(*a,**ka): return ap.add_argument( action='store_true', *a,**ka)
apbool( '--rm',  help= 'cmd=remove')
ap.add_argument( '--cmd', default= 'ls -ogF',  help= 'команда ако няма --rm')
ap.add_argument( '--filter', default= './radio/*/*.wav', help= 'филтър входящи файлове ако няма зададени')
ap.add_argument( 'files', nargs='*', help= 'входящи файлове')
apbool( '--nothing', '-n',)
optz = ap.parse_args()
cmd = optz.rm and 'rm' or optz.cmd

from pathlib import Path
from sumtim2 import filesize, minsec

for b in [Path(p) for p in optz.files] or Path().glob( optz.filter):
    a = b.with_name( b.name.split('.org.')[0] )
    for sfx in ['','.wav','.out']:
        c = a.with_suffix( sfx+'.flac')
        if c.exists():
            a = c
            break
    else:   #nema
        continue
    atime,afsz = filesize( str(a))
    btime,bfsz = filesize( str(b))
    if abs(atime-btime)<0.4:
        print( '=', minsec( atime), a)
        cmds = cmd.split() + [ str(b) ]
        if optz.nothing: print( '>', cmds)
        else: subprocess.call( cmds)
    else:
        print( '? ', atime, minsec( atime), afsz, a)
        print( ' ?', btime, minsec( btime), bfsz, b)

# vim:ts=4:sw=4:expandtab

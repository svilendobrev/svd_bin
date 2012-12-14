#!/usr/bin/env python
#sdobrev 2007-

from svd_util import optz
optz.help( '''use as filter: enc2enc [options] input_encoding output_encoding <input >output
    use utf2 as special input_encoding to double decode utf8
''' )
optz.bool( 'reverse')
optz, argz = optz.get()

import codecs
import sys
import os

e_from = argz[0]
e_to = argz[1]

utf2 = e_from == 'utf2'
if utf2: e_from = 'utf8'

fi = codecs.getreader( e_from)( sys.stdin, errors='replace')

if utf2:
    from unutf2 import unutf2
    fi = [ unutf2( l, decode= False) for l in fi ]

fo = codecs.getwriter( e_to)( sys.stdout, errors='replace')

for l in fi:
    if optz.reverse:
        a = list(l)
        a.reverse()
        l = ''.join(a)
    fo.write( l)

# vim:ts=4:sw=4:expandtab

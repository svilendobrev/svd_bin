#!/usr/bin/env python
#sdobrev 2007-

from svd_util import optz
optz.help( '''use as filter: enc2enc [options] input_encoding output_encoding <input >output
    use "utf2" as special input_encoding to double decode utf8
    use "octal" as special input_encoding to decode octal sequences
''' )
optz.bool( 'reverse')
#optz.bool( 'unicodeio', help= 'i/o is utf, but encode2input+decode2output')
optz, argz = optz.get()

import codecs
import sys
import os

stdin = sys.stdin
stdout= sys.stdout
_v3 = sys.version_info[0]>=3
if _v3:
    stdin= stdin.buffer
    stdout=stdout.buffer

e_from = argz[0]
e_to = argz[1]

utf2 = e_from == 'utf2'
if utf2: e_from = 'utf8'

octal = e_from == 'octal'
if octal: e_from = 'utf8'

fi = codecs.getreader( e_from)( stdin, errors='replace')

if utf2:
    from unutf2 import unutf2
    fi = [ unutf2( l, decode= False) for l in fi ]
if octal:
    def uoct2u( x):
        return x.encode( 'latin1').decode( 'unicode-escape').encode('latin1').decode('utf8')
    import re
    def decode( t):
        def func( m): return uoct2u( m.group(0))
        return re.sub( r'(\\\d{3})+', func, t)
    fi = [ decode( l) for l in fi ]

fo = codecs.getwriter( e_to)( stdout, errors='replace')

for l in fi:
    if optz.reverse:
        l = ''.join( reversed(l))
    fo.write( l)

# vim:ts=4:sw=4:expandtab

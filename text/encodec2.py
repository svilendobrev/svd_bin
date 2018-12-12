#!/usr/bin/env python
#sdobrev 2007-

from svd_util import optz
optz.help( '''default use is filter: %prog [options] input_encoding output_encoding <input >output
    output_encoding default is utf8 ;
    use "utf2" as special input_encoding to double decode utf8
''' .strip())
optz.bool( 'reverse', help= 'reverses each line' )
optz.text( 'input',   '-i', default= '-', help= 'input  filename, -/empty means stdin, default: stdin')
optz.text( 'output',  '-o', default= '-', help= 'output filename, = means overwrite input, -/empty means stdout, default: stdout')
#optz.bool( 'overwrite')
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
e_to = (argz[1:] or ['utf8'])[0]

utf2 = e_from == 'utf2'
if utf2: e_from = 'utf8'

xi = codecs.getreader( e_from)
xo = codecs.getwriter( e_to)

fin = stdin
if optz.input and optz.input != '-':
    fin = open( optz.input, 'rb')

fout = stdout
fouttmp  = None
if optz.output and optz.output != '-':
    assert optz.output != optz.input
    if optz.output != '=':
        fout = open( optz.output, 'wb')
    else:
        import tempfile
        assert fin is not stdin
        dir,name = os.path.split( optz.input)
        fout = tempfile.NamedTemporaryFile( prefix= name, dir= dir, delete= False)
        fouttmp = fout.name

#try:
with fout:
    with fin:
        fo = xo( fout, errors='replace')
        fi = xi( fin,  errors='replace')
        for l in fi:
            if utf2:
                from unutf2 import unutf2
                l = unutf2( l, decode= False)
            if optz.reverse:
                l = ''.join( reversed(l))
            fo.write( l)
#except:
#    if fouttmp: os.remove( fouttmp)
#    raise
if fouttmp:
    os.remove( optz.input)
    os.rename( fouttmp, optz.input)

# vim:ts=4:sw=4:expandtab

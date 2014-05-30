#!/usr/bin/env python
from __future__ import print_function

import sys
from util import optz
optz.usage( '%prog [opts] wavfile[s]' )
optz.bool( 'verbose', '-v')
optz.text( 'outfile', '-o', help= 'outfile, "-" for stdout')
optz.int(  'maxsize', '-l', help= 'max size in MBs, per item')
options,args = optz.get()

def prn( *a):
    print( *a, file=sys.stderr)

import wave
o = None
oname = options.outfile
if oname == '-': oname = sys.stdout
sz = options.maxsize
totals = 0.0
oparams = None
for a in args:
    i = wave.open( a, 'r')
    params = (nchannels, sampwidth, framerate, nframes, comptype, compname) = i.getparams()
    iparams = params[:3]+params[4:]
    size = nframes/float(framerate)
    totals += size
    prn( '< %s: %.2f s' % (a, size,) , options.verbose and params or '')
    if oparams:
        assert iparams == oparams, (oparams, iparams)
    oparams = iparams
    if not oname: continue
    while 1:
        data = i.readframes(1024*1024)
        if not data: break
        if o is None:
            o = wave.open( oname, 'w')
            o.setparams( params)
            prn( '>>', oname)
        o.writeframes( data)
        if sz is not None:
            sz-=1
            if not sz: break

prn( '>>', totals, 's')
# vim:ts=4:sw=4:expandtab

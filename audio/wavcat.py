#!/usr/bin/env python

import sys
from util import optz
optz.usage( '%prog [opts] wavfile[s]' )
optz.bool( 'verbose', '-v')
optz.text( 'outfile', '-o', help= 'outfile, "-" for stdout')
optz.int(  'maxsize', '-l', help= 'max size in MBs')
options,args = optz.get()

import wave
o = None
oname = options.outfile
if oname == '-': oname = sys.stdout
sz = options.maxsize
totals = 0.0
for a in args:
    i = wave.open( a, 'r')
    params = (nchannels, sampwidth, framerate, nframes, comptype, compname) = i.getparams()
    size = nframes/float(framerate)
    totals += size
    print >>sys.stderr, '< %s: %.2f s' % (a, size,) ,
    print >>sys.stderr, options.verbose and params or ''
    if not oname: continue
    while 1:
        data = i.readframes(1024*1024)
        if not data: break
        if o is None:
            o = wave.open( oname, 'w')
            o.setparams( params)
            print >>sys.stderr, '>>', oname
        o.writeframes( data)
        if sz is not None:
            sz-=1
            if not sz: break

print >>sys.stderr, '>>', totals, 's'
# vim:ts=4:sw=4:expandtab

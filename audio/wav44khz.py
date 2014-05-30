#!/usr/bin/env python
# -*- coding: utf-8 -*-
FRATE = 44100
import wave, os, sys
for fn in sys.argv[1:]:
    i = wave.open( fn)
    p = i.getparams()
    if p[2] == FRATE: continue
    #f,ext = os.path.splitext( fn)
    o = wave.open( fn + '.' + str(FRATE) + '.wav', 'w')
    q = list( p)
    q[2] = FRATE
    o.setparams( q)
    while 1:
        data = i.readframes( 8*1024*1024)
        if not data: break
        o.writeframes( data)
    o.close()

# vim:ts=4:sw=4:expandtab

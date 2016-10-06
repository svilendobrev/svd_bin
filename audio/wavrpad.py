#!/usr/bin/env python
# -*- coding: utf-8 -*-
#reverse of wavrtrim.py
from __future__ import print_function #,unicode_literals
import wave, sys
fname = sys.argv[1]
zerosec = float(sys.argv[2])

i = wave.open( fname )
params = (nchannels, sampwidth, framerate, nframes, comptype, compname) = i.getparams()
zeroframes = int( zerosec * framerate )

n = i.getnframes()
w = i.readframes(n)
lf = len(w) // n
print( fname, zerosec, zeroframes)
w = w + bytes( lf * zeroframes)
o = wave.open( fname+'.zeropad.wav', 'w')
o.setparams( params)
o.writeframes( w)
# vim:ts=4:sw=4:expandtab

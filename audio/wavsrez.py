#!/usr/bin/env python
#use: srez  a.wav 4.2 141.3
#use: srez  a.wav 4.2 -5
#use: srez  a.wav 4.2 0
#use: srez  a.wav 0 -44
#use: srez  a.wav 25 +70  ->  25..95

import sys
class DictAttr( dict):
    def __init__( me, *a, **k):
        dict.__init__( me, *a, **k)
        me.__dict__ = me
#verbose = 1
infile, ss, se = sys.argv[1:4]
import wave
i = wave.open( infile, 'r')
p = DictAttr()
params = (p.nchannels, p.sampwidth, p.framerate, p.nframes, p.comptype, p.compname) = i.getparams()
#size = p.nframes/float(p.framerate)
#print nframes, framerate
#if verbose: print( '%sHz %s x %sbit' % (p.framerate, p.nchannels, p.sampwidth*8))
def sec2frames(sec):
    if ':' in sec:
        min,sec = sec.split(':')
        sec = float(sec) + 60*float(min)
    return int( float(sec) * p.framerate)

fs,fe = [sec2frames(x) for x in (ss,se) ]
if se[0]=='+': fe += fs
cur = 0
ooname = 'cut.'+infile
i.readframes( fs - cur) #skip
data = i.readframes( (fe if fe>0 else p.nframes + fe) - fs )
assert data
o = wave.open( ooname, 'w')
o.setparams( params)
o.writeframes( data)
o.close()
# vim:ts=4:sw=4:expandtab

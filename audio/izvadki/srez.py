#!/usr/bin/env python
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
    return int(sec * p.framerate)

fs,fe = [sec2frames( float(x) ) for x in (ss,se) ]
cur = 0
ooname = 'cut.'+infile
i.readframes( fs - cur) #skip
data = i.readframes( fe - fs )
assert data
o = wave.open( ooname, 'w')
o.setparams( params)
o.writeframes( data)
o.close()
# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python

from svd_util import optz
optz.int( 'n', default=5, help= 'lenght in seconds to match, 0=whole')
optz, argz = optz.parse()
import wave
import audioop

class wav:
    def __init__( me, fname, duration =None):
        w = me.wav = wave.open( fname)
        n = duration and duration * w.getframerate() or 0
        me.mono = me.data = me.wav.readframes( n or w.getnframes() )
        if w.getnchannels() == 2:
            me.mono = audioop.tomono( me.data, 2, 0.5, 0.5)
        me.params = w.getsampwidth(), w.getframerate()

print( optz.n)
find  = wav( argz[0], optz.n )
where = wav( argz[1])

assert where.params == find.params, (where.params, find.params)

ofs,coef = audioop.findfit( where.mono, find.mono)
print( ofs/where.wav.getframerate(), coef)

# vim:ts=4:sw=4:expandtab

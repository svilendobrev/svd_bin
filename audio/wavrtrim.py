#!/usr/bin/env python
# -*- coding: utf-8 -*-
#reverse of wavrpad.py
from __future__ import print_function #,unicode_literals
import wave, sys
for fname in sys.argv[1:]:
    i = wave.open( fname )
    n = i.getnframes()
    w = i.readframes(n)
    lf = len(w) // n
    print( fname, len(w), n )
    zeros = bytes( lf* 2**16)
    lz = len(zeros)
    while lz >= lf:
        while w[-lz:] == zeros[:lz]:
            #print( len(w), w[-10:] )
            w = w[:-lz]
        lz //= 2
    print( len(w), w[-10:] )

    o = wave.open( fname+'.rtrim.wav', 'w' )
    o.setparams( i.getparams() )
    #o.setnframes( len(w) // n )
    o.writeframes( w)

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys

dx = {}
for cue in sys.argv[1:]:    #seno
    track = None
    try:
     for l in open(cue):
        l = l.split()
        if not l: continue
        l0 = l[0].lower()
        if l0 == 'track':
            track = int(l[1])
            continue
        if track and l0 == 'title':
            ll = ' '.join( l[1:]).lower()
            dx.setdefault( ll, []).append( (cue, track) )
    except:
        print( '?', cue)
        raise

track = wfile = None
tracks = {}
for l in sys.stdin:     #igli
    l = l.split()
    if not l: continue
    l0 = l[0].lower()
#    print(44444, l)
    if l0 == 'file':
        ll = ' '.join( l[1:-1]).lower()
        wfile = ll
        track = None
        tracks.clear()
        continue
    if l0 == 'track':
        track = int(l[1])
        continue
    if track and l0 == 'title':
        if track in tracks: continue
        tracks[ track] = l
        try: l.remove('[live]')
        except: pass
        ll = ' '.join( l[1:]).lower()
        if ll in dx: print( '+', ll, '==', dx[ll])
        else: print( '?', ll, wfile, track)

# vim:ts=4:sw=4:expandtab

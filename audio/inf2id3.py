#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys
import glob, os
import mstagger
def opt( *xx):
    for x in xx:
        if x in sys.argv: return sys.argv.remove( x ) or True
    return None
rename = opt( '--ren', '--rename')
enc = opt( '--latin1', '--latin') and 'latin1' or opt( '--cp1251', '--win1251', '--1251') and 'cp1251' or None
if enc: mstagger.encv1 = enc
enc = enc or 'utf8'

for inf in sys.argv[1:]:
    tags = dict( x.split('=',1) for x in open( inf, 'rb').read().decode( enc).splitlines() if '=' in x )
    #tags = dict( (k.lower(),v) for k,v in tags.items())
    t2t = dict(
        albumperformer=	'artist',
        performer=	'artist',
        albumtitle=	'album',
        tracktitle=	'title',
        tracknumber='track',
    )
    #print( tags)
    tid3 = {}
    for k,v in tags.items():
        v = v.strip().strip('"\'')
        t = t2t.get( k.lower())
        if not t or not v: continue
        if t=='track': v = int(v)
        tid3[t] = v

    mp3 = glob.glob( os.path.splitext( inf)[0] +'*.mp3' )
    if not mp3:
        print( inf, '! no mp3')
        continue
    mp3 = mp3[0]
    print( inf, mp3, tid3)
    if tid3:
        mstagger.write( mp3, tid3)

    if tid3 and rename:
        fname = ''
        for k in 'track artist album title'.split():
            v = tid3.get(k)
            if not v: continue
            sep='--'
            if k=='track':
                sep='-'
                v = str(v).zfill(2)
            if fname: fname += sep
            fname += v
        fname += '.mp3'
        fname = fname.replace('/','-')
        print( inf, mp3, '>', fname)
        p = os.path.dirname( mp3)
        os.rename( mp3, os.path.join( p,fname))

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import json, sys, shutil, os

# https://together.jolla.com/question/169680/how-to-add-sounds-to-the-default-list-of-ringtones/
# but does not work XXX
# variants tried:
# * plainnames inside stereo/ + stereo.index
# * translationCatalog-prefixed  -ringtone suffiexd names inside stereo/stereo.index
# * separate sounds/ + sounds.index next to stereo/
# so.... just replace the available aloe.*-ringtone.ogg with whatever sound file u want (can be mp3,wav,.. noone cares about .ogg extension )

pathsys = '/usr/share/sounds/jolla-ringtones/stereo'
idx = [ f for f in sys.argv[1:] if f.endswith( '.index') ]
infiles = [ f for f in sys.argv[1:] if f not in idx ]
path = idx and idx[0].replace( '.index','') or pathsys
index = path+'.index'
try:
    with open( index) as fi:
        x = json.load( fi)
except FileNotFoundError:
    x = dict( translationCatalog= 'sounds', files= [] )

xfiles = x['files']
byfname = dict( (f['fileName'], f) for f in xfiles )
#maybe also .aliases if any
'''
{
    "translationCatalog" : "jolla-ringtones",
    "files" : [
        {
            "displayName"   : "jolla-ringtones-ringtone",
            "fileName"      : "jolla-ringtone.ogg",
            "category"      : "Ringtone",
            "aliases"       : [ "jolla-ringtone.wav" ]
        }, {
        ...
'''
# $translationCatalog-$imeto-ringtone

newfiles = []
for f in infiles:
    if f in byfname: continue
    name = 'zz'+f.rsplit( '/',1)[-1].rsplit( '.', 1)[0]
    newfiles.append( dict(
            displayName = x['translationCatalog']+'-'+ name.replace('-','_') + '-ringtone',
            fileName    = f,
            category    = "Ringtone",
            ))
    if os.getenv('COPY'):
        print( 'cp', f, path)
        shutil.copy( f, path)

if newfiles:
    xfiles.extend( newfiles)
    print( 'overwrite', index)
    print( 'may need:   systemctl --user restart lipstick.service')
    os.rename
    with open( index, 'w') as fo:
        json.dump( x, fo, indent=4)

# vim:ts=4:sw=4:expandtab

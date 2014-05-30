#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aeidon
import sys
import os.path as op

from svd_util import optz
from svd_util.osextra import execresult

optz.optany( 'framerate', type= float, default=25)
optz,args = optz.get()

class FRAMERATE:
    value= optz.framerate
UNDO_LIMIT =None
doc = aeidon.documents.MAIN

import re
durmkv = re.compile( 'Duration: (\d+)')

p = aeidon.Project( FRAMERATE, UNDO_LIMIT)
project = None
size = 0
for path in args:
    encoding = aeidon.encodings.detect( path)
    sz = execresult( ['mkvinfo', op.splitext( path)[0] + '.mkv'])
    m = durmkv.search( sz)
    assert m
    sz = int( m.group(1))
    if not project:
        project = aeidon.Project( FRAMERATE, UNDO_LIMIT)
        project.open( doc, path, encoding )
    else:
        #offset = project.subtitles[-1].end
        offset = size
        p.open( doc, path, encoding )
        p.shift_positions( None, offset)
        tp = project
        tn = len(tp.subtitles)
        print 'add to ', offset, tn
        indices = range(tn, tn + len( p.subtitles))
        project.insert_subtitles( indices, p.subtitles)
    size += sz

print 'all', len( project.subtitles)
project.save( doc, sys.stdout)


# vim:ts=4:sw=4:expandtab

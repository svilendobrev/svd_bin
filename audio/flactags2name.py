#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

metaflac = 'metaflac --export-tags-to=-'.split()
soxi     = 'soxi -V0'.split()

import sys, subprocess, os
tags = [ t.lower() for t in sys.argv[1:]]
for fname in sys.stdin:
    fname = fname.rstrip()
    info = subprocess.check_output( metaflac + [ fname ] ).decode( sys.stdout.encoding)
    #print( info)
    info = dict( [x.strip() for x in a.split('=',1)]
                    for a in info.strip().split('\n')
                    if '=' in a
                    )
    info = dict( (k.lower(),v) for k,v in info.items())
    newname = ': '.join( info.get( t,'?') for t in tags )
    newname = newname.replace( '/', '-')
    #print( newname)
    os.rename( fname, os.path.join( os.path.dirname( fname), newname + os.path.splitext( fname)[1] ))

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
'apply timestamps from orig.files into tree of renamed files'
import sys
import datetime

fdati, dir = sys.argv[1:3]

#find . -name \*jpg -printf '%T+ %p\n'
#2014-02-02+02:47:02.0000000000 /path/to/img12345.jpg
dati1 = [ a.split() for a in open( fdati )]
dati  = dict( (int(f.split('/')[-1].lower().strip('miovk_.')), d) for d,f in dati1 )
print( 'dati', len(dati))
assert len(dati) == len(dati1), ( len(dati), len(dati1))

import os, stat

for root, dirs, files in os.walk( dir ):
    for fn in sorted(files):
        if not fn.lower().endswith('.mkv'): continue
        f = fn.lower()
        f = f.split('.')[0]
        f = f.split('-')[0]
        f = f.split('v6c')[-1]
        f = f.strip('miovk_')
        print( f, fn)
        f = int(f)
        fp = os.path.join( root, fn)
        if f in dati:
            s = os.stat( fp) #.st_ctime  stat.ST_CTIME
            dt = datetime.datetime.strptime( dati[f].split('.')[0], '%Y-%m-%d+%H:%M:%S')
            ts = dt.timestamp()
            print( fp, dt) #, s.st_ctime))
            os.utime( fp, (s.st_atime, ts) )

# vim:ts=4:sw=4:expandtab

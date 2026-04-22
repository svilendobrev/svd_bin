#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys, datetime

use_ver = None
try: use_ver = not sys.argv.remove('--ver')
except ValueError: pass
#else: use date

ver2date = {}
date2ver = {}
ver = None
for a in sys.stdin:     # | hg log
    if not a.strip():
        ver = None
        continue
    k,v = [ x.strip() for x in a.split(':',1)]
    if k== 'changeset': ver = int(v.split(':')[0])
    elif k=='date':
        dt = datetime.datetime.strptime( v, '%c %z' )#'%a %b %d %H:%M:%S %Y')
        ver2date[ ver] = dt.date().isoformat()
        date2ver[ dt.date().isoformat() ] = ver

dates_sorted = sorted( date2ver)
import bisect
def find_le( a, x):
    'Find rightmost value less than or equal to x'
    i = bisect.bisect_right( a, x)
    if i:
        return a[i-1]
    raise ValueError
def date2ver_then( d):
    if d in date2ver: return date2ver[d]
    d2 = find_le( dates_sorted, d)
    return date2ver[ d2]

all_exts = set()
by_ver = {}
for a in sys.argv[1:]:
    when,ext = a.split('.')
    tot = [ x.split()[0] for x in open( a) if 'общо' in x ][0]
    v = by_ver.setdefault( int(when) if use_ver else when, {})
    ext = ext.split('lc')[0]
    v[ ext] = tot
    all_exts.add( ext)

import csv
d = csv.DictWriter( sys.stdout, 'ver date'.split() + sorted( all_exts) )
d.writeheader()
for k,v in sorted( by_ver.items()):
    #print( k, ':', *[ e[:2] + '=' + str(ev) for e,ev in sorted( v.items())])
    when = dict( ver=k, date= ver2date[ k]) if use_ver else dict( ver= date2ver_then( k), date=k)
    d.writerow( dict( **when, **v))

# vim:ts=4:sw=4:expandtab

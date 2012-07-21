#!/bin/env python
FS=75
import sys
args=[]
for a in sys.argv[1:]:
    if a.startswith('-fs='):
        FS= int(a[4:])
    else: args.append( a)
f0 = 0
for a in args or sys.stdin:
    f = int(a)
    f -= f0
    s = int(f/FS)
    ff = f-s*FS
    m = int(s/60)
    ss = s-60*m
    if not f0: f0 = f
    print '%d:%02d.%02d' % (m,ss,ff)

#from util import minsec
#for x in minsec.frame2minsec( args or sys.stdin, FS=FS): print x

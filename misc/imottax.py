#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys
i = float(sys.argv[1])
notarialni = [
    [0,     30,0  ],
    [100 ,   0,1.5],
    [1000 ,  0,1.3],
    [10000,  0,0.8],
    [50000 , 0,0.5],
    [100000, 0,0.2],
    [500000, 0,0.1],
  ]

notar = 0
ii = i
for n,fix,perc in reversed(notarialni):
    if ii>n:
        notar += fix + perc/100*(ii-n)
        ii=n

r = dict(
    danyk = 2.6/100 * i,    #2--3% според общината
    vpis  = max( 0.01/100*i, 10),
    notar = notar,
    ddsnotar = notar*0.2,
    )
for k,v in r.items(): r[k] = round(v,2)
s = sum(r.values())
print( 'данък={danyk} вписване={vpis} нотар={notar} ддс-н={ddsnotar} ; общо {s} '.format( s=s,** r))

# vim:ts=4:sw=4:expandtab

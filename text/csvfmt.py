#!/usr/bin/env python
# -*- coding: utf-8 -*-
#$Id$

ENC = 'utf-8'
obedini_pfx = 'rem'

import sys,csv
poleta = None
k2vse = {}
vse=[]
for r in csv.reader( open(sys.argv[1], encoding= ENC), delimiter= (sys.argv[2:]+['|'])[0]):
    r = [ a.replace( '\t',' ') for a in r]  #.decode( ENC)
    if poleta is None:
        poleta = r
        continue
    for k,v in zip( poleta, r):
        k2vse.setdefault( k, []).append( v )
        #print( k,v)

obedineni = [ p for p in poleta if p.startswith( obedini_pfx) ]
for p in obedineni: poleta.remove( p)
poleta.append( obedini_pfx)

ob_vse = [ k2vse.pop( p) for p in obedineni]
ob1 = [ ' '.join( v) for v in zip( *ob_vse)]
k2vse[ obedini_pfx] = ob1

razmeri = [ max( (len(x) for x in k2vse[k]), default= 0) for k in poleta ]

print( poleta)
print( len(razmeri), sum(razmeri), razmeri)

razd = '|'

def izhod( red, razmeri, center=False):
    r = ''
    start=1
    for v,l in zip( red, razmeri):
        if center: f = v.center
        else:
            f = v.replace('.','').isdigit() and v.rjust or v.ljust
        if not start: r+= razd+' '
        start=0
        r+= f(l)    #.encode( ENC)
    print( r)

izhod( poleta, razmeri, center=True)

for red in zip( *(k2vse[k] for k in poleta)):
    izhod( red, razmeri)

# vim:ts=4:sw=4:expandtab

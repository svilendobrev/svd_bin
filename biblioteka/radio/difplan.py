#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, datetime
for a in sys.argv[1:]:
    print( a)

    n = [ i.strip() for i in open(a).readlines() ]
    o = [ i.strip() for i in open( '/osha/radio/'+a).readlines() ]
    n0 = n[0].replace( '1 дни', '2 дни')
    o0 = o[0]
    if n0 != o[0]:
        print( '''
?%(a)s
< %(n0)s
> %(o0)s
''' % locals() )

    def read( ii):
        c = flt = []
        all = []
        for i in ii[2:]:
            i = i.strip(' #,').strip()
            if not i: continue
            if i == ']' or i.startswith('всички'):
                c = all
                continue
            d = eval(i)
            for k in 'channel stream ime tmdt'.split():
                d.pop(k,None)
            e = 'endtime'
            if d[e]==(18,35): d[e]=(18,30)
            c.append( d)
        return flt,all

    nf,na = read( n)
    of,oa = read( o)

#                if 'text' not in od:

    def dif( a, nl,ol):
        for ni,oi in zip( nl,ol):
            if oi == ni: continue
            print( '''
?%(a)s
<< %(ni)s
>> %(oi)s
''' % locals() )

        if len(ol)>len(nl):
            for oi in of[len(nl):]:
                if oi.get( 'today') > nl[0].get('today'): continue
                if not oi.get( 'text'): continue
                print( a, 'miss', ol[ len(nl): ] )

    dif( a,nf,of)
    dif( a,na,oa)

# vim:ts=4:sw=4:expandtab

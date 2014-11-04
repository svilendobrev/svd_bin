#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from svd_util import optz
from svd_util.struct import DictAttr
optz.int( 'year', default= 2012)
optz.bool( '2011', )

y2011 = DictAttr(
 superannuation = 0.09,
 bands = [
    [  6000 , .15 ],
    [ 37000 , .30 ],
    [ 80000 , .37 ],
    [180000 , .45 ],
    ],
 levy = dict(
    medical = 0.015,
    #medical_no_private = 0.01 # additional 1% if no-private-health care
    flood = [
        [  50000,  .005 ],
        [ 100000,  .01  ],
        ]
    )
)

all = {
    2011: y2011,
    2012: DictAttr(     #2012-2013
      y2011,
      bands = [
        [ 18200 , .19 ],
        [ 37000 , .325],
        [ 80000 , .37 ],
        [180000 , .45 ],
        ],
      levy = dict( y2011['levy'],
            flood=0 )
    ),
}

optz,args = optz.get()
x = float( args[0])
year = getattr( optz, '2011', None) and 2011 or optz.year

shema = all[ year]
sup = x / (1+shema.superannuation) * shema.superannuation
x -= sup
print( "superann {shema.superannuation} /{sup} = {x}".format( **locals() ))

def banded( bands, x):
    tax = 0
    for lin in reversed( bands):
        l,coef = lin
        if x <= l: continue
        tax += ( x-l ) * coef
        #print ' ', l,coef,tax
        x = l
    return tax

tax = banded( shema.bands, x)

levy = 0
for typ,l in shema.levy.items():
    if not l: continue
    if isinstance( l, (tuple,list)):
        lv = banded( l, x)
    else:
        lv = l * x
    print( ' levy', typ, l, lv)
    levy+= lv
tax += levy

x -= tax
x12 = x/12.0
x52 = x/52.0
print( "tax: {tax:.2f}; clear: {x:.2f}; /12: {x12:.2f}; /52: {x52:.2f}".format( **locals()))

# vim:ts=4:sw=4:expandtab

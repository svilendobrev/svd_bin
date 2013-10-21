#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

#from svd_util.divan import cubase, views
from svd_util import optz

from abbr import Abbr, razdeli_kamila, razdeli_kamila2
sykrashtenia = Abbr()
def vnesi_sykr( sykr_fn):
    sykrashtenia.cheti_eutf( sykr_fn)
    sykrashtenia.popylni_avto()

def iznesi_sykr():
    for k,vv in sorted( sykrashtenia.imena.items()):

        print( k,vv)

gg={}
optz.str(  'vnesi_sykr',  help= 'чети файл със съкращения (списъци имена или от грамофонче)', **gg)
optz.bool( 'iznesi_sykr', help= 'сложи имената и съкращенията на Дивана', **gg)
optz.list( 'sykrati',     help= 'съкрати това име (може няколко пъти)', **gg)

if __name__ == '__main__':
    optz,argz = optz.get()
    #optz.vnesi_sykr = '/zapisi/abbr' #argz[0]
    #optz.iznesi_sykr = True
    if optz.vnesi_sykr:
        vnesi_sykr( optz.vnesi_sykr)
    if optz.iznesi_sykr:
        iznesi_sykr()
    for i in (optz.sykrati or ()):
        #i = optz.sykrati
        sykrashtenia.eto_imepylno( i)
        print( i, ':', sykrashtenia.dai_kyso( i, vse=True) )

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
употреба: p2opis --papka коренна/  *opisi*

чете опис, съдържащ ред:
#http://78.83.22.128/_nradio/2014/-видове/деца-рт/bezpodobni/hb-0419-0715+Рт_за_деца+Грозният_принц_Куша--индийска/

- взема ПЪТ и ИМЕ (от след _nradio/)
- извлича ЧАСТ# от описа

преименува описа в ИМЕ-ЧАСТ.opis на място,
и го слага също и в (papka+)ПЪТ (създавайки лисващите нива)
'''

import os, subprocess
from svd_util import optz
from svd_util import lat2cyr
from svd_util import osextra
optz.bool( 'nedei', '-n')
optz.text( 'papka', '-p', help= 'начална коренна папка')
optz.text( 'cmd', help= 'изпълни вместо преименоване тази команда с 2 аргумента')
optz.help( __doc__)
#rec2dir
def c2l( x): return lat2cyr.zvuchene.cyr2lat( x).lower()
join = os.path.join

optz,argz = optz.get()
for a in argz:
    o = open(a).readlines()
    http = [ l.strip('#') for l in o if 'http://' in l and '/_nradio' in l]
    if not http:
        print( '??? http-къде', a)
        continue
    chast= [ l.split(':',1)[-1] for l in o if l.startswith( '#част:') ]
    chast = chast and chast[0].strip() or ''

    pyt = http[0].strip().split('/_nradio/')[-1]
    papka = pyt.strip('/').split('/')[-1]
    ime = papka.split('+')
    if ime[0].startswith('hb'):
        ime = ime[-1]
    else:
        assert ime[-1].startswith('hb'), papka
        ime = ime[-2]
    ime_lat = c2l( ime)
    if chast: ime_lat += '-'+chast
    fime = ime_lat+'.opis'
    print( a, ':', fime, '->', pyt)
    if optz.nedei: continue

    if optz.papka:
        pyt = join( optz.papka, pyt)
    osextra.makedirs( pyt, exist_ok= True)
    pyt_ime = join( pyt, fime)
    try:
        os.link( a, pyt_ime )
    except FileExistsError:
        print( '?? FileExistsError', pyt_ime)
    if optz.cmd:
        subprocess.call( optz.cmd.split() + [ a, fime])
    else:
        os.rename( a, fime)

# vim:ts=4:sw=4:expandtab

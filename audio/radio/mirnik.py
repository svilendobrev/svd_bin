#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Иван Кулеков. Немският посланик.mp3.mp3
import sys, re
import os
from os.path import join, isdir, splitext, basename, exists
from util import lat2cyr
def c2l( x): return lat2cyr.zvuchene.cyr2lat( x).lower()

for a in sys.argv[1:]:
    b = basename( a)
    print( b)
    oavtor,oime,ext = re.split('[-.]', b,2)
    avtor = c2l(oavtor).split()
    ime   = c2l( oime).split()

    adir = '--'.join( ['.'.join(ime), '.'.join(avtor), 'radio'])
    adir_da = join( adir, '0', 'da.mir-nik')
    print( adir_da, a)
    try: os.makedirs( adir_da)
    except: pass
    try:
        os.link( a, join( adir_da, b) )
        os.rename( a, join( adir, adir+'.mp3' ) )
    except Exception as e:
        print( e)
    #ime = ' '.join(ime)
    #avtor = ''.join( avtor)
    oavtor = oavtor.replace(' ','')
    opis = '''
име: %(oime)s
автор: %(oavtor)s
ет: възр
изд: радио
уч:
 пр:
 др:
 ред:
 изп:
 з.реж:
 з.оп:
 з.оф:
 м.оф:
 реж:
'''
    fop = join( adir, 'opis')
    if not exists( fop):
        open( fop, 'w').write( opis % locals() )


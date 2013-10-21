#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import prikazki
import opisvane
from svd_util import eutf, optz, lat2cyr
from glob import glob
import datetime #import datetime, timedelta
from svd_util.struct import DictAttr, attr2item

info = prikazki.info

gg = {}
optz.bool( 'simvolni', '-L',    help= 'обхожда и символни връзки', **gg)
optz.bool( 'davai',         help= 'извършва промените', **gg)
optz.bool( 'prezapis',      help= 'презаписва всички файлове (иначе само ако са различни)')

optz.text( 'html_enc',      help= 'кодировка на html [%default]', default='utf8', **gg)  #cp1251
optz.text( 'html_spisyk',   help= 'прави общ списък html-страница', **gg)
optz.text( 'html_novi',     help= 'прави списък новости отделен (иначе част от общия списък)', **gg)
optz.text( 'html_izbrani',  help= 'прави списък на само хубавите - извадка от общия списък', **gg)
optz.bool( 'obshto_otgore',         help= 'слага Общо: отгоре (иначе отдолу)', **gg)
optz.bool( 'obshto_broi_zapisi',    help= 'брои файловете със записи, а не папките', **gg)
optz.text( 'podredba',              help= 'подрежда по изброените полета [%default]',
            default= 'humor,ime_sglobeno,pored',
                **gg)
optz.bool( 'otkoga_e_mintime',      help= 'слага липсващо откога=най-ранното време на папката', **gg)
optz.int(  'kolko_dni_e_novo',   default=35, help= 'толкова дни нещо се счита за ново [%default]', **gg)
optz.int(  'kolko_sa_novi',      default=0,  help= 'толкова последни неща се считат за нови [%default]', **gg)

options,args = optz.get()
prikazki.info.options = options

#for path,dirs,files in info.obikoli( args, info.e_za_propuskane ):
data = []
for a in args:
    for f in glob( a+'/*/apapka.tmp'):
        data4papka = DictAttr( eval( open(f).read(), dict( datetime= datetime)))
        data.append( (f, data4papka) )

total = DictAttr(
    time= 0,
    size= 0,
    n= 0,
    n_zapisi = 0,
    )
novi = []
spisyk = []
izbor = []

for f,d in data:
    for k in total:
        total[ k] += d.total[ k]

    novi += [ DictAttr( red= red, _otkoga= otkoga, key= key) for red, otkoga, key in d.html4novi ]

    spisyk.append( (d.spisyk, d.podredba) )
    if d.izbor:
        izbor.append( (d.spisyk, d.podredba) )


spisyk.sort( key= lambda x: x[-1])
izbor.sort(  key= lambda x: x[-1])
#for s,k in spisyk: print( k )

prikazki.html_spisyk( options,
    spisyk = [s for s,k in spisyk],
    izbor  = [s for s,k in izbor],
    novi = sorted( novi, key= lambda i: i.key),
    total = total,
    gotovi = True,
    html4novi= lambda ii: ((x.red,x._otkoga,x.key) for x in ii)
)

# vim:ts=4:sw=4:expandtab

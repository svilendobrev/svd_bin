#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, io, re
import rec2dir
from svd_util.yamls import usability
from svd_util.struct import DictAttr
from svd_util import optz

'''
име:           Как щастието се скри в четирилистна детелина
автор:         ИринаКарадимчева
откъде:        ВзаП 20140801
издание:       радио
ориг_описание: >-
  „Как щастието се скри в четирилистна детелина“ от Ирина Карадимчева
ориг_рубрика:  Време за приказка

===>
hb-0801-1820+ВзаП+Как_щастието_се_скри_в_четирилистна_детелина--Ирина_Карадимч
'''

optz.bool( 'move',    help= 'преименувай към новото име')
optz.bool( 'link',    help= 'направи символна връзка = новото име')
optz.str(  'target',  help= 'къде да сложи горните')
optz.bool( 'avtori_otdelni',   help= 'ползва #автори_отделни: вместо автор:')
_podredbi = 'ime+rubr+vreme rubr+ime+vreme vreme+rubr+ime'.split()
_podredba = _podredbi[0]
optz.str( 'podredba',
    type= 'choice', choices= _podredbi, default= _podredba,
    help= 'подредба в името, подразбиране: %default, другите са: '+' '.join(p for p in _podredbi if p!=_podredba) )
#optz.str(  'prefix',  help= 'слага пред новото име')

optz,argz = optz.get()
for dir in argz:
    fn = dir + '/opis'
    print( '... ', dir)
    try:
        f = open(fn).readlines()
    except Exception as e:
        print( fn, e)
        continue
    f = [
            'автори_отделни: "'+ l.split(':',1)[-1].strip()+'"'
            if l.startswith( '#автори_отделни:')
            else l.rstrip()
            for l in f
        ]
    f = io.StringIO( '\n'.join( f))
        #f.replace( '\n#автори_отделни:', '\nавтори_отделни:' ))

    opis = dict( usability.load( f ) )
    ime = opis.get( 'име')
    ime = ime and str(ime)
    if not ime or not ime.strip('?'):
        ime = ''#l2c( os.path.basename( fn))
    avtor = opis.get( 'автор')
    avtor_dylyg = opis.get( 'автори_отделни')
    if avtor_dylyg and optz.avtori_otdelni: avtor = avtor_dylyg

    def sykr_rubr(x):
        return (x
                ).replace('Салон_за_класифицирана_словесност', 'Салон_словесност'
                ).replace('Салон_за_класифицирана', 'Салон_словесност'
                ).replace('Голямата_къща_на_смешните_хора', 'ГКСХ'
                ).replace('Златните_гласове_на_радиото', 'Златните_гласове'
                ).replace('Запазена_марка', ''
                ).replace('Запазна_марка',  ''
                ).replace('Детски_радиотеатър', 'Рт_за_деца'
                ).replace('Радиотеатър',    'Рт'
                ).replace('Радотеатър',     'Рт'
                ).lstrip('_')
    otkyde = str(opis.get( 'откъде', '') or '').split()
    rubrika_kysa = otkyde[0]
    if rubrika_kysa.isdigit(): rubrika_kysa = ''
    else:
        rubrika_kysa = sykr_rubr(rubrika_kysa)

    rubrika_orig = opis.get( 'ориг_рубрика')
    ime = (ime
            ).replace('документалния', 'док.'
            ).replace('документалната', 'док.'
            ).replace('документално', 'док.'
            ).replace('документална', 'док.'
            ).replace('документален', 'док.'
            )

    if 'еко-ехо' in rubrika_kysa.lower(): ime = avtor = ''
    if len(ime)>30 and opis.get( 'ориг_описание', '').startswith( ime): ime = '' #HACK

    ime = rec2dir.filt_er( ime)
    ime = sykr_rubr( ime)
    if ime in (rubrika_kysa, rubrika_orig): ime = ''
    if ime.startswith( rubrika_kysa+'_:'):
        ime = ime[ len( rubrika_kysa+'_:'):]
    ime = ime.strip('_')

    ldirname = rec2dir.filt_er( '--'.join( a for a in [ ime, avtor, ] if a ))
    fname_kanal_vreme = dir.strip('/').split('/')[-1]

    dt = otkyde[-1]
    if dt.isdigit():
        y,m,d = dt[:4],dt[4:6],dt[6:]
    else: y = m = d = ''
    dotkyde = dict( kan='', god=y, dat=m+d, tim='')

    re_kanalvreme = re.compile( '\+?(?P<kan>\w\w)(?P<god>\d{4})?-(?P<dat>\d{4})-(?P<tim>\d{4})' )
    match = re_kanalvreme.search( fname_kanal_vreme)
    dvreme = DictAttr( (k, v or (match.group(k) if match else '')) for k,v in dotkyde.items() )
    kanal_vreme = '-'.join( x for x in [ dvreme.kan + dvreme.god, dvreme.dat, dvreme.tim ] if x)

    popodredba = dict( ime= ldirname[:70], rubr= rubrika_kysa, vreme =kanal_vreme)
    ldirname = '+'.join( popodredba[i] for i in optz.podredba.split('+') if popodredba[i] )
    if 0:
        ldirname = '+'.join( n for n in [
                    fname_kanal_vreme,
                    rubrika_kysa,
                    ldirname[:60] ]
                    if n )

    #if optz.prefix: ldirname = optz.prefix + ldirname

    cmd = print
    if optz.move: cmd = os.rename
    if optz.link: cmd = os.symlink
    if optz.target: ldirname = os.path.join( optz.target, ldirname)
    try:
        cmd( dir, ldirname)
    except FileExistsError as e:
        print( e)

# vim:ts=4:sw=4:expandtab

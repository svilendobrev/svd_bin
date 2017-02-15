#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, io, re
import rec2dir
from svd_util.yamls import usability
from svd_util.struct import DictAttr
from svd_util import optz

'''
име:        името му
автор:      AвтOра
откъде:     оттам 20140801

===>
времето+оттам+името_му--Aвт_Oра
'''

optz.bool( 'quiet', '-q',  help= 'без излишни съобщения')
optz.bool( 'move',    help= 'преименувай към новото име')
optz.bool( 'link',    help= 'направи символна връзка = новото име')
optz.str(  'target',  help= 'къде да сложи горните')
optz.bool( 'avtori_otdelni',   help= 'ползва #автори_отделни: вместо автор:')
optz.bool( 'ime_sled_avtor',   help= 'автор+име; по подразбиране е име+автор')
optz.str( 'sykr',   help= 'ползва съкращения от този файл')
optz.str( 'razdeli_ime_avtor',  default='--',  help= 'разделител между име и автор ("spc" се замества с интервал " ")')
optz.str( 'razdeli_drugi',      default='+',   help= 'разделител между другите ("spc" се замества с интервал " ")')
_podredbi = 'ime=ime+rubr+vreme rubr=rubr+ime+vreme vreme=vreme+rubr+ime'.split()
_podredba = _podredbi[0].split('=')[0]
optz.str( 'podredba',
    type= 'choice', choices= [s.split('=')[0] for s in _podredbi],
    default= _podredba,
    help= 'подредба в името, подразбиране: %default; варианти: '+' '.join( _podredbi))
#optz.str(  'prefix',  help= 'слага пред новото име')

def spc(x): return x.replace( 'spc', ' ')

optz,argz = optz.get()

sykrashtenia = None
if optz.sykr:
    from abbr import Abbr#, razdeli_kamila, razdeli_kamila2
    sykrashtenia = Abbr()
    sykrashtenia.cheti_eutf( optz.sykr)
    sykrashtenia.popylni_avto()

for dir in argz:
    fn = dir + '/opis'
    if not optz.quiet: print( '... ', dir)
    try:
        f = open(fn).readlines()
    except Exception as e:
        if optz.quiet: print( '... ', dir)
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
    #if ime: ime = ime[0].upper()+ime[1:]
    avtor = opis.get( 'автор')
    avtor_dylyg = opis.get( 'автори_отделни')
    if avtor_dylyg and optz.avtori_otdelni: avtor = avtor_dylyg
    if avtor:
        avtor = avtor.replace('аЛегенда', 'аПриказка' )
        #if sykrashtenia: avtor = sykrashtenia.dai_kyso( avtor, vse=True) or avtor
        if sykrashtenia:
            sykrashtenia.eto_imepylno( avtor)
            avtor = sykrashtenia.dai_imepylno( avtor) or avtor
            #avtor = sykrashtenia.dai_imekyso( avtor, vse=True) # or avtor
        avtor = avtor.replace('аПриказка', 'а')
    def sykr_rubr(x):
        for a,b in [
                  ('Салон_за_класифицирана_словесност', 'ССл'
                ),('Салон_за_класифицирана', 'ССл'
                ),('Голямата_къща_на_смешните_хора', 'ГКСХ'
                ),('Златните_гласове_на_радиото', 'Златните_гласове'
                ),('Запазе?на_марка', ''
                ),('Детски_радиотеатър', 'Рт_деца'
                ),('Рт_за_деца',         'Рт_деца'
                ),('Ради?отеатър',    'Рт'
                )]:
            x = re.sub( a,b, x, flags= re.IGNORECASE)
        return x.lstrip('_')
    otkyde = str(opis.get( 'откъде', '') or '').split()
    rubrika_kysa = otkyde[0]
    if rubrika_kysa.isdigit(): rubrika_kysa = ''
    else:
        rubrika_kysa = sykr_rubr(rubrika_kysa)

    rubrika_orig = opis.get( 'ориг_рубрика')
    ime = re.sub( 'документа\w+', 'док.', ime, flags= re.IGNORECASE)

    if 'еко-ехо' in rubrika_kysa.lower(): ime = avtor = ''
    ###if len(ime)>30 and opis.get( 'ориг_описание', '').startswith( ime): ime = '' #HACK

    ime = rec2dir.filt_er( ime)
    ime = sykr_rubr( ime)
    if ime in (rubrika_kysa, rubrika_orig): ime = ''
    if ime.startswith( rubrika_kysa+'_:'):
        ime = ime[ len( rubrika_kysa+'_:'):]
    ime = ime.strip('_')

    imeavtor = [ ime, avtor ] if not optz.ime_sled_avtor else [ avtor, ime ]
    ldirname = spc(rec2dir.filt_er( optz.razdeli_ime_avtor.join( a for a in imeavtor if a )))
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

    popodredba = dict( ime= ldirname[:90], rubr= rubrika_kysa, vreme =kanal_vreme)
    podredba = dict( s.split('=') for s in _podredbi)[ optz.podredba ]
    ldirname = spc(optz.razdeli_drugi).join( popodredba[i] for i in podredba.split('+') if popodredba[i] )

    #if optz.prefix: ldirname = optz.prefix + ldirname

    cmd = print
    if optz.move: cmd = os.rename
    if optz.link: cmd = os.symlink
    if optz.target: ldirname = os.path.join( optz.target, ldirname)
    try:
        cmd( dir, ldirname)
    except FileExistsError as e:
        if not optz.quiet: print( e)

# vim:ts=4:sw=4:expandtab

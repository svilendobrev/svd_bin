#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from svd_util.struct import DictAttr, attr2item
from svd_util.lists import appendif, extendif, listif
import re

def realt( x): return '('+'|'.join( x)+')'

izdateli = DictAttr(
    kynev   = 'Кънев',
    pan     = 'Пан',
    bnr     = 'БНР',
    gega    = 'ГегаНю',
    litia   = 'Лития',
    rem     = 'РЕМ',
    suprafon= 'Супрафон',
    balkanton= 'БалканТон',
    balkanton_kys = 'БТон',
    polysound= 'ПолиСаунд',
    orfei    = 'Орфей',
    ckt      = 'ЦентраленКукленТеатър',
    ckt_kys  = 'ЦКТ',
)
r_izdateli = dict( (v,k) for k,v in izdateli.items())
radio  = 'радио'
org_izdateli = { izdateli.balkanton, radio }

_izdatel4opis = dict( (izdateli[k],izdateli[k].lower()) for k in 'balkanton pan litia bnr kynev polysound orfei'.split())
def izdatel4opis( i):
    return _izdatel4opis.get( i,i)

re_bton_sig = re.compile( '[бв]([еат][амнк])-?(\d+)', re.IGNORECASE)# '--в\1\2' *
def re_bton_sig_repl( m):
    return ('в'+m.group(1)).upper() + m.group(2)
def nomer4opis( n):
    n = re_bton_sig.sub( re_bton_sig_repl, n)
    n = n.replace( 'ВТТЕС', 'ВТТеС')
    n = n.replace( 'АДД', 'ADD')
    n = n.replace( 'ААД', 'AAD')
    n = n.replace( 'СД', 'cd')
    n = n.replace( 'РАДИОПРОМ', 'радиопром')
    return n

kaseta = 'касета'
ploca  = 'плоча'
ploca1 = 'малка.плоча'
ploca2 = 'плоча_малка'
disk   = 'диск'
lenta  = 'лента'
tv     = 'ТВ'

nositel4izdatel = {
    ploca:  [ izdateli.balkanton, izdateli.balkanton_kys, ],
    ploca2: [ izdateli.suprafon],
    kaseta: [ izdateli.kynev, izdateli.pan, izdateli.rem, izdateli.litia ],
    disk:   [ izdateli.polysound, izdateli.bnr, izdateli.orfei ],
}
nositel4izdatel = dict( (k, [ v.lower() for v in vv]) for k,vv in nositel4izdatel.items() )

balkanton = izdateli.balkanton.lower()
balkanton_kys = izdateli.balkanton_kys.lower()

izdateli_kys = {
    balkanton   : balkanton_kys,
    izdateli.ckt.lower(): izdateli.ckt_kys.lower(),
}
def izdatel_kys( i):
    k = i and izdateli_kys.get( i.lower())
    return k or i

#V не е валидно но може да се получи от кир.ВАА->lat2cyr()->VAA
bukvi_lat = 'A V B E X M H T C O K P D'.replace(' ','') #e
bukvi_cyr = 'А В В Е Х М Н Т С О К Р Д'.replace(' ','') #е
txbton = dict( zip( bukvi_cyr.lower(), bukvi_lat.lower()) )
txbton[ 'б' ] = 'вbv'
txbton[ 'в' ] = 'бbv'

def eqcyrlat( x):
    return ''.join(
        '['+a+txbton[a]+']' if a in txbton else a
        for a in x.lower() )

re_izdanie = DictAttr(
    (k, re.compile( '(?P<kod>'+'|'.join( eqcyrlat(x) for x in v.split())+')-?(?P<nomer>[\d,]+)', re.IGNORECASE))
    for k,v in dict(
        bton_ploca = 'б'+realt('тнаесокрх')+realt('амкн') +' бтонр? радиопром',
        bton_kaseta = 'бамс бттес',
        disk = 'cd add',
    ).items() )

nositeli = {
    'cd': disk,
    'mc': kaseta,
    'lp': ploca,
    'tv': tv,
    'ep': ploca2,
    disk: disk,
    ploca: ploca,
    ploca1: ploca2,
    ploca2: ploca2,
    kaseta: kaseta,
    lenta: lenta,
}

kysi_cyr = {
    kaseta:     'мк',
    ploca:      'пл',
    ploca+'?':  'пл',
}
kysi_lat = {
    kaseta:     'mc',
    ploca:      'lp',
    ploca+'?':  'lp',
    ploca2:     'ep',
    ploca1:     'ep',
    disk :      'cd',
    tv:         'tv',
}

def e_nositel( izdania, *vidove):
    for izdanie in izdania.lower().split():
        for a in vidove:
            if isinstance( a, str):
                if izdanie.startswith( a): return True
            elif a.search( izdanie): return True

def e_balkanton( izdanie):
    if balkanton in izdanie.lower() or balkanton_kys in izdanie.lower(): return True
    return e_nositel( izdanie, re_izdanie.bton_kaseta, re_izdanie.bton_ploca)

def koi_izdatel( izdanie, kys =False, strict =False):
    izd = izdanie.lower()
    for i in izd.split():
        if i in (radio, izdateli.bnr.lower()): return radio #izdateli.bnr
    if e_balkanton( izd): return kys and izdateli.balkanton_kys or izdateli.balkanton
    for k,v in izdateli.items():
        if k.lower() in izd or v.lower() in izd:
            return kys and izdatel_kys( v) or v
    ff = izdanie.split( '-', 1)
    if len(ff)==2:
        if ff[0].lower() in nositeli:
            r = ff[1]
            if r.strip('?') in ('', 'друг', 'друга'): return ''
            return r
    return izdanie

def koi_nositel( izdania):
    for izdanie in izdania.lower().split():
        if e_nositel( izdanie, re_izdanie.disk, disk, 'cd-') : return disk
        if e_nositel( izdanie, re_izdanie.bton_kaseta, kaseta, 'mc-' ): return kaseta
        if e_nositel( izdanie, ploca1,ploca2 ): return ploca2
        if e_nositel( izdanie, re_izdanie.bton_ploca, ploca ): return ploca
        if radio in izdanie: return radio
        if balkanton in izdanie.lower(): return ploca+'?'
        if izdanie in nositeli: return izdanie
    return '?'


bxa_godini = sorted( {
# 6395: 1960,
 491: 1966,
 1052 : 1968,
 1149 : 1969,
 1181 : 1970,
 1301 : 1971,
 1348 : 1972,
 1501 : 1973,
 1674 : 1974,
 1741 : 1975,
 1948 : 1976,
 2063 : 1977,
 2100 : 1978,
 2198 : 1978,
 2200 : None,
 10000: 1979,
 10449: 1980,
 10608: 1981,
 10926: 1982,
 10986: 1983,
 11253: 1984,
 11391: 1985,
 11676: 1986,
 12062: 1987,
 12257: 1988,
 12582: 1989,
 12709: 1990,

 19000: 1994,
}.items())
'''
ВТА-12781 - CONSTANTIN J.B-COUNTRI / WESTERN
'''

'''
В = Балкантон
ВТА- танцова музика
ВНА- народна музика
ВАА- художествено слово
ВЕА- детски песни
ВСА- симфонична музика
ВОА- оперна музика
ВКА- камерна музика
ВРА- оперетна музика
ВХА- хорова музика ?
ВМА- чужда народна музика
крайна Буква "А" = 30 сантиметрова дългосвиреща плоча 33 (или 45 об)
крайна Буква "М" = Малки плочи на 33 оборота - Спрени от производство около 1973г
крайна Буква "К" = малки плочи на 45 оборота ("Краткосвиреща")
крайна Буква "Н" = 10" на 33 оборота ("Нормална") .. т.е. средни?
има и стари малки плочи 33об само с номер без сигнатура
Независимо от сигнатурата, номерацията расте и е обща за всички жанрове музика

но има и КК*:
ККХ 1005 - Борис Христов
ККО 1004 - Николай Гяуров

последните са:
BTTxL 1016 -  Богомил Манов и Херувими

'''


def bton_nomer2godina( nomer):
    m = re_izdanie.bton_ploca.match( nomer)
    if not m: return None
    kod = m.group('kod').lower()
    nomera = m.group('nomer')
    nom = int( nomera.split(',')[0])
    godina = 1965
    gg = str( godina)+'?'
    #XXX това предполага вече преведен код+номер
    if len(kod)==3 and kod[0] in 'бв' and kod[-1] not in 'кмн':
        for n,g in bxa_godini:
            if nom >=n: godina = g
            if n > nom: break
    return godina and str( godina) or gg, kod, nomera

def izdanie_razglobi( izdanie):
    neznajno = '?' in izdanie
    izdanie = izdanie.replace( '?','')
    i = izdanie
    godina = None
    sg = izdanie.rsplit('/',1)
    if len(sg)==2:
        i,g = (s.strip() for s in sg)
        if g: godina = g

    s = i.split('-')
    nositel = koi_nositel( i)
    izdatel = koi_izdatel( i)
    izd_kys = koi_izdatel( i, kys=True)

    pp = [ p.lower().strip('?')
            for p in (nositel, izdatel, izd_kys, r_izdateli.get( izdatel, izdatel) ) ]
    nn = []
    for a in s:
        b = a.lower()
        if not b or b in pp: continue
        if b in nositeli or b in kysi_cyr.values(): continue
        appendif( nn, a)
    nomer = '-'.join( nn)
    godina2nomer = False
    if izdatel.lower()==balkanton and nomer and nositel in (ploca, ploca1, ploca2):
        nomer = nomer.upper()
        for l,c in zip( bukvi_lat, bukvi_cyr):
            nomer = nomer.replace( l,c)
        gkm = bton_nomer2godina( nomer)
        if gkm:
            god,kod,nom = gkm
            nomer = kod.upper()+str(nom)
            if not (godina or '').strip('?'):
                godina = god
                godina2nomer = True
    if nositeli.get( izdatel)== nositel: izdatel = nositel   #ploca1/ploca2
    return DictAttr( nositel=nositel, izdatel=izdatel, nomer=nomer, neznajno= neznajno, godina=godina, godina2nomer=godina2nomer)

def izdanie_sglobi( nositel, izdatel, nomer, neznajno =False, godina =None, opis= False, godina2nomer =False):
    #prn( locals(), koi_izdatel( nomer), koi_nositel( nomer) )
    if not nomer:
        if koi_nositel( izdatel) ==nositel: nositel = ''
    else:
        if koi_izdatel( nomer) ==izdatel: izdatel = ''
        if koi_nositel( nomer) ==nositel: nositel = ''

    if opis:
        izdatel = izdatel4opis( izdatel)
        #nositel = nositel4opis( nositel)
        nomer = nomer4opis( nomer)
    r = '-'.join( listif( [a for a in (nositel, nomer, izdatel) if a]))
    if godina and not godina2nomer: r+='/'+str(godina)
    if '?' not in r and neznajno: r += '?'
    return r

fname_kaseta  = re.compile( '(касета|kaseta|bamc|вамс|[\.-]mc\.)')
fname_cd      = re.compile( '[\.-](cd|add)')
fname_ploca   = re.compile( '(плоча|ploch?a|[\.-]lp\.|[\.-](b[a-z][a-z])\d{4,5}|-\d{5}\.)')
#fname_radio   = re.compile( '-radio')
def koi_nositel4fname( fname, media, izdanie):
    if fname_kaseta.search( fname.lower()): return kaseta
    if fname_cd.search(   fname):   return disk
    if fname_ploca.search( fname):  return ploca
    if media == radio: return ''
    if media in (disk, kaseta): return media
    izdanie = izdanie.lower().strip('?')
    for k,vv in nositel4izdatel.items():
        if izdanie in vv: return k
    return ''

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opisvane
from opisvane import zaglavie, prn, dictOrder, dict_lower, make_dict_attr, make_dict_trans, str2list, fnmatch_list, cyr2lat
from opisvane import appendif, extendif, setorder, listif
from util.struct import DictAttr, attr2item
from util import optz
import collections
import subprocess, re, os, glob
from os.path import isdir, basename, exists, join, dirname

import mp3times

from abbr import Abbr, razdeli_kamila, razdeli_kamila2

''' metafiles:
time.cache  :вх/изх; общо времетраене
opis        :вх/изх; всички данни
org/da.imeorg :вх: добавя imeorg към произхода
org/ne.imeorg :пропуска
*.mp3/*.wma :вх, звукови файлове
*.jpg :вх, картинки
'''


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
)
r_izdateli = dict( (v,k) for k,v in izdateli.items())
radio  = 'радио'
org_izdateli = { izdateli.balkanton, radio }

def izdatel4opis( i):
    if i in (izdateli[k] for k in 'balkanton pan litia bnr kynev polysound orfei'.split()): return i.lower()
    return i
def nomer4opis( n):
    n = n.replace( 'ВТТЕС', 'ВТТеС')
    n = n.replace( 'АДД', 'ADD')
    n = n.replace( 'ААД', 'AAD')
    n = n.replace( 'СД', 'cd')
    n = n.replace( 'РАДИОПРОМ', 'радиопром')
    return n

kaseta = 'касета'
ploca  = 'плоча'
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

def izdatel_kys( i):
    if i and i.lower() in (balkanton, balkanton_kys): return izdateli.balkanton_kys
    return i

re_izdanie = DictAttr(
    (k, re.compile( '('+'|'.join(v.split())+')(\d+)', re.IGNORECASE))
    for k,v in dict(
        bton_ploca = '[бв][а-я][а-я] b[a-z][a-z] бтонр радиопром',
        bton_kaseta = '[бв]амс bamc [бв]ттес',
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
    disk :      'cd',
    tv:         'tv',
}

bukvi_lat = 'A B E X M H T C O K D e P'.split()
bukvi_cyr = 'А В Е Х М Н Т С О К Д е Р'.split()

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
    if e_balkanton( izd): return kys and izdateli.balkanton_kys or izdateli.balkanton
    for k,v in izdateli.items():
        if k.lower() in izd or v.lower() in izd: return v
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
        if e_nositel( izdanie, ploca2 ): return ploca2
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

def bton_nomer2godina( nomer):
    m = re_izdanie.bton_ploca.match( nomer)
    if not m: return None
    kod = m.group(1).lower()
    nom = int( m.group(2))
    godina = 1965
    gg = str( godina)+'?'
    if kod[0] in 'бв' and kod[-1] != 'м':
        for n,g in bxa_godini:
            if nom >=n: godina = g
            if n > nom: break
    return godina and str( godina) or gg

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
    if izdatel.lower()==balkanton and nomer and nositel in (ploca, ploca2):
        nomer = nomer.upper()
        for l,c in zip( bukvi_lat, bukvi_cyr):
            nomer = nomer.replace( l,c)
        if not godina or not godina.strip('?'):
            godina = bton_nomer2godina( nomer)
            godina2nomer = True
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

fname_kaseta  = re.compile( '(касета|kaseta|bamc|[\.-]mc\.)')
fname_cd      = re.compile( '[\.-](cd|add)')
fname_ploca   = re.compile( '(плоча|ploch?a|[\.-]lp\.|[\.-](b[a-z][a-z])\d{4,5}|-\d{5}\.)')
#fname_radio   = re.compile( '-radio')
def koi_nositel4fname( fname, media, izdanie):
    if fname_kaseta.search( fname): return kaseta
    if fname_cd.search(   fname):   return disk
    if fname_ploca.search( fname):  return ploca
    if media == radio: return ''
    if media in (disk, kaseta): return media
    izdanie = izdanie.lower().strip('?')
    for k,vv in nositel4izdatel.items():
        if izdanie in vv: return k
    return ''



extra_exts= set( kysi_lat.values())
IKONA = '.ikona.jpg'
MIKONA = '.m'+IKONA
from datetime import datetime
sega_fmt = '%y%m%d'
sega = datetime.today()

tipove_ = dictOrder()
tipove= attr2item( tipove_)
tipove.prikazki= DictAttr( url= 'prikazki', pyt= 'prikazki',
        ime= 'приказки',
        dylgo= 'детски приказки и театър',
        )
tipove.pesni   = DictAttr( url= 'pesnicki', pyt= 'pesni',
        ime= 'песнички',
        dylgo= 'детски песни и стихове',
        )
tipove.zagolemi= DictAttr( url= 'zagolemi', pyt= 'teatyr',
        ime= 'за възрастни',
        dylgo= 'театър и стихове за възрастни',
        )

shabloni = '''
        шапка/елементи
        елементи:
            автори
                с-изпълнители   = изпълнители-в-автор
                с-участници     = участници-в-автор
                с-музика-текст  = музика-текст-в-автор
            номерация   #няма смисъл за отделен елемент
                    = без-номер
                    = номер0
            именоване-файл
                    = шаблон_елемент? # преименоване-папки и прехвърляне-папки
                    = представка/prefix
                    = и-име
                    = и-автор
                    = и-номер
            етикети-мп3:
                име     := v.ime :v.izdatel_kys
                албум   := x.ime :x.etiketi.avtor :v.izdanie
                артист  := +( dai_imepylno( p.avtor1_s_uchastnici))
                номер   := (not номер0) + пореден-номер-в-описа
                година
                коментар
            в-страница/хтмл
                именоване
                автори-след-описание
            в-списък-страници/хтмл
                именоване
                без-автори
                без-описание

        шапка:
            в-страница/хтмл
                заглавие/title
                именоване-заглавие.1
            в-списък-страници/хтмл
                именоване
            именоване-папка     =шаблон # преименоване-папки и прехвърляне-папки

    '''

class nskaPrikazka:
    re_ia = '([иа])'
    re_nsk = '^([А-Яа-я][а-я]+(н|ск))'
    re_prik= 'Приказк'
    re_nsk_prikazka = re.compile( re_nsk+re_ia+'('+re_prik+re_ia+')?$')
    @classmethod
    def syvpada( me, t):
        return me.re_nsk_prikazka.match( t)
    @classmethod
    def dai_imepylno( me, t, edinstveno =None):
        if edinstveno is None:
            krai = r'\3'
        else:
            krai= edinstveno and 'а' or 'и'
        return me.re_nsk_prikazka.sub( r'\1'+krai+'Приказк'+krai, t)
        return re.sub( me.re_nsk+me.re_ia+'$', r'\1\3'+me.re_prik+r'\3', t)


class info( opisvane.info):
    @staticmethod
    def opts():
        opisvane.info.opts()
        optz.str(  'debug',   default='', help= 'списък(,) от main,dirs,sizes,times,items2,tags')
        optz.str( 'vreme_app',   type= 'choice', choices= mp3times.apps,
                help= 'проверява продължителността с този инструмент')
        optz.bool( 'dveniva',       help= 'търси файлове и в */ (освен в ./)')
        optz.str( 'proizhod_da',    help= 'подпапка за използвани оригинали-от-кого [%default]', default= '0/da.*')
        #optz.str( 'proizhod_ne',    help= 'подпапка за неползвани оригинали-от-кого [%default]', default= '0/ne.*')
        optz.bool( 'prezapis',       help= 'презаписва всички файлове (иначе само ако са различни)')

        gg = optz.grouparg( 'съкращения и участници/дейности')
        optz.str( 'sykr',           help= 'файл със съкращения (списъци имена или от грамофонче)', **gg)
        optz.str( 'sykr_spisyk',    help= 'прави файл със съкращения като списък', **gg)
        optz.str( 'sykr_moin',      help= 'прави файл със съкращения за грамофонче', **gg)
        optz.bool( 'sykr2dylgo',    help= 'разписва знайните съкращения', **gg)
        optz.bool( 'opis2dejnosti', help= 'извлича участници/дейности/роли от полето описание', **gg)

        gg = optz.grouparg( 'mp3-етикети на съдържанието')
        optz.str(  'tags_app',    type= 'choice', choices= 'mp3info eyed3'.split(),
                help= 'с кой инструмент да се слагат mp3-етикети - ако изобщо', **gg)
        optz.bool( 'tags_direct',   help= 'слага етикетите на място', **gg)
        optz.str(  'tags_enc',      help= 'кодировка на етикетите [%default]', default= 'cp1251', **gg)
        optz.str(  'tags_spisyk',       help= 'прави общ списък за слагане на етикети', **gg)
        optz.str(  'tags_po_papki',     help= 'прави списъци по папки за слагане на етикети', **gg)
        optz.str(  'tags_po_otdelno',   help= 'прави отделни рецепти за слагане на етикети', **gg)

        gg = optz.grouparg( 'преименоване на съдържанието')
        optz.str( 'spisyk_preimenovane',   help= 'прави списък за преименоване+превеждане на съдържанието', **gg)
        optz.str( 'prehvyrli_sydyrzhanie', help= 'прехвърля+превежда съдържанието към тук/', **gg)

        gg = optz.grouparg( 'html списъци')
        optz.str( 'html_enc',       help= 'кодировка на html [%default]', default='utf8', **gg)  #cp1251
        optz.bool( 'vnosa_e_obiknoven',    help= 'внесените външни папки са като обикновени', **gg)
        optz.str( 'url_koren',  default= '/detski/zvuk',    help= 'абс.адрес на общия корен', **gg)

        optz.str( 'html_index',     help= 'прави отделни html-страници по папки', **gg)
        optz.str( 'html_papka',     help= 'прави отделни html-новости-избор по папки', **gg)

        optz.str( 'html_spisyk',    help= 'прави общ списък html-страница', **gg)
        optz.str( 'html_novi',      help= 'прави общ списък новости отделен (иначе част от общия списък)', **gg)
        optz.str( 'html_izbrani',   help= 'прави общ списък само хубавите - извадка от общия списък', **gg)

#       optz.str( 'url_tuk',    default= '',                help= 'отн.адрес тук спрямо корена', **gg)
#       optz.str( 'pyt_tuk',    default= '',                help= 'отн.път   тук спрямо корена', **gg)
#       optz.str( 'pyt_kym_drugvid',    default= '../%(drugvid)s/xxx',  help= 'отн.файлов път към папка-корен от другвид (приказки/песнички/..)', **gg)
#       optz.append( 'samo_vnos',   default=[], help= 'папка-внос от/обработена другаде - показва се само в списъка', **gg)
        optz.bool( 'obshto_otgore',         help= 'слага Общо: отгоре (иначе отдолу)', **gg)
        optz.bool( 'obshto_broi_zapisi',    help= 'брои файловете със записи, а не папките', **gg)
        optz.str(  'podredba',              help= 'подрежда по изброените полета [%default]',
            default= 'humor,ime_sglobeno,pored',
                **gg)
        optz.bool( 'otkoga_e_mintime',      help= 'слага липсващо откога=най-ранното време на папката', **gg)
        optz.int( 'kolko_dni_e_novo',   default=35, help= 'толкова дни нещо се счита за ново [%default]', **gg)
        optz.int( 'kolko_sa_novi',      default=0,  help= 'толкова последни неща се считат за нови [%default]', **gg)

        optz.str( 'izdania_spisyk',    help= 'прави общ списък по издания', )


    stoinosti_simvoli = dict(
      преценка = dict(
        #за/от елементите и в папка
        preporyka   = 'преп*оръка препоръчвам',
        izbor       = 'изб*ор',
        novo        = 'ново',
        ),
      съдържание = dict(
        #за/от елементите и в папка
        zagolemi    = 'възр*астни за-големи',
        #само папката
        povtorenie  = 'повторение', #???
        koren       = 'корен без-данни', #мета/корен
        ),
      вид = dict(
        #за/от елементите и в папка
        glas1       = 'прочит',
        pesen       = 'песни песен песничка песнички',
        teatyr      = 'театър',
        humor       = 'хумор',
        stihove     = 'стих*ове стихот*ворение стихотворения',
        dokumentalni= 'документални документално док',
        muzikal     = 'мюзикъл мюзикъли',
        otkys       = 'откъс откъси',
        opera       = 'опера',
        ),

      преименоване = dict( #? може би шаблон?
        #за елементите и в папка
        prefixime   = 'и-име',
        prefixavtor = 'и-автор',
        prefixnomer = 'и-номер',
        ),
      именоване = DictAttr(     #именоване/представяне
        #само папката
        nomer       = 'номер*1',
        nomer0      = 'номер0',
        prefix      = 'представки представка префикс',
        nakratko    = 'накр*атко',               #в списъка - без описания
        #само елементите
        nakratko_bez_otdelni_avtori  = 'накратко-без-автори',   #в списъка - без отделни автори
        avtor_sled_opisanie = 'автор-след-опис*ание автор-в-опис*ание',  #в index - отделните автори не са към имената, а след описанието
        vid_v_opisanie = 'вид-след-опис*ание вид-в-опис*ание',
        #на папката/елемента
        izp_v_avtor = 'изпълнители-в-автор изп-в-автор',
        uch_v_avtor = 'участници-в-автор уч-в-автор',
        mt_v_avtor  = 'м-т-в-автор мт-в-автор музика-текст-в-автор',
        ),
    )
    stoinosti_danni = dict(
        ##поредица
        ##организатор/инициатор/постановка/запис
        #на папката/елемента
        opisanie2   = 'описание2 опис2',
        vryzki      = 'опис.връзки опис-връзки вр*ъзки връзка url wryzki wryzka',
        fon         = 'опис.фон    опис-фон    фон',
        povreda     = 'повреда',    #към описанието
        obrabotka   = 'обр*аботка',
        otkoga      = 'откога',
        otkyde      = 'откъде',
        #за/от елементите и в папка
        uchastnici  = 'уч*астници участв*ат',
        izdanie     = 'изд*ания издание',
        proizhod    = 'произход',
        proizhod2   = 'произход2',
        kachestvo   = 'кач*ество качество-съдържание/запис кач-во quality q',
        vid         = 'вид',    #полу-изчислимо
        #само папката
        ikoni       = 'ик*они икона',
        pored       = 'поред',  #ако има няколко едноименни папки, напр. Андерсенови приказки
        #avtor       = 'автор',
        #godina      = 'година',
        #изчислими и запомнени
        vreme       = '_време продължителност',
        razmer      = '_размер големина тегло',
        options     = 'действия опции options',
    )
    stoinosti0 = DictAttr( opisvane.info.stoinosti0 )
    stoinosti0.update( stoinosti_danni)
    for simv in stoinosti_simvoli.values():
        stoinosti0.update( simv)


    def kachestva( az, **kargs):
        return kachestva( az.etiketi.kachestvo, **kargs)

    @classmethod
    def zaredi_danni( klas, args):
        klas.abbr = Abbr2()
        if klas.options.sykr:
            klas.abbr.cheti_eutf( klas.options.sykr)
            klas.abbr.popylni_avto()
        return super().zaredi_danni( args)

    vse_str_orgs = set()

    def samopopylva_etiketi( az):
        if az.etiketi.koren: return
        az._samopopylva_etiketi()
        #az._samopopylva_etiketi_otdelni( az.etiketi_papka)
        #az._samopopylva_etiketi_otdelni( az.etiketi_element)
    #def _samopopylva_etiketi_otdelni( az, etiketi):

    def _samopopylva_etiketi( az):

        d = razglobi( az.ime)
        dime = d.pop( 'ime', '')
        if dime != az.ime:
            #prn( 222222222, az.ime, dime, d)
            az.etiketi.ime = dime

        dvid = d.pop( 'vid', ())
        assert not d
        #assert not d.get('izdanie')
        #assert not d.get('kachestvo')
        #assert not d.get('avtor')

        for v in dvid:
            az.slaga_etiket( v, True)

        qcontent,qrecord = az.kachestva()
        az.etiketi.kachestvo = qcontent+'/'+qrecord

        for k in 'izdanie godina'.split():
            v = az.etiketi.get( k) or []
            if isinstance( v, str): v = v.split()
            g = d.get( k, [])
            if isinstance( g, str): g = g.split()
            vv = listif( i.lstrip('/') for i in v + g)
            az.slaga_etiket( k, ' '.join( vv))

        az._izdania = az.opravi_izdania( az.etiketi)

        eotkoga = str( az.etiketi.otkoga)
        if not eotkoga or '+' in eotkoga:
            otkoga = sega
            if az.options.otkoga_e_mintime:
                t = min( getattr( os.path, f)( az.fname ) for f in 'getmtime getctime getatime'.split() )
                otkoga = datetime.fromtimestamp( t)
            o = otkoga.strftime( sega_fmt)
            if not eotkoga:
                o = int(o)
            else:
                o = ' '.join( listif( eotkoga.strip('+').split() + [ o]))
            az.etiketi.otkoga = o
        else:
            otkoga = max( datetime.strptime( str(a), sega_fmt) for a in eotkoga.split())
        az.otkoga = otkoga

        az.orgs_files = proizhod( az.fname, az.options.proizhod_da)
        orgs_meta1 = set( az.etiketi.proizhod.split())
        if az.orgs_files and orgs_meta1 != az.orgs_files:
            az.etiketi.proizhod = ' '.join( sorted( az.orgs_files))

        az.ikoni_vse = sorted( [ basename( i) for i in glob.glob( az.fname+'/*'+MIKONA )])
        if not az.etiketi.ikoni and len(az.ikoni_vse)==1:
            az.etiketi.ikoni = az.ikoni_vse[0].replace( MIKONA, '.jpg')

        for o in 'opisanie opisanie2'.split():
            opis,lipsva = lipsva_izvadi( getattr( az.etiketi, o))
            if lipsva:
                az.slaga_etiket( o, opis)
                az.slaga_etiket( 'povreda', lipsva, zamesti= False)

        az.opravi_avtori( az.etiketi)

        ss = str2list( az.etiketi.obrabotka)
        if ss: az.etiketi.obrabotka = ss

        az.setup_prevodi()
        az.opis2hora2dejnosti()

        ime = az.ime.lower()
        #if ime.startswith( 'стихове'): az.etiketi.stihove = True
        if 'хумор' in ime: az.etiketi.humor = True

    def opravi_izdania( az, etiketi):
        if not etiketi.izdanie: return ()
        izdania = [ izdanie_razglobi( i) for i in etiketi.izdanie.split() ]
        etiketi.izdanie = ' '.join( izdanie_sglobi( opis=True, **i) for i in izdania)
        return izdania

    def options2( az, k):
        return k in az.etiketi.options

    def opis2hora2dejnosti( az):
        abbr = az.abbr

        az.uchastnici_vse = az.make_Uchastnici()

        for e in [ az.etiketi ] + list( az.prevodi.values()):
            dejnosti2hora = az.make_Uchastnici()

            if isinstance( e.uchastnici, list):
                dejnosti2hora.slaga_dejnost( az.dejnost_podrazbirane, e.uchastnici)
            elif isinstance( e.uchastnici, str):
                r = dejnosti2hora.opis2dejnosti( e.uchastnici, e)
                assert not r, e.uchastnici
            elif e.uchastnici:
                for dd,v in e.uchastnici.items():
                    vv = isinstance( v, dict) and [ v ] or ( v.split() if isinstance( v, str) else list(v) )
                    for d in dd.split('+'):
                        d = abbr.dejnosti4vse.get( d.strip('.'), d)
                        extendif( dejnosti2hora.setdefault( d, []), vv)

            # дейности извадени извън .участници
            zatriene = []
            for k,v in e.items():
                if k in az.stoinosti: continue
                d = abbr.dejnosti4vse.get( k.strip('.'))
                if not d: continue
                dejnosti2hora[ d] = (
                     isinstance( v, dict) and [ v ]
                        or ( v.split() if isinstance( v, str) else list(v) )
                     )
                zatriene.append( k)
            for k in zatriene: del e[k]

            for hora in dejnosti2hora.values():
                hh = []
                for h in hora:
                    h,r = dejnosti2hora.h2hr( h)
                    abbr.dobavi( h, e.ime)
                    if az.options.sykr2dylgo:
                        h = abbr.dai_imepylno( h, True)
                        hh.append( dejnosti2hora.hr2h( h,r))
                if hh: hora[:] = hh

            if az.options2( 'avtor2dejnosti') and e.avtor:
                dejnost_podrazbirane = None
                if e.pesen or az.etiketi.pesen or e.stihove or az.etiketi.stihove:
                    dejnost_podrazbirane = abbr.dejnosti['текст']
                aa = []
                zalepi = False
                for a in e.avtor:
                    if zalepi: aa[-1] += '+'+a
                    else: aa.append( a)
                    m = abbr.re_dejnost.search( a+'.')   #само дейност, м.
                    zalepi = m and m.end() >= len(a)

                ost = [ dejnosti2hora.opis2dejnosti( a, e, dejnost_podrazbirane)
                        for a in aa ]
                r = [ a for a in ost if a.strip() ]
                #r = '+'.join( r)
                if r: e.avtor = r
                else: del e.avtor
            else:
                for a in e.avtor:
                    hora = abbr.dobavi( a, e.ime)
                    if 0:
                        dejnosti2hora.slaga_dejnost( 'автор', hora)

            if (az.options.opis2dejnosti or az.options2( 'opis2dejnosti')) and e.opisanie:
                opis = dejnosti2hora.opis2dejnosti( e.opisanie, e)
                if opis: e.opisanie = opis
                else: del e.opisanie

            if dejnosti2hora: e.uchastnici = dejnosti2hora
            else: del e.uchastnici

            #общо за цялото
            az.uchastnici_vse.dobavi( dejnosti2hora, bezplus= True)

            if e is not az.etiketi:
                #общо за парчето
                vse = az.make_Uchastnici().dobavi( dejnosti2hora, bezplus= True )    #copy
                if az.etiketi.uchastnici:
                    for d,hh in az.etiketi.uchastnici.items():
                        if not hh: continue
                        hhmoe = dejnosti2hora.get( d)
                        if hhmoe: #донаследи
                            if hhmoe[0] != '+': continue
                            hhmoe = hhmoe[1:]
                            o = dictOrder( vse.h2hr( h) for h in hh)
                            for h in hhmoe:
                                h,r = vse.h2hr( h)
                                o[h] = joinif(' ', [o.get( h,''), r])
                            hh = [ vse.hr2h( h,r) for h,r in o.items() ]
                        vse[ d] = hh
                if vse: e.uchastnici_vse = vse

    def make_Uchastnici( az):
        r = az.Uchastnici( _prevodach= az.abbr.dejnosti4vse )
        r.abbr = az.abbr
        return r

    class Uchastnici( make_dict_trans( dictOrder)):

        def dobavi( az, *otdelni, bezplus =False):
            for o in otdelni:
                for d,hora in o.items():
                    az.slaga_dejnost( d, hora, bezplus)
            return az

        def slaga_dejnost( az, dejnost, hora, bezplus =False):
            if not hora: return
            dai_imepylno = az.abbr.dai_imepylno
            for d in isinstance( dejnost, str) and [dejnost] or dejnost:
                i = az.setdefault( d, [])
                for h in hora:
                    if bezplus and h == '+': continue
                    h,r = az.h2hr( h)
                    h = dai_imepylno( h, True)
                    appendif( i, az.hr2h( h,r))
        @staticmethod
        def h2hr( h):
            r = ''
            if isinstance( h, dict):
                assert len(h)==1, h
                h,r = list(h.items())[0]
            return h,r
        @staticmethod
        def hr2h( h,r):
            if r: h = { h: r }
            return h

        def opis2dejnosti( az, opis, element, dejnost_podrazbirane =None):
            abbr = az.abbr
            opis = abbr.re_dejnost_.sub( r'\1\2', opis)
            r = []
            for b in opis.split(';'):
                r.append( [] )
                kalpak = None
                bb = b.split()
                while bb:
                    aa = bb.pop(0)
                #for aa in b.split():
                    pred_kalpak = kalpak
                    a = aa.rstrip(',.')
                    kalpak = abbr.dai_kalpak( a)
                    if 0:
                        if kalpak and not kalpak[0].isupper():
                            prn( '??sykr', a, element.ime)
                            kalpak = None
                    if not kalpak:
                        if not a: continue
                        #if aa[0]=='(' and  pred_kalpak:    #роля?
                        #    aa='(='+aa[1:]
                        r[-1].append( aa)
                        continue

                    rolia = ''
                    while bb:
                        if bb[0]: break
                        bb.pop(0)  #next
                    if bb:
                        if bb[0][0] == '(': #roli
                            rolia = []
                            while bb:
                                rolia.append( bb.pop(0) )
                                if rolia[-1][-1]==')': break
                            rolia = ' '.join( rolia ).strip( '()' )

                    hora = abbr.dobavi( kalpak, element.ime)
                    if rolia: hora = [ { h:rolia } for h in hora ]  #TODO io only!
                    for d in abbr.dai_dejnosti( a, dejnost_podrazbirane):
                        az.slaga_dejnost( d, hora)

            opis = joinif( '; ', [' '.join(a) for a in r if a] )
            return opis



    @classmethod
    def bez_ext1x1( az, fname, exts= ()):
        return super().bez_ext1x1( fname, exts, extra_exts)

    @property
    def novo( az):
        if az.etiketi.novo: return True
        d = sega - az.otkoga
        return d.days <= az.options.kolko_dni_e_novo

    def setup_prevodi( az):
        for p in az.prevodi.values():
            ime = p.ime
            razglobeni = razglobi( ime)
            if razglobeni.get('ime') == ime: del razglobeni['ime']  #?
            for k in razglobeni.pop( 'vid', ()):
                az._slaga_etiket( k, True, p.etiketi)
            p.update_pre( **razglobeni)
            az.opravi_avtori( p)
            p._izdania = az.opravi_izdania( p)

    def setup( az):
        rfname = az.origfname
        rvse_prefix = info.vse_prefix_orig
        az.rname = rfname[ len( rvse_prefix):].strip('/')
        o = az.options

        fniva = az.fname.split('/')
        az.vnos = False

        for d in o.dirs:
            if az.fname.startswith( d.rstrip('/')+'/'):
                az.rname = az.fname[ len(d)+1:]
                break
        else:
            az.vnos = not az.options.vnosa_e_obiknoven
        if az.vnos:
            if az.options.podrobno: prn( 'vnos', az.fname)

        if tipove.pesni.url in fniva or tipove.pesni.pyt in fniva: az.tip = tipove.pesni
        elif az.etiketi.zagolemi or tipove.zagolemi.url in fniva or tipove.zagolemi.pyt in fniva: az.tip = tipove.zagolemi
        else: az.tip = tipove.prikazki

        rurl = [ az.rname]
        if az.vnos or 1:
            prname = az.rname.split('/')
            if prname[-1] == fniva[-1]:
                for p in az.tip.pyt, az.tip.url:
                    if p in fniva:
                        rurl = fniva[ fniva.index( p)+1 :]
                        break

        az.absurl = join( o.url_koren, az.tip.url, *rurl)  #path from root


        az.ikoni = [ i.replace( '.jpg', IKONA) for i in az.etiketi.ikoni.split() if 'jpg' in i]
        az.kartinki = [ i.replace( MIKONA, '.jpg') for i in az.ikoni_vse ]

        orgs_files = az.orgs_files
        orgs_meta1 = set( az.etiketi.proizhod.split())
        orgs_meta2 = set( az.etiketi.proizhod2.split())
        az.orgs = (orgs_meta1 | orgs_files | orgs_meta2) or ['svd']
        str_orgs = sorted( info.meta_prevodi.get( s, s) for s in az.orgs )
        az.vse_str_orgs.update( str_orgs)
        az.str_orgs = ' '.join( str_orgs)

        def vid4ime( **k):
            return [ a for a in [
                az.znak( 'muzikal', **k) and az.stoinosti.muzikal,
                az.znak( 'otkys', **k)   and az.stoinosti.otkys,
            ] if a]
        az.vid4ime = vid4ime()

        #елементи
        az.soundfiles = [ DictAttr( fname=f) for f in soundfiles( az.fname, o) ]
        if not az.soundfiles:
            if az.etiketi.papka: return
            prn( '!empty', az.fname)

        for v in az.soundfiles:
            #при 1 ниво bname == name
            v.bname = basename( v.fname)
            v.name = v.fname[ 1+len( az.fname.rstrip('/')):]
            v.relname = join( az.rname, v.name)

        avtor = az.etiketi.avtor

        if not az.prevodi and len( az.soundfiles) == 1:
            az.soundfiles[0].update( ime=az.ime, avtor=avtor, izdanie=None, godina=None, _izdania=())
        else:
            az.prevedi_elementi()
            for v in az.soundfiles:
                nm = az.bez_ext( v.name)
                bez_ext = az.bez_ext1x1( v.name)
                if v.name != v.bname:
                    bez_ext += az.bez_ext1x1( v.bname)
                p = None
                pnm = ''
                for m in bez_ext:
                    if not pnm: pnm = az.file_prevodi.get( m)
                    p = az.prevodi.get( m)
                    if p: break

                #и понеже преводът с :автор може да е скапан с .mp3 в prevedi_elementi..
                v.ime = pnm and az.bez_ext( pnm, extra_exts=extra_exts)
                if not v.ime or v.ime == nm:
                    v.ime = nm
                    if re.search( nm, '[a-zA-Z]') or o.podrobno:
                        prn( '!prevod?', v.relname)

                if az.etiketi.prefix:
                    pfx = az.etiketi.prefix
                    v.ime = bez_pfx( v.ime, pfx, zaglavie( pfx)).strip()

                grupa = p and p.grupa

                if grupa:
                    grupa_kysa = grupa.kyso+':'
                    grupa = grupa.ime
                else:
                    grupa = grupa_kysa = ''

                smes = dict( ime= v.ime, avtor= avtor,
                    godina= None, izdanie= None,
                    kachestvo= '', opisanie= '',
                    )
                bez = ['ime']
                if not p:
                    p = razglobi( v.ime)
                    #TODO... създава превод ако има метаинфо в името
                    bez = ()
                    if p.get('vid'): p.etiketi = p.pop('vid')
                    az.opravi_avtori( p)

                for k in smes:
                    if k in bez: continue
                    s = p.get( k)
                    if s:
                        if isinstance( s, str) and s.startswith('+'): s = str(smes[k]) + s
                        elif isinstance( s, (tuple,list)) and s[0].startswith('+'):
                            s = list( smes[k])
                            extendif( s, (x.lstrip('+') for x in s ))
                        smes[k] = s

                v.update( grupa= grupa, **smes)
                for k in 'uchastnici uchastnici_vse sydyrzhanie opisanie2 otkyde vryzki povreda etiketi _izdania'.split():
                    u = p.get( k)
                    #if u:
                    v[k]=u
                #TODO a tezi?
                v.ime_bez_grupa = bez_pfx( v.ime, grupa_kysa, zaglavie( grupa_kysa) ).strip()
                v.ime_bez_grupa_i_nomer = re.sub( '^\d+\.', '', v.ime_bez_grupa).strip()

        #подредба
        if len( az.soundfiles) > 1:
            if o.sort_prevodi:
                az.soundfiles.sort( key= lambda v: v.ime )
            else:
                def porednost( v):
                    nm = v.name
                    if nm not in az.prevodi:
                        nm = az.bez_ext( nm)
                        if nm not in az.prevodi:
                            nm = az.bez_ext( nm, extra_exts )
                            if nm not in az.prevodi:
                                return v.name
                    return '%04d' % list( az.prevodi.keys()).index( nm.lower() )
                az.soundfiles.sort( key= porednost)

        #номерация и красоти
        izdania = []
        nositel = listif( i.nositel for i in az._izdania if i.nositel)
        if nositel: nositel = nositel[0]
        n = 0
        nn = len(az.soundfiles) - bool( az.etiketi.nomer0)
        nsz = len(str(nn))  #10:2, 9:1

        az.avtori2vse( az.etiketi, az.uchastnici_vse, avtor)

        for v in az.soundfiles:
            i = v._izdania or az._izdania
            v.izdanie_kyso = izdatel_kys( i and i[0].izdatel or '')
            v.nositel = koi_nositel4fname( v.name, nositel, v.izdanie_kyso)
            v.vid4ime = vid4ime( etiketi= v.get( 'etiketi'), za_elementi=True, )
            uchastnici_vse = v.get( 'uchastnici_vse')
            az.avtori2vse( v, uchastnici_vse, za_elementi=True)
            extendif( izdania, v._izdania )
            v._godina = listif( i.godina for i in v._izdania or () if i.godina)
            if v._godina: v._godina = min( v._godina)

            v.e_radio = ( radio in v.nositel )
            v.e_teatyr, v.vid = az.vidove( v.get( 'etiketi'), v.get( 'vid'), uchastnici_vse, v.e_radio)

            n+=1
            v.nomer = v.nomer_str = None
            if len( az.soundfiles)!=1 and az.etiketi.nomer or az.etiketi.nomer0:
                nr = n
                if az.etiketi.nomer0: nr = n-1
                v.nomer = nr
                v.nomer_str = str(nr).zfill(nsz)

        #обобщаващи
        az.nositel = sorted( set( v.nositel for v in az.soundfiles if v.nositel))
        extendif( izdania, az._izdania)
        az._izdania_vse = izdania
        az.izdateli = set( v.izdatel for v in izdania if v.izdatel)
        if izdateli.balkanton in az.izdateli:
            az.izdateli &= org_izdateli
        az.izdateli = sorted( az.izdateli)
        g1 = az.etiketi.godina.split()
        g2 = [i.godina for i in az._izdania if i.godina]
        g3 = [i.godina for i in izdania if i.godina]
        az.godina = g1 and min(g1) or g2 and min(g2) or ''
        az.godina_min = az.godina or g3 and min(g3) or ''

        eradio = ( radio in az.nositel or radio in az.izdateli)
        eteatyr, az.vid = az.vidove( az.etiketi, az.etiketi.vid, az.uchastnici_vse, eradio)
        az.e_radio = eradio
        az.e_teatyr = eteatyr

        az.v_zaglavieto2 = [ i==radio and eteatyr and 'радиотеатър' or i
                                for i in az.izdateli]
        az.v_zaglavieto = [ i=='радиотеатър' and i+'/драматизация' or i
                                for i in az.v_zaglavieto2]
        if eteatyr and 'радиотеатър/драматизация' not in az.v_zaglavieto:
            az.v_zaglavieto += [ 'театър/драматизация' ]

    def vidove( az, etiketi, vid ='', uchastnici_vse =(), eradio =False):
        eteatyr = ( etiketi and etiketi.teatyr
                    or uchastnici_vse and bool(
                          uchastnici_vse.get( 'драматизация')
                       or uchastnici_vse.get( 'адаптация')
                       or uchastnici_vse.get( 'режисьор')
                       or len( uchastnici_vse.get( 'изпълнение',()))>1
                       ))

        #TODO множ.число/род
        vid = vid and vid.split() or etiketi and sorted( v for v in [
                etiketi.dokumentalni and az.stoinosti.dokumentalni,
                etiketi.stihove      and az.stoinosti.stihove,
                etiketi.pesen        and az.stoinosti.pesen,
                etiketi.glas1        and az.stoinosti.glas1,
                etiketi.humor        and az.stoinosti.humor,
                etiketi.muzikal      and az.stoinosti.muzikal,
            ] if v) or ()
        if eteatyr:
            if not vid:
                vid = [ eradio and 'радиотеатър/драматизация' or 'театър/драматизация']
            else: eteatyr = False
        return eteatyr, vid

    class Prevod( opisvane.info.Prevod):
        _vytr_svoistva = opisvane.info.Prevod._vytr_svoistva + '_izdania'.split()
        _izdania = ()


    @classmethod
    def all( klas):
        all( sorted( (x for x in klas.vse.values() if not x.etiketi.koren), key= lambda x: x.ime), klas.options)
        super().all()

    def opravi_avtori( az, et):
        abbr = az.abbr
        avtor = et.get('avtor')
        if not avtor: return
        #edinstveno = et is not az.etiketi or len( az.prevodi)<=1
        aa = []
        if isinstance( avtor, str): avtor = avtor.split()
        for av in avtor:
            for a in av.split('+'):
                if not a:
                    if not aa: a = '+'    #startswith +
                    else: continue
                else:
                    if a.islower(): a = zaglavie( a)
                    a = abbr.dai_imepylno( a) or nskaPrikazka.dai_imepylno( a)#, edinstveno=edinstveno)
                appendif( aa, a)
        et.avtor = aa


    def znak( az, t, etiketi =None, za_elementi =False):
            r = az.etiketi[ t]
            if not za_elementi: return r or az.etiketi_papka[t]
            return r or az.etiketi_element[t] or  etiketi and etiketi[ t]

    def avtori2vse( az, v, uchastnici_vse =None, avtor =(), za_elementi =False):
        v.avtor1 = v.avtor and [ nskaPrikazka.dai_imepylno( a, edinstveno=True)
                                    for a in v.avtor] or avtor
        aa = []
        vetiketi = v.get( 'etiketi')
        def znak( t): return az.znak( t, vetiketi, za_elementi)
        if uchastnici_vse:    #ред: текст, музика, изпълнение, всички други
            c = []
            z = DictAttr( (k, znak(k)) for k in 'uch_v_avtor izp_v_avtor mt_v_avtor pesen muzikal stihove'.split())
            izp = z.izp_v_avtor or z.uch_v_avtor or za_elementi and (z.stihove or z.pesen)
            if izp and z.pesen: appendif( c, 'изпълнение')
            if za_elementi and z.pesen or z.muzikal or z.mt_v_avtor or z.uch_v_avtor:
                mt = 'либрето текст'.split()
                m = 'музика'.split()
                if z.muzikal or z.pesen: mt = m+mt
                else:    mt = mt+m
                c += mt
            if izp: appendif( c, 'изпълнение')
            #if z.pesen: prn( 11111111, v.ime, c, z, uchastnici_vse)
            for a in c:
                ii = uchastnici_vse.get( a)
                if not ii: continue
                if a=='изпълнение' and len(ii)>=3 and not (z.uch_v_avtor or z.izp_v_avtor):
                    continue
                extendif( aa, ii)
            if z.uch_v_avtor:
                for u in uchastnici_vse.values():
                    extendif( aa, u)
        aa = [ az.Uchastnici.h2hr(h)[0] for h in aa]
        v.avtor1_s_uchastnici = list( v.avtor1 or ())
        extendif( v.avtor1_s_uchastnici, aa)
        v.avtor_s_uchastnici = list( v.avtor or ())
        extendif( v.avtor_s_uchastnici, aa)

    def sykrati_avtori( az, aa):
        dai_kyso = az.abbr.dai_kyso
        rr = [ dai_kyso( h, original= False) or h
                for h in aa]
        return '+'.join( rr)


def kachestva( k, as_dict =False, default ='?'):
    if k and '/' in k:
        qcontent,qrecord = k.split('/')
    else:
        qcontent = qrecord = k or ''
    qcontent = qcontent.strip() or default
    qrecord  = qrecord.strip() or default
    if as_dict: return dict( qcontent= qcontent, qrecord= qrecord)
    return qcontent, qrecord

def save_if_diff( *a,**k):
    return opisvane.save_if_diff(
        naistina= info.options.davai,
        podrobno= not info.options.davai,
        prezapis= info.options.prezapis,
        *a,**k)


def anea( a, t, sep=''): return t and sep.join( ['<'+a+'>',t,'</'+a+'>'])
def bold( t, **k):  return anea( 'b', t, **k)
def ital( t, **k):  return anea( 'i', t, **k)
def h4( t, sep=' '): return anea( 'h4', t, sep)
def h1( t, sep=' '): return anea( 'h1', t, sep)
def blockquote( t, sep= '\n '): return anea( 'blockquote', t, sep)
def center( t, sep= '\n'):  return anea( 'center', t, sep)
def font_1( t, sep=''   ):  return t and sep.join( ['<font size=-1>',t,'</font>'])
def joinif( j,tt):  return j.join( [t.strip() for t in tt if t and t.strip() ])
def divl( l, klas =''): return l and [
    '<div'+(klas and ' class='+klas or '') + '>'
    ] + l + [ '</div>' ]



def bez_pfx( t, *pfx):
    for p in pfx:
        if p and t.startswith(p):
            t = t[ len(p):]
    return t

def sglobi( ime, avtor='', vid ='', izdanie ='', godina='', nomer =None, html= True):
    r = zaglavie( ime)
    if vid:
        if isinstance( vid, str): vid = vid.split()
        for i in vid:
            assert i not in r
            r += ' -'+ i
    if avtor:
        if not isinstance( avtor, str): avtor = '+'.join( avtor)
        if html: avtor = ital( avtor)
        r += ' :'+ avtor
    for gi in izdanie, godina:
        if not gi: continue
        if isinstance( gi, int): gi = str(gi)
        if isinstance( gi, str): gi = gi.split()
        for i in gi: r += ' /'+ i.lstrip('/')

    if nomer is not None:
        r = nomer + '.' + r
    return r

re_all = re.compile( ' ('+ '|'.join( [
    '(?P<kachestvo>[*~?+-]/[~?+-])',
    '-(?P<vid>песен|песни|мюзикъли?|откъси?)',
    ':(?P<avtor>\S+)',
    '/(?P<godina>\d+\??)',  #(-\d+\??)?
    '/(?P<izdanie>\S+)',
    ]) +')$', re.IGNORECASE)

def razglobi( ime ):
    #ime -vid :avtor [extra]/izdanie /godina; opisanie
    d = DictAttr()
    ime = ime.strip()
    if ';' in ime:
        ime,d.opisanie = (a.strip() for a in ime.split( ';', 1))

    while 1:
        m = re_all.search( ime)
        if not m: break
        for k,v in m.groupdict().items():
            if not v or not v.strip(): continue
            d.setdefault( k, []).insert( 0, v.strip() )
        ime = ime[0:m.start()] + ime[ m.end():]
        ime = ime.strip()

    d.ime = ime
    return DictAttr( (k,v) for k,v in d.items() if v)

def lipsva_izvadi( t):
    mm = re.split( '(липсва .*)', t, 1)
    if len(mm)<3: return t,''
    start, lipsva, end = [m.strip(' ;') for m in mm]
    t = joinif( ' ; ', [start, end ])
    return t,lipsva
def lipsva_udebeli( t):
    return re.sub( '(липсва \S+)', bold( r'\1'), t)

##############

def soundfiles( fn, options ):
    soundfiles = glob.glob( fn+'/*.mp3') #+ glob.glob( fn+'/*.wma')
    if options.dveniva:
        innerfiles = glob.glob( fn+'/*/*.mp3') #+ glob.glob( fn+'/*/*.wma')

        soundfiles += [ i for i in innerfiles
                        if not fnmatch_list( i[len(fn):].lstrip('/').split('/')[0], options.bez) ]
    return sorted( soundfiles)

def proizhod( fn, proizhod_dir):
    return set( basename( d).split('.',1)[-1]
            for d in glob.glob( join( fn, proizhod_dir)))

def sizes( items, options):
    prn( '..размери')
    dbg = 'sizes' in options.debug
    for x in items:
        x.size = 0
        for v in x.soundfiles:
            x.size += os.path.getsize( v.fname)
        x.size = (x.size +1024*1024//2) // (1024*1024)
        if dbg: prn( x.fname, x.size)
    if dbg:
        prn( '=', sum( x.size for x in items))
        prn( 20*'#')


def time1( x, options):
    fn = x.fname
    tsec, cache = mp3times.durations( fn,
                    [ v.fname for v in x.soundfiles],
                    cache_file= fn+'/time.cache',
                    force_app= options.vreme_app
                    )
    x.time = tsec
    x.timecache = cache
    if 'time' in options.debug: prn( fn, tsec )

def times( items, options):
    prn( '..времена')
    for x in items:
        time1( x, options)
    if 'time' in options.debug:
        prn( ' =', sum( x.time for x in items)/60.0, 'min')



def ref( x):
    return 'ref_' + basename( x.fname)
NBSP = '&nbsp;'

def alt4ikona( ikona, imeavtor, media, izdanie):
    r = imeavtor +' /'+ koi_nositel4fname( ikona, media, izdanie)
    return re.sub( r'</?[a-z]+>', '', r)


def html4uchastnici( uchastnici, sykr =False, bez_dejnosti =(), samo_dejnosti =() ):
    if not uchastnici: return ''
    u = dictOrder( uchastnici)
    if samo_dejnosti: u = dictOrder( (k,u[k]) for k in samo_dejnosti if k in u )
    if bez_dejnosti: u = dictOrder( (k,v) for k,v in u.items() if k not in bez_dejnosti)
    dh = dictOrder( (d, u.pop(d)) for d in Abbr2.dejnosti if d in u)
    if u: dh.update( u)
    abbr = info.abbr
    r = []
    hd = {}
    for d,hora in dh.items():
        if d == abbr.dejnost_podrazbirane: continue
        for h in hora:
            hd.setdefault( h, []).append( d)

    def dsykr( d):
        g = abbr.dejnosti2sykr.get( d)
        return g and g+'.' or d

    for d,hora in dh.items():
        podrazb = (d == abbr.dejnost_podrazbirane)
        if sykr:
            d = dsykr( d)

            #групиране м.+т.
            if not podrazb:
                if len(hora)==1:
                    xd = hd.get( hora[0])
                    if not xd: continue     #вече изядено
                    if xd and len( xd)>1:
                        d = '+'.join( dsykr( x) for x in xd)
                        del hd[ hora[0] ]

        hh = []
        for h in hora:
            h,rolia = uchastnici.h2hr( h)
            if sykr:
                h = abbr.dai_kyso( h, original= False, min= False) or h
                if '.' not in h: h = razdeli_kamila2( h)
            else:
                h = abbr.dai_imepylno( h, True)
                h = razdeli_kamila2( h)
                if rolia: h += ' ('+ rolia +')'
            hh.append( h)
        hh = ( sykr and (not podrazb and '+' or ', ') or ', ' ).join( hh)
        r.append( (d, hh) )

    if sykr:
        r = '; '.join( d+' '+hh for d,hh in r )
    else:
        r = '<br>\n '.join( d+': '+hh for d,hh in r )
    return blockquote( r)


def href( url, ime):
    return '<a href="%(url)s"> %(ime)s</a>' % locals()
def repl( m):
    func = m.group(1)
    url = m.group(2).strip()
    ime = m.group(3).strip()
    if url.startswith( './'):
        url = '%(url2papka)s'+url[1:]
    if func == 'file':
        url = join( info.options.url_koren, url)
    elif func == 'papka':
        url = join( info.options.url_koren, url).rstrip('/')+'/'
        if func == 'zpapka':
            ime += '''<?php $i= "%(url)sikona.jpg";
                if (file_exists( $_SERVER['DOCUMENT_ROOT'] . $i)) echo "<img src='$i' height=48>";
                ?>''' % locals()
    return href( url,ime)
def url( x):
    x = re.sub( r'(url|papka|file)\[ *(\S+) *= *(.*?) *\]url', repl, x)
    return x

def html4opisanie( d):
    return blockquote( url( d.replace( '%', '%%')).replace( '\n', '\n <br> ' ))

def otkyde( o):
    if o: o = '('+o+')'
    return o

def html( x):
    url2papka = x.absurl
    x.html = DictAttr()

    size = x.size
    time = (x.time+30)//60

    izbor       = x.etiketi.izbor
    kachestvo   = x.etiketi.kachestvo
    preporyka   = x.etiketi.preporyka

    org = x.str_orgs

    q = kachestvo
    prepizbor = preporyka and '**' or izbor and '*' or ''
    if prepizbor: q = prepizbor + ' ' + q

    opisanie    = joinif( ' ; ', [ x.etiketi.opisanie,
                                   lipsva_udebeli( x.etiketi.povreda) ])
    opisanie12  = joinif( '\n', [ opisanie, x.etiketi.opisanie2, otkyde( x.etiketi.otkyde) ])
    sydyrzhanie = '\n'.join( x.etiketi.sydyrzhanie or () )

    izdanie = x.etiketi.izdanie
    nositel = x.nositel

    ime = x.ime_sglobeno2

    for a in '''
            url2papka
            q size time org
            opisanie opisanie12 sydyrzhanie
            ime nositel
            izdanie kachestvo preporyka izbor prepizbor
            '''.split():    #avtor
        x.html[a] = locals()[a]
    return x.html

def html4koloni( redove):
    nm = len(redove)
    nm2 = (len(redove)+1)//2
    if nm2<3:
        nkoloni = 1
        r = divl( redove, 'kolona0')
    else:
        nkoloni = 2
        for n in nm2, nm2-1, nm2+1, nm2-2, nm2+2:
            if n< nm and redove[n].startswith('<h4>'):  #HACK
                nm2 = n
                break

        r = divl( redove[ :nm2], 'kolona1')
        r+= divl( redove[ nm2:], 'kolona2')

    return '\n'.join( ['<br>'] + r), nkoloni


def html4zapisi( x, imeavtor, sykr =False,
        bez_avtor =False,
        avtor_sled_opisanie= False,
        uchastnici= True,
        uchastnici_vse  =False,
        uchastnici_sykr =False,
        sydyrzhanie= True,
        vryzki= True,
        opis2= True,
        godina= True,
        izdanie= True,
        vid_v_opisanie =None,
        ):
    if sykr:
        #bez_avtor = x.etiketi.nakratko_bez_otdelni_avtori
        avtor_sled_opisanie =False
        uchastnici      =False
        uchastnici_vse  =False
        uchastnici_sykr =False
        sydyrzhanie =False
        vryzki =False
        opis2= False
        godina= False
        izdanie= False
    #else:
    #    avtor_sled_opisanie= x.etiketi.avtor_sled_opisanie

    if vid_v_opisanie is None:
        vid_v_opisanie = x.znak( 'vid_v_opisanie', za_elementi=True)


    def linkzapis( fname, imeavtor ):
        return href( '%(url2papka)s/'+fname, imeavtor )

    if not x.prevodi and len( x.soundfiles) == 1:
        redove = [ linkzapis( x.soundfiles[0].name, imeavtor ) ]
    else:
        grupa = ''
        redove = []
        for y in x.soundfiles:
            g = ''
            if y.grupa != grupa:
                grupa = y.grupa
                redove.append( h4( url( grupa )) )
            avtor = ()
            if not bez_avtor and y.avtor and y.avtor != x.etiketi.avtor:
                avtor = y.avtor
            r = linkzapis( y.name,
                           sglobi( y.ime_bez_grupa_i_nomer,
                                avtor= not avtor_sled_opisanie and avtor,
                                vid= y.vid4ime,
                                godina= godina and y.godina,
                                izdanie= izdanie and y.izdanie,
                                ))
            qcontent,qrecord = kachestva( y.kachestvo, default='')
            r += ' ' + qcontent


            opisanie = [ lipsva_udebeli( url( str( y.opisanie))) ]
            if opis2:
                opisanie += [ y.opisanie2 and str( y.opisanie2),
                              otkyde( y.otkyde),
                              y.povreda and lipsva_udebeli( y.povreda) or '',
                              ]

            if vid_v_opisanie:
                for k in 'stihove pesen'.split():
                    if x.znak( k, za_elementi= True, etiketi= y.etiketi):
                        v = x.stoinosti[k]
                        if sykr: v = v[0]
                        opisanie += [ '/'+ v ]

            if avtor_sled_opisanie and avtor:
                opisanie += [ ital( '+'.join( avtor)) ]
            if y.vryzki and vryzki:
                opisanie += [ html4vryzki( y.vryzki) ]

            opisanie = joinif( '\n', opisanie)

            uc = None
            if uchastnici or uchastnici_vse or uchastnici_sykr:
                koi = y.uchastnici_vse if uchastnici_vse else y.uchastnici
                uc = html4uchastnici( koi, sykr= uchastnici_sykr)

            if uc and uchastnici_sykr:
                if opisanie: opisanie += ' ; '
                opisanie += uc

            if y.sydyrzhanie and sydyrzhanie:
                opisanie += ''.join( '\n<br> '+NBSP+i for i in y.sydyrzhanie)

            if opisanie:
                r += font_1( ' - ' + opisanie )
            if uc and not uchastnici_sykr:
                r += '\n<br> ' + uc
            if not (r.endswith( 'blockquote>') or r.endswith( 'br>') ):
                r+= '<br>'
            redove.append( ' ' + r )

    return html4koloni( redove)

def html4vryzki( vryzki):
    if not vryzki: return vryzki
    return '\n'.join( href( k, v) for k,v in vryzki.items() )

def html4index( x):
    h = DictAttr( x.html, url2papka='.')

    kartinki = [ '''\
  <a href="%(k)s">
    <img src="%(i)s" alt="%(alt)s" hspace=5 align=right vspace=3 style='clear:right' >
  </a>''' % dict( locals(), alt= alt4ikona( i, x.imeavtor, h.nositel, h.izdanie))
        for k,i in sorted( zip( x.kartinki, x.ikoni_vse), key= lambda p: p[0].replace('.jpg','') ) ]

    r= ''
    #r +='<div align=right> '
    r += href( '/detski/zvuk/', 'Грамофонче-записи') + ':'
    #r += NBSP+NBSP
    for tip in tipove_.values():
        rr = ' ~ '+href( join( info.options.url_koren, tip.url)+'/', tip.ime)
        if tip is x.tip: rr = bold( rr)
        r+= rr
    #r += ' </div>'
    r += ' ~'

    r = center( font_1( '\n'+r, sep=' '), sep=' ' )+'\n'
    r += h1( x.ime) +'\n'

    qcontent,qrecord = x.kachestva()
    if qcontent == qrecord:
        if   qcontent == '?': kach_opis = ''
        elif qcontent == '+': kach_opis = 'хубави съдържание и запис'
        elif qcontent == '~': kach_opis = 'горе-долу'
        elif qcontent == '-': kach_opis = 'калпаво'
    else:
        def kachestvo_s_duma( q, vid, nastavka =''):
            kach = {
                '+': 'хубав'+nastavka+' '+vid,
                '~': vid+': горе-долу',
                '-': 'калпав'+nastavka+' '+vid,
                }
            return kach.get( q, vid+': '+q)
        kach_opis = ', '.join( [ kachestvo_s_duma( qcontent, 'съдържание', 'о'),
                                 kachestvo_s_duma( qrecord , 'запис', '') ])

    zapisi = html4zapisi( x, imeavtor= x.imeavtor, sykr= False,
                            avtor_sled_opisanie= x.znak( 'avtor_sled_opisanie', za_elementi=True),
                            )
    if kartinki: kartinki = divl( kartinki, 'kolona_kartinki')
    izdania = [ joinif( ' ', listif( i.izdatel, i.nositel, i.nomer, i.neznajno and '?') ) for i in x._izdania ]
    for a in [
        #'тип нещо = приказки',
        '\n'.join( kartinki),
        ['автор'    , ', '.join( razdeli_kamila2(a) for a in x.etiketi.avtor) ],
        ['вид' , ', '.join( x.vid) ],
        ['година'   , x.godina ],
        ['издания'  , ', '.join( izdania) ],
        joinif( '; ', [
           ( x.etiketi.izbor     and ital('нашият избор') or '' ),
           ( x.etiketi.preporyka and bold('препоръчвам') or '' ),
           ]) or None,
        ['качество' , ' '.join( [x.etiketi.kachestvo, NBSP, kach_opis ])  ],
        ['описание' , html4opisanie( h.opisanie12) % h ],
        ['връзки',  html4vryzki( x.etiketi.vryzki) ],
        ['фон',     x.etiketi.fon, ],
        ['участници', html4uchastnici( x.etiketi.uchastnici, sykr= False) ],
        '',
        [ bold('записи'), zapisi and zapisi[0] % h + (zapisi[1]>1 and '<br clear=left>' or '') ],
        ['размер'   , '%(size)sM:%(time)sмин' % h ],
        ['произход' , h.org  ],
        ['източник' , ' '.join( h.nositel) ],
        ['съдържание', html4opisanie( h.sydyrzhanie) ],
        href( 'opis', 'опис'),
        ]:
        if a is None: continue
        if not isinstance( a, str):
            k,v = a
            if not v: continue
            a = k+': '+str(v)
        r += a
        if not a.endswith( 'br clear=left>') and not a.endswith( 'blockquote>'):# and not (a.endswith('div>') or a.startswith( '<div')):
            r += ' <br>'
        r += '\n'

    h.title = 'Грамофонче: ' + x.ime_sglobeno.replace('"',"'")
    return '''\
<script language="php">
$title="%(title)s";
$lang='bg';
$hasnoen=1;
$noh1=1;
$head="
<link rel='image_src' href='/kartinki/gramofonche2.jpg'>
<link rel='stylesheet' type='text/css' href='/detski/zvuk/spisyk.css'>
";
$bodycolor='ddddc0';
include( $_SERVER['DOCUMENT_ROOT'].'/ezik.php' ); </script>

''' % h + r + '''
<?php bottom() ?> <!-- svilen 2011 -->
'''

def html_spisyk( items, table =False):
    result =''
    for x in items:
        h = x.html
        imgs = [ '<img src="%(url2papka)s/%(i)s" align=right hspace=7 alt="%(alt)s">'
                        % dict( h, i=i, alt= alt4ikona( i, x.imeavtor, h.nositel, h.izdanie) )
                    for i in reversed( x.ikoni) ] #reversed because of right align
        imgs_ime = joinif( '\n ', imgs + [ h.ime ] )
        content1 = href( h.url2papka+'/', imgs_ime)

        if x.etiketi.nakratko:
            gr = [ g.kyso+' <br>' for g in x.grupi ]
            zapisi = gr and html4koloni( gr) or ''
        else:
            zapisi = html4zapisi( x, imeavtor= '(запис)', sykr=True,
                                    bez_avtor= x.etiketi.nakratko_bez_otdelni_avtori,
                                    )

        opisanie = joinif( '\n', [
                html4opisanie( h.opisanie),
                html4uchastnici( x.uchastnici_vse, sykr= True,
                    samo_dejnosti= x.abbr.dejnosti_vazhni,
                    bez_dejnosti= ( x.papka_etiketi.nakratko_bez_otdelni_avtori and
                                    (x.papka_etiketi.mt_v_avtor or x.element_etiketi.mt_v_avtor) and
                                    'музика текст'.split() or [])
                    ),
                ])
        content2 = joinif( '\n ', [
                    zapisi and zapisi[0],
                    zapisi and zapisi[1]>1 and opisanie and '<br clear=left>',
                    opisanie
                    ] )

        result += ('''
<div><hr>
 <span class=p>%(prepizbor)s</span> ''' + #'<span class=q>
 '''%(qcontent)s
 ''' + content1 + '''
 <font size=-1> %(size)sM:%(time)sмин</font>
 ''' + content2 + '''
</div>
''') % dict( h, prepizbor= NBSP*(2-len( h.prepizbor)) + h.prepizbor,
            ** x.kachestva( as_dict=True)
            )
    result += '<br clear=all>'
    return result

def html_total( items, options):
    total_time = sum( x.html.time for x in items)  #or x.time??
    total_size = sum( x.size for x in items)

    total_n = len( items)
    #total_time_h = '%.1f' % (total_time/60.0)
    total_time_h = total_time//60
    if options.obshto_broi_zapisi:
        total_n = sum( len( x.soundfiles) for x in items)
    total = '''
общо: %(total_n)sброя / %(total_size)sMb / %(total_time_h)sчаса ''' % locals()
    return total

def sort4time4file( x):
    if not x.soundfiles: return 0
    return max( func( x.soundfiles[0].fname ) for func in (os.path.getmtime, os.path.getctime) )


def html_novi( items, options):
    nz = [ x for x in items if x.novo ]
    prn( '..new', len(nz))
    if options.kolko_sa_novi and len(nz) < options.kolko_sa_novi:
        vse = sorted( items, key= lambda x: (x.etiketi.novo, x.otkoga, x.ime))
        nz = vse[-options.kolko_sa_novi:]
    if not nz: return '',nz
    nz.sort( key= lambda x: (x.otkoga, x.ime))
    nz.reverse()
    r = [ '<ul> Последни придобивки и поправки:' ]
    for x in nz:
        rr = '<li>'
        rr += href( x.absurl+'/', x.ime_sglobeno2)
        rr += ' -- ('+ x.str_orgs +')'
        r += [rr]
    r+= ['</ul> <hr width=50%>']
    return '\n'.join(r), nz




def rename( x):
    MAXSZ = 82 #64  #dvd/joliet=64, longjoliet=103
    nms = {}

    ime0 = x.ime

    for v in x.soundfiles:
        avtor_sykr = x.sykrati_avtori( v.avtor1_s_uchastnici )
        nfn = '--'.join(
            s #cyr2lat( s.lower().replace(' ','_'))
            for s in [
                joinif( '', [
                    x.etiketi.prefixime and ime0+': ',
                    x.etiketi.prefixavtor and avtor_sykr+': ',
                    x.etiketi.prefixnomer and (v.nomer_str+'.'),
                    v.ime, ] ),
                (not x.etiketi.prefixavtor and avtor_sykr),
                #v.godina,
                v.izdanie_kyso.lower(),
                ]
            if s )

        if v.nositel:
            nfn += '.'+ kysi_lat.get( v.nositel, cyr2lat( v.nositel)).lower()
        if '-радио' in nfn and 'lp' in nfn:
            print( '!!!!!!!!!!!!!! ', nfn, v.izdanie_kyso, v.nositel, v.izdanie)
        fnoext,ext = os.path.splitext( v.name) #basename(f) )

        maxsz = MAXSZ - len(ext)
        if len(nfn)>maxsz: #try shorten
            nfn0 = nfn
            for rr in [
                ( ', ',','),
                ( '--','-'),
                ( '- ','-'),
                ( ' -','-'),
                x.etiketi.papka and ( '-'+v.izdanie, '') or (),
                ( ': ',':'),
                ( '-мюзикъл', '-мюз'),
                ( '-мюз', ''),
                ]:
                if not rr: continue
                if len(nfn)>maxsz:
                    nfn = nfn.replace( *rr)
            if len(nfn)>maxsz:
                prn( '%-50s' % fnoext )
                prn( '\t', nfn0, len(nfn0) )
                prn( (len(nfn)>maxsz) * '??', '\t', nfn, len(nfn),maxsz )

        assert nfn not in nms, (nfn,sorted(nms))
        nms[nfn]=1

        nfn += ext
        ttfile = join( x.etiketi.papka and '--'.join(
                            [ime0,
                            avtor_sykr,
                            #v.godina,
                            v.izdanie_kyso,
                            ]) or '',
                        nfn)

        qcontent,qrecord = x.kachestva()

        d = dict( all =1,
                da   = x.etiketi.preporyka,
                dobre= '+' in qcontent and not x.etiketi.preporyka,
                izbor= x.etiketi.izbor,
                moze = '~' in qcontent,
                neizv= '?' in qcontent,
                zle  = '-' in qcontent,
               )

        ttpfxs = [ join( #options.rename_dir or '',
                         x.etiketi.zagolemi and 'zagolemi' or '',
                         pfx )
                    for pfx, qv in sorted( d.items())
                    if qv ]

        yield v.relname, ttfile, ttpfxs

def rename_all( items, options):
    rename_script = []

    for x in items:
        if x.vnos: continue
        #if x.etiketi.povtorenie:
        #    prn( '!повтаря други:', x.ime)
        #    continue
        try:
            for f,ttfile,ttpfxs in rename( x):
                rename_script.append( 'rena2b( '+ ', '.join( '"'+a+'"'
                                                    for a in [f, ttfile]+ ttpfxs
                                                    ) + ' )' )
                if options.prehvyrli_sydyrzhanie:
                    ff = join( *(x.path[ :x.path.index( f.split( '/', 1)[0] )] + [f] ))
                    for ttpfx in ttpfxs:
                        tt = join( options.prehvyrli_sydyrzhanie, ttpfx, ttfile)
                        if exists( tt): continue
                        ttd = dirname( tt)
                        if not isdir( ttd): os.makedirs( ttd)
                        os.link( ff, tt)
                        stats.snds[ ff] = 1
        except:
            print( '!!!', x.ime, x.fname)
            raise

    if options.spisyk_preimenovane:
        rename_script.insert( 0, '# rena2b( src, dest, prefixes...)' )
        save_if_diff( options.spisyk_preimenovane, rename_script, prepend_py_enc= True)

def tags4mp3( x, options):
    #nokia: по първите 3 букви се познава кирилица или не... т.е. Аб.Вг не става, Абв.г става

    ikoni = x.ikoni #or x.kartinki
    if ikoni:
        image = ikoni[0].replace('.ikona','')
    else: image = None

    album_title = sglobi( x.ime,
                        x.sykrati_avtori( x.etiketi.avtor_s_uchastnici ),
                        vid= x.vid4ime,
                        html= False) #x.etiketi.izdanie) #??
    izdanie = x.etiketi.izdanie
    for v in x.soundfiles:
        avtor = '+'.join( x.abbr.dai_imepylno( h, True)
                            for h in v.avtor1_s_uchastnici )

        izdanie = koi_izdatel( v.izdanie or izdanie)#, kys=True)
        #izdanie = izdanie.lower()

        title = sglobi( v.ime,
                        vid= v.vid4ime,
                        izdanie= izdanie, html= False)#, nomer= v.nomer_str ) #avtor=avtor
        artist= avtor or ''
        album = joinif( ' :', [ album_title, izdanie, ] )
        godina= v.godina or v._godina or x.godina
        if godina:
            if isinstance( godina, str): godina = godina.split()
            if isinstance( godina, int): godina = [ str(godina) ]
            godina = [ g.strip('?') for g in godina]
            godina = str(int(godina[0]))
        nomer = v.nomer is not None and str(v.nomer) or ''

        comment = 'gramofonche@' #+','.join( x.orgs)

        if 'tags' in options.debug:
            f = v.relname
            prn( '-- %(f)-130s Title=%(title)-50s Artst=%(artist)-40s Album=%(album)s' % locals())

        d = DictAttr(
            title   = title,
            album   = album,
            artist  = artist,
            godina  = godina,
            nomer   = nomer,
            genre   = '101',    #genre 101:Speech
            comment = comment
            )
        if image: d.image = image
        yield d,v

def tags4mp3info( d):
    #id3-1
    #mp3info -a artist -t title -l album -c comment -y year -g genre
    return [ 'mp3info', '$ARGSpred',
                '-t', d.title,
                '-l', d.album,
                '-a', d.artist,
                '-y', d.godina,
                '-n', d.nomer,
                '-g', d.genre,
                '-c', d.comment,
                '$ARGSsled', '%(file)s',
              ]

def tags4eyed3( d):
    #id3-2
    #eyeD3 -a artist -t title -A album -Y year -G genre -p publisher
    # --comment=lng:description:comment
    # --lyrics=lng:description:lyrics
    # --add-image=path:type[:description]
    #   types: OTHER ICON OTHER_ICON FRONT_COVER BACK_COVER LEAFLET MEDIA LEAD_ARTIST ARTIST CONDUCTOR BAND COMPOSER LYRICIST RECORDING_LOCATION DURING_RECORDING DURING_PERFORMANCE VIDEO BRIGHT_COLORED_FISH ILLUSTRATION BAND_LOGO PUBLISHER_LOGO
    # --set-encoding=latin1|utf8|utf16-LE|utf16-BE       utf8 not supported by ID3 v2.3 tags
    # --rename=pattern --fs-encoding=..
    # -F delim   default :
    cargs = [ 'meyeD3', '$ARGSpred',
                '-t', d.title,
                '-A', d.album,
                '-a', d.artist,
                '-Y', d.godina,
                '-n', d.nomer,
                '-G', d.genre,
                '--v12', '--encv1=cp1251', #+tags_enc,  #Tag.fake1
                #'--v2', #Tag.fake2
                '--to-v2.3', '--set-encoding='+'utf16-LE',
                '--no-tagging-time-frame',
                '--remove-comments',
            ]
    if d.get( 'comment'): cargs += [ '-c', '::'+d.comment ]
    if d.get('image'): cargs += [ '--add-image', '%(image)s:FRONT_COVER' ]

    cargs += [ '$ARGSsled', '%(file)s' ]
    return cargs

apps = dict( eyed3 = tags4eyed3, mp3info = tags4mp3info)

#from util.py.wither import wither

def tags4mp3_all( items, options):
    a2app = apps[ options.tags_app.lower() ]
    o = options
    #items.sort( key= sort4time4file)
    #items.reverse()

    tags_spisyk = []
    dirpfx = '${DIR}'
    for x in items:
        if x.vnos: continue
        tags_papka = []
        for args,v in tags4mp3( x, o):
            cargs = a2app( args)
            d = DictAttr()
            d.path_rname = dirpfx+ x.rname
            d.path_fname = x.fname
            d.file_name  = v.name
            d.file_rname = dirpfx+ v.relname
            d.file_fname = v.fname
            i = args.get('image')
            d.image_name  = i and args.image
            d.image_rname = i and join( d.path_rname, d.image_name)
            d.image_fname = i and join( d.path_fname, d.image_name)

            r = ' '.join( ['$GO'] + [ not a.startswith( '$') and '"'+a+'"' or a for a in cargs] )

            tags_spisyk.append( r % dict( file= d.file_rname, image= d.image_rname) )

            rr = r % dict( file= dirpfx+d.file_name, image= d.image_name and dirpfx+d.image_name)
            tags_papka.append( rr )
            if o.tags_po_otdelno:
                save_if_diff( v.fname +'.'+ o.tags_po_otdelno,
                    rr,
                    enc= o.tags_enc, prepend_py_enc= True )
            if o.tags_direct:
                subprocess.call( [
                    c % dict( file= d.file_fname, image= d.image_fname)
                    for c in cargs ])

        if o.tags_po_papki:
            save_if_diff( join( x.fname, o.tags_po_papki),
                tags_papka,
                enc= o.tags_enc, prepend_py_enc= True )
    if o.tags_spisyk:
        save_if_diff( o.tags_spisyk, tags_spisyk, enc= o.tags_enc, prepend_py_enc= True)

##############
class Abbr2( Abbr):
    @classmethod
    def setup( az):
        d2sykr = dictOrder()
        d2vse  = dictOrder()
        for a in az.dejnosti.strip().split( '\n'):
            xx = a.split()
            if not xx: continue
            k = xx[0]
            podrazb = k[0] == '*'
            k = k.replace('*', '')
            if podrazb:
                az.dejnost_podrazbirane = k

            dd = []
            sykr = []
            sykr_avto = []
            for v in xx:
                v = v.lstrip('*')
                if v[0]=='.': appendif( sykr, v[1:] )
                v = v.lstrip('.')
                if '*' in v:
                    l,r = v.split('*')
                    vv = [ l+r[:i] for i in range( len(r))]
                    extendif( dd, vv)
                    extendif( sykr_avto, vv)
                appendif( dd, v.replace('*',''))

            d2vse[ k] = dd
            dd += [ v.replace('-',' ') for v in dd if '-' in v ]
            dd += [ cyr2lat( v) for v in dd ]
            extendif( sykr, sorted( sykr_avto, key= len))
            if sykr: d2sykr[k] = sykr
        az.dejnosti = d2vse
        az.dejnosti4vse = dict_lower( (v,k)
                for k,vv in d2vse.items()
                for v in vv
                )
        az.dejnosti4vse.update( (k,k) for k in d2vse )

        az.dejnosti2sykr = dict( (k,v[0]) for k,v in d2sykr.items() )
        ds = az.dejnosti4sykr = dict( (v,k)
                for k,vv in d2sykr.items()
                for v in vv
                )
        d = '('+'|'.join( ds.keys() )+')'
        az.re_dejnost0 = '('+d+'([.+]|\.\+))*'+d+'\.'
        az.re_dejnost  = re.compile( '^'+az.re_dejnost0)    #1
        az.re_dejnost_ = re.compile( '(^| )('+ az.re_dejnost0 +'*) +')  #много

        az.dejnosti_vazhni = [ l.split()[0].replace('*','') for l in (az.dejnosti1+az.dejnosti3).strip().split( '\n') if l.strip() ]

    def dai_dejnosti( az, a, dejnost_podrazbirane =None ):
        m = az.re_dejnost.search( a)
        dejnosti = m and [ az.dejnosti4sykr[ g]
                        for g in m.group(0).replace('.','+').split('+')
                        if g and g.isalpha() ]
        return dejnosti or [ dejnost_podrazbirane or az.dejnost_podrazbirane ]

    @staticmethod
    def nglavni(x): return sum( a.isupper() for a in x)

    def dai_kalpak( az, a):
        a = a.rstrip(',.;')
        if not a or not a[0].isalpha(): return
        ng = az.nglavni( a)
        if not ng: return
        if ng==1:
            #print( 11, a, 555555, x.ime)
            return

        kalpak = az.re_dejnost.sub( '', a)
        return kalpak

    tyrseni = {}
    def dobavi( az, tt, xime):
        r = [ i.rstrip(',?') for i in tt.split('+') ]
        r = [ i for i in r if i.strip() ]
        for i in r:
            if '.' in i: az.tyrseni.setdefault( i, set()).add( xime)
            else:
                if nskaPrikazka.syvpada( i): continue
                if az.dai_imepylno( i): continue
                az.eto_imepylno( i)
        return r

    dejnosti1 = '''
        пр*евод         .прев          преводач
        д*раматизация   .др            драматург
        ад*аптация      .адапт
        сц*енарий                      сценарист
        реж*исьор       .реж .р        режисура пост*ановка постановчик
        съст*авител                    съставил композиция
        л*ибрето        .либр
        м*узика                        комп*озитор
        текст           .т
        текст-песни     .т.п .тп       текстове
        стихове         .стих
        музика-песни    .п .м.п .мп    песни
        ар*анжимент
        дир*игент
    '''
    dejnosti2 = '''
        хор*майстор     .хорм      хор-дир*игент диригент-хор хордир
        музикално-оформление  .м.оф  .м.о  .мо    музикална-картина музикална-среда музикално-оформление муз.оф*ормление
        звуково-оформление    .зв.оф .зв .з .з.оф  .зв.еф .з.е .зе звук звукова-картина звукова-среда звуково-оформление зв.оф*ормление звукови-ефекти ефекти
        звукореж*исьор  .зв.реж    .з.реж .з.р  тонр*ежисьор
        звукооп*ератор  .зв.оп     .з.оп        тоноп*ератор
        звукоинж*енер   .зв.инж    .з.инж       тонинж*енер тонм*айстор
        звукотех*ник    .зв.тех    .з.тех .з.т  тонт*ехник *ник зв.тех*ник
        звукозапис      запис
        ред*актор
        рис*унка
        худ*ожник       .худ .худ.оф    художествено-оформление
        фот*ограф       снимки снимка
    '''
    dejnosti3 = '''
        сол*ист                         солисти
       *изп*ълнение                     изпълни*тели изпълня*ват
    '''
    dejnosti = dejnosti1 + dejnosti2 + dejnosti3

    #текст-песни е същото като текст за неща които са песни
    #музика-песни е същото като музика/композитор за неща които не са музикални, а само музикално-оформени
Abbr2.setup()


def sykr_all( items, options):
    abbr = info.abbr

    for fn,moin in [[options.sykr_spisyk,False], [options.sykr_moin,True]]:
        if not fn: continue
        r = list( abbr.zapishi( moin=moin ))
        r.append( '')
        for vid,sorter in [ [ 'съкращение', None],  [ 'изпълнение', lambda kv: sorted(kv[1])[0] ]]:
            r.append( '#? ### неизвестни, по '+ vid)
            for a, xime in sorted( abbr.tyrseni.items(), key= sorter ):
                if not abbr.dai_imepylno(a):
                    r.append( ('#? %-20s ' % a) + '; '.join( xime) )
        save_if_diff( fn, r, prepend_py_enc =True)


from util.attr import get_attrib
podredba = dict(
    #ime= 'az',
    #ime_sglobeno= 'az',
    avtor= lambda x: x.etiketi.avtor or [],
    humor= lambda x: bool( x.etiketi.humor),
    stihove= lambda x: bool( x.etiketi.stihove),
    kachestvo= lambda x: (not x.etiketi.preporyka, not x.etiketi.izbor, x.etiketi.kachestvo),
    pored= lambda x: x.etiketi.pored == '' and 999 or int(x.etiketi.pored),
)
def podredi( x):
    #TODO: nagore/nadolu?
    r = []
    for i in x.options.podredba:
        v = podredba.get( i)
        if callable( v): v = v(x)
        #elif v == 'etiketi': v = getattr( x.etiketi, i)
        else: v = get_attrib( x, i)
        r.append( v)
    return r

def all( items, options):
    prn( '..zvuci')
    for x in items:
        try:
            x.setup()
        except :
            prn( '? ? ', x.fname, x.ime)
            raise

    #prn( '..proizhod:', ' '.join( sorted( info.vse_str_orgs)))

    sykr_all( items, options)

    for x in items:
        avtor = x.etiketi.avtor_s_uchastnici
        x.imeavtor = sglobi( x.ime, avtor=avtor, vid= x.vid4ime )
        x.ime_sglobeno = sglobi( x.ime, avtor= avtor, vid= x.vid4ime,
                                izdanie= ' '.join( x.v_zaglavieto), html= False )
        x.ime_sglobeno2= sglobi( x.ime, avtor= avtor, vid= x.vid4ime,
                                izdanie= ' '.join( x.v_zaglavieto2),
                                godina= x.godina
                                )

    options.podredba = options.podredba.split(',')
    items.sort( key= podredi)

    if 'items' in options.debug:
        from pprint import pprint
        for x in items:
            prn( x.ime)
            prn( x.ime_sglobeno)
            prn( x.ime_sglobeno2)
            prn( x.uchastnici_vse)
            pprint( x.etiketi)

            #for c in x.soundfiles: pprint( c)

            prn( 20*'#')

    if options.html_spisyk or options.html_index:
        sizes( items, options)
        times( items, options)
        for x in items: html(x)

    if options.html_spisyk:
        total = html_total( items, options)
        spisyk = html_spisyk( items)
        rt = [spisyk, total]
        if options.obshto_otgore: rt.reverse()

        rnovo,novi = html_novi( items, options)
        if options.html_novi:
            save_if_diff( options.html_novi, rnovo, enc= options.html_enc )
        else:
            rt.insert( options.obshto_otgore and 0, rnovo)
        rhtml = '\n<hr>\n'.join( rt)

        save_if_diff( options.html_spisyk, rhtml, enc= options.html_enc )

        if options.html_izbrani:
            hubavi = html_spisyk( [ x for x in items if x.html.prepizbor and not x.vnos] )
            save_if_diff( options.html_izbrani, hubavi, enc= options.html_enc )

    if options.html_index:
        for x in items:
            if x.vnos: continue
            ofname = join( x.fname, options.html_index)
            try:
                save_if_diff( ofname, html4index( x), enc= options.html_enc )
            except:
                prn( '?', x.fname)
                raise

    if options.spisyk_preimenovane or options.prehvyrli_sydyrzhanie:
        rename_all( items, options)
    if options.tags_app:
        tags4mp3_all( items, options)
    if options.izdania_spisyk:
        izd = {}
        def a2list(x):
            return isinstance( x, str) and x.split() or isinstance( x, int) and [ str(x) ] or x
        re_izd = re.compile( '(\D*)(\d*)(.*)')
        neizv = 0
        for az in items:
            if az.vnos: continue
            ii = [ DictAttr(
                    izdanie= az._izdania,
                    godina = az.etiketi.godina or '',
                    ime   = [ az.etiketi.ime ],
                    avtor = az.etiketi.avtor_s_uchastnici or '',
                    vid = az.vid,
                    shapka= 1,
                    fname = az.fname,
                    )]
            if len(az.soundfiles)>1:
                for v in az.soundfiles:
                    if re.search( '(страна|част) *[1-9]$', v.ime): continue
                    appendif( ii[0].ime, v.ime )
                    if v._izdania:
                        ii+= [ DictAttr(
                                izdanie= v._izdania,
                                godina = v.godina or '',
                                ime   = [ v.ime ],
                                avtor = v.avtor_s_uchastnici or '',
                                shapka= 0,
                                fname = v.relname,
                                vid = v.vid or az.vid,
                                )]

            for d in ii:
                xizdanie = d.izdanie
                xgodina  = xizdanie.godina and xizdanie.godina.split() or a2list( d.godina)
                xavtor   = a2list( d.avtor)

                for i in xizdanie:
                    if i.izdatel in (radio, 'avtori.com'): continue
                    m = re_izd.match( i.nomer )
                    assert m, d
                    dd = DictAttr(
                                    prednomer= m.group(1),
                                    bashnomer= m.group(2),
                                    slednomer= m.group(3),
                                    izdatel= i.izdatel,
                                    nomer  = i.nomer,
                                    nositel= i.nositel,
                                )
                    #prn( 3333333, i, dd.nomer, m.groups())
                    if not dd.bashnomer:
                        neizv-=1
                        dd.bashnomer = neizv
                    else:
                        dd.bashnomer = int( dd.bashnomer)
                    di = izd.setdefault( (dd.izdatel, dd.nositel, dd.nomer, dd.bashnomer), dd)
                    di.setdefault( 'godina', set()).update( xgodina)
                    extendif( di.setdefault( 'ime', [] ), d.ime)
                    extendif( di.setdefault( 'avtor', []), xavtor)
                    di.setdefault( 'fname', set()).update( d.fname)
                    di.setdefault( 'vid', set()).update( d.get( 'vid',()))

        r = []
        for i in sorted( izd.values(),
                    key= lambda i: (i.izdatel, i.nositel,
                                        i.bashnomer, i.prednomer, i.slednomer) ):
            for a,v in i.items():
                if a in ('avtor', 'vid'): continue
                if isinstance( v,(tuple,set,list)) and len(v)==1: i[a] = list(v)[0]
            o = dictOrder()
            d = attr2item(o)
            d.izdatel = i.izdatel
            d.nositel = i.nositel
            d.nomer = i.nomer or '?'
            d.bashnomer = ''
            if i.bashnomer>0:
                d.bashnomer = str(i.bashnomer)
                if i.slednomer.startswith(','):
                    d.bashnomer += ','+ d.bashnomer[ : len(d.bashnomer)-len(i.slednomer)+1] + i.slednomer[1:]
            d.ime = i.ime
            d.vid = i.vid and '('+','.join( i.vid)+')' or ''
            d.avtor = i.avtor and ':'+'+'.join( i.avtor) or ''
            d.godina = i.godina or ''

            r += [' '.join( str( l) for l in o.values())]

        save_if_diff( options.izdania_spisyk, r, enc= options.html_enc )


if __name__ == '__main__':
    info.main()

# vim:ts=4:sw=4:expandtab

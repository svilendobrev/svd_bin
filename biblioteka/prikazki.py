#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opisvane
from opisvane import zaglavie, prn, dictOrder, dict_lower, make_dict_attr, make_dict_trans, str2list, fnmatch_list, cyr2lat
from svd_util.lists import appendif, extendif, listif
from svd_util.struct import DictAttr, attr2item
from svd_util import optz
import collections
import subprocess, re, os
from glob import glob
from svd_util.osextra import globescape
from os.path import isdir, basename, exists, join, dirname
import pprint

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

#http://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx#file_and_directory_names
ntfs_forbids = ''.join( a[0] for a in r'''
< (less than)
> (greater than)
: (colon)
" (double quote)
/ (forward slash)
\ (backslash)
| (vertical bar or pipe)
? (question mark)
* (asterisk)
'''.strip().split('\n') )
def fname_filter( f):
    for n in ntfs_forbids:
        f = f.replace( n, '.')
    f = f.strip()
    f = f.rstrip(' .')
    return f

from izdania import *

extra_exts= set( kysi_lat.values())
IKONA = '.ikona.jpg'
MIKONA = '.m'+IKONA
from datetime import datetime, timedelta
sega_fmt = '%y%m%d'
sega_fmt2 = '%Y%m%d'
sega = datetime.today()
def date( a):
    return datetime.strptime( str(a), len(str(a))>6 and sega_fmt2 or sega_fmt)

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

'''
евентуална последователност при всяка папка поотделно:
 - за всяка: прочит на описа, извличане на хората
 - обобщаване на хората
 - за всяка: прочит на описа, обработка, резултати
или
 - за всяка: прочит на описа, извличане на хората, обработка според текущите общи хора, резултати
 - обобщаване на хората ; индекси по хора
   > при разлики -> пускане отново
или със зависимости:
    папка Х зависи от хора А,Б,В
    и обратно, човек А играе в Ч,Ш,Щ
    не е ясно незнайните съкращения как точно се помнят.. като отделни хора ли

'''

class info( opisvane.info):
    @staticmethod
    def opts():
        opisvane.info.opts()
        optz.text( 'debug',   default='', help= 'списък(,) от main,dirs,sizes,times,items2,tags')
        optz.text( 'vreme_app',  type= 'choice', choices= mp3times.apps,
                                    help= 'проверява продължителността с този инструмент')
        optz.bool( 'dveniva',       help= 'търси файлове и в */ (освен в ./)')
        optz.text( 'proizhod_da',   help= 'подпапка за използвани оригинали-от-кого [%default]', default= '0/da.*')
        #optz.text( 'proizhod_ne',   help= 'подпапка за неползвани оригинали-от-кого [%default]', default= '0/ne.*')
        optz.bool( 'prezapis',      help= 'презаписва всички файлове (иначе само ако са различни)')

        gg = optz.grouparg( 'съкращения и участници/дейности')
        optz.text( 'sykr',          help= 'чете файл със съкращения (списъци имена или от грамофонче)', **gg)
        optz.text( 'sykr_spisyk',   help= 'прави файл със съкращения като списък', **gg)
        optz.text( 'sykr_moin',     help= 'прави файл със съкращения за грамофонче', **gg)
        optz.bool( 'sykr2dylgo',    help= 'разписва знайните съкращения', **gg)
        optz.bool( 'opis2dejnosti', help= 'извлича участници/дейности/роли от полето описание', **gg)

        gg = optz.grouparg( 'mp3-етикети на съдържанието')
        optz.text( 'tags_app',  type= 'choice', choices= 'mp3info eyed3'.split(),
                                    help= 'с кой инструмент да се слагат mp3-етикети - ако изобщо', **gg)
        optz.bool( 'tags_direct',   help= 'слага етикетите на място', **gg)
        optz.text( 'tags_enc',      help= 'кодировка на етикетите [%default]', default= 'cp1251', **gg)
        optz.text( 'tags_spisyk',       help= 'прави общ списък за слагане на етикети', **gg)
        optz.text( 'tags_po_papki',     help= 'прави списъци по папки за слагане на етикети', **gg)
        optz.text( 'tags_po_otdelno',   help= 'прави отделни рецепти за слагане на етикети', **gg)

        gg = optz.grouparg( 'преименоване на съдържанието')
        optz.text( 'preimenovane_spisyk',    help= 'прави списък за преименоване на съдържанието', **gg)
        optz.text( 'preimenovane_prehvyrli', help= 'прехвърля/link преименовано съдържанието към тук/', **gg)
        optz.int(  'preimenovane_max', default= 100, help= 'макс.дължина на име [%default] - dvd/udf=255, cd/joliet=64-103..180, extfs=255, win/max_path=256', **gg)
        optz.bool( 'preimenovane_lat',  help= 'преименова на латиница', **gg)
        optz.bool( 'preimenovane_opis', help= 'поправя описи', **gg)

        gg = optz.grouparg( 'html списъци')
        optz.text( 'html_enc',      help= 'кодировка на html [%default]', default='utf8', **gg)  #cp1251
        optz.bool( 'vnosa_e_obiknoven',         help= 'внесените външни папки са като обикновени', **gg)
        optz.bool( 'nakratko_stihove_pesni',    help= 'ет.стихове и ет.песни стават ет.накратко', **gg)
        optz.bool( 'spisyk_samo_papki',         help= 'общия списък само с папки, без връзки към файлове', **gg)
        optz.text( 'url_koren',  default= '/detski/zvuk',    help= 'абс.адрес на общия корен', **gg)

        optz.text( 'html_index',    help= 'прави отделни html-страници по папки', **gg)
        optz.text( 'html_papka',    help= 'прави отделни данни=списък-новости-избор по папки', **gg)
        optz.textfile( 'html_pred',     help= 'файл-заглавка за html-страници', **gg)
        optz.textfile( 'html_sled',     help= 'файл-опашка за html-страници', **gg)

        optz.text( 'html_spisyk',   help= 'прави общ списък html-страница', **gg)
        optz.text( 'html_spisyk_sykr', help= 'съкращава имената на участниците в общия списък', **gg)
        optz.text( 'html_novi',     help= 'прави списък новости отделен (иначе част от общия списък)', **gg)
        optz.text( 'html_izbrani',  help= 'прави списък на само хубавите - извадка от общия списък', **gg)
        optz.text( 'html_novi_vse', help= 'прави списък на всички подредени по новост', **gg)
        optz.text( 'html_hora',     help= 'прави общ списък на хората', **gg)
        optz.text( 'index_hora',    help= 'прави общ списък на хората не-html', **gg)

#       optz.text( 'url_tuk',    default= '',                help= 'отн.адрес тук спрямо корена', **gg)
#       optz.text( 'pyt_tuk',    default= '',                help= 'отн.път   тук спрямо корена', **gg)
#       optz.text( 'pyt_kym_drugvid',    default= '../%(drugvid)s/xxx',  help= 'отн.файлов път към папка-корен от другвид (приказки/песнички/..)', **gg)
#       optz.append( 'samo_vnos',   default=[], help= 'папка-внос от/обработена другаде - показва се само в списъка', **gg)
        optz.bool( 'obshto_otgore',         help= 'слага Общо: отгоре (иначе отдолу)', **gg)
        optz.bool( 'obshto_broi_zapisi',    help= 'брои файловете със записи, а не папките', **gg)
        optz.text( 'podredba',              help= 'подрежда по изброените полета [%default]',
            default= 'humor,ime_sglobeno,pored',
                **gg)
        optz.bool( 'otkoga_e_mintime',      help= 'слага липсващо откога=най-ранното време на папката', **gg)
        optz.int(  'kolko_dni_e_novo',   default=35, help= 'толкова дни нещо се счита за ново [%default]', **gg)
        optz.int(  'kolko_sa_novi',      default=0,  help= 'толкова последни неща се считат за нови [%default]', **gg)
        optz.int(  'novi_prez_dni',      help= 'през толкова дни се слага дата; по подразбиране не се слага', **gg)

        optz.text( 'izdania_spisyk',    help= 'прави общ списък по издания', )
        optz.bool( 'otdeli',            help= 'прави отделни папки с отделните парчета', )
        optz.append( 'ima_etiket',      help= 'включва папки с такъв етикет или имащи елементи с такъв етикет; може няколко', )
        optz.text( 'vkl_etiket',        help= 'включва само папки с такъв етикет', )
        optz.append( 'izkl_etiket',     help= 'изключва папки с такъв етикет', )
        optz.bool( 'khz',               help= 'включва честотни и др. звуко-кодиращи параметри', )


    stoinosti_simvoli = dict(
      преценка = dict(
        #за/от елементите и в папка
        preporyka   = 'преп*оръка препоръчвам',
        izbor       = 'изб*ор',
        #novo        = 'ново',
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
        litdok      = 'лит-док*-композиция литдок',
        litkomp     = 'лит-комп*озиция литкомп',
        dokkomp     = 'док-комп*озиция доккомп',
        humor       = 'хумор',
        stihove     = 'стих*ове стихот*ворение стихотворения',
        dokumentalni= 'документални док*ументално',
        muzikal     = 'мюзикъл мюзикъли',
        portret     = 'портрет',
        otkys       = 'откъс откъси',
        opera       = 'опера',
        #само папката
        otdelni     = 'отделни отделно отделени  самостоятелни', #независими
        #само елементите
        neotdelno   = 'неотделно неотделни несамостоятелно несамостоятелни',
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
        nenakratko  = 'ненакр*атко',             #дори да е само 1, да се описва..
        #само елементите
        nakratko_bez_otdelni_avtori = 'накратко-без-автори',   #в списъка - без отделни автори
        nakratko_bez_sydyrzhanie    = 'накратко-без-съдържание без-съдържание',   #в списъка - без съдържания
        nakratko_bez_uchastnici     = 'накратко-без-уч*астници',   #в списъка - без отделни участници
        avtor_sled_opisanie = 'автор-след-опис*ание автор-в-опис*ание',  #в index - отделните автори не са към имената, а след описанието
        vid_v_opisanie = 'вид-след-опис*ание вид-в-опис*ание',
        #на папката/елемента
        izp_v_avtor = 'изпълнители-в-автор изп-в-автор',
        izp_ne_v_avtor = 'изпълнители-не-в-автор изп-не-в-автор',
        izp_v_avtor_nenasledeni = 'изпълнители-в-автор-ненаследени изп-в-автор-ненасл*едени',
        uch_v_avtor = 'участници-в-автор уч-в-автор',
        mt_v_avtor  = 'м-т-в-автор мт-в-автор музика-текст-в-автор',
        prev_v_avtor    = 'превод-в-автор прев-в-автор пр-в-автор',
        prev_ne_v_avtor = 'превод-не-в-автор прев-не-в-автор пр-не-в-автор',
        rez_v_avtor     = 'режисьор-в-автор реж-в-автор',
        godina_v_ime    = 'година-в-име год-в-име',
        ),
    )
    stoinosti_danni = dict(
        ##поредица
        ##организатор/инициатор/постановка/запис
        #на папката/елемента
        ime_kyso    = 'име-късо',
        opisanie2   = 'описание2 опис2',
        vryzki      = 'опис.връзки опис-връзки вр*ъзки връзка url wr*yzki wryzka',
        nagradi     = 'опис.награди опис-награди наград*а награди nagrad*a nagradi',
        fon         = 'опис.фон    опис-фон    фон',
        poredica    = 'опис.поредица опис-поредица поредица',
        povreda     = 'повреда',    #към описанието
        obrabotka   = 'обр*аботка',
        otkoga      = 'откога',
        bez_otkoga  = 'без-откога', #елементите които нямат откога
        otkyde      = 'откъде',
        srez        = 'срез срез*ове',
        #за/от елементите и в папка
        uchastnici  = 'уч*астници участв*ат',
        izdanie     = 'изд*ания издание',
        proizhod    = 'произход',
        proizhod2   = 'произход2',
        kachestvo   = 'кач*ество качество-съдържание/запис кач-во quality q',
        vid         = 'вид wid',    #полу-изчислимо
        #само папката
        ikoni       = 'ик*они икона',
        pored       = 'поред',  #ако има няколко едноименни папки, напр. Андерсенови приказки
        avtor       = 'ав*тор автори awt*ori',
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

    stoinosti_edinstveno = dict(
        стихове = 'стих',   #отворение
        песни   = 'песен',
    )

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

    def opravi_vid( az, etiketi):
        _vidove = az.stoinosti.portret, az.stoinosti.glas1, az.stoinosti.teatyr
        if 0*'към вид':
            vid = etiketi.vid or []
            if vid:
                vid = isinstance( vid,str) and vid.split() or list( vid)
            for a in _vidove:
                if etiketi.pop( a,None):
                    appendif( vid, a)
        else:   #към етикети
            vid = etiketi.vid
            if not vid: return
            vid = isinstance( vid,str) and vid.split() or list( vid)
            for a in _vidove:
                try:
                    vid.remove( a)
                    az._slaga_etiket( a, True, etiketi)
                except ValueError: pass
        az._slaga_etiket( 'vid', ' '.join( vid), etiketi)

    def opravi_otkoga( az, etiketi, fname, predv_otkoga =None, lipsva_otkoga =False):
        eotkoga = str( etiketi.otkoga).split()
        vse_eotkoga = list( eotkoga)
        otkoga_e_mintime = az.options.otkoga_e_mintime
        if not vse_eotkoga and not otkoga_e_mintime and predv_otkoga:
            appendif( vse_eotkoga, predv_otkoga.strftime( sega_fmt2))

        try:
            eotkoga.remove('+')
            novo = True
        except: novo = False

        if novo or not vse_eotkoga:
            otkoga = sega
            if otkoga_e_mintime:
                t = min( getattr( os.path, f)( fname ) for f in 'getmtime getctime getatime'.split() )
                otkoga = datetime.fromtimestamp( t)
            lipsva_otkoga = True
        else:
            otkoga = max( date( a) for a in vse_eotkoga )

        if lipsva_otkoga:
            o = otkoga.strftime( sega_fmt2)
            if not eotkoga:
                o = int(o)
            else:
                o = ' '.join( listif( eotkoga + [ o]))
            etiketi.otkoga = o

        return otkoga

    @staticmethod
    def fix_urls( etiketi):
        return
        for o in 'opisanie opisanie2'.split():
            if etiketi[o]:
                etiketi[o] = re_url.sub( r'\1[ \2 == \3 ]url', etiketi[o])

    def _samopopylva_etiketi( az):
        d = razglobi( az.ime)
        dime = d.pop( 'ime', '')
        if dime != az.ime:
            az.etiketi.ime = dime

        dvid = d.pop( 'vid', ())
        assert not d
        #assert not d.get('izdanie')
        #assert not d.get('kachestvo')
        #assert not d.get('avtor')

        for v in dvid:
            az.slaga_etiket( v, True)

        az.opravi_vid( az.etiketi)

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

        az._otkoga = az.opravi_otkoga( az.etiketi, az.fname)

        az.orgs_files = proizhod( az.fname, az.options.proizhod_da)
        orgs_meta1 = set( az.etiketi.proizhod.split())
        if az.orgs_files and orgs_meta1 != az.orgs_files:
            az.etiketi.proizhod = ' '.join( sorted( az.orgs_files))

        az.ikoni_vse = sorted( [ basename( i) for i in glob( globescape( az.fname)+'/*'+MIKONA )])
        if not az.etiketi.ikoni and len(az.ikoni_vse)==1:
            az.etiketi.ikoni = az.ikoni_vse[0].replace( MIKONA, '.jpg')

        for o in 'opisanie opisanie2'.split():
            opis,lipsva = lipsva_izvadi( str(getattr( az.etiketi, o) or ''))
            if lipsva:
                az.slaga_etiket( o, opis)
                az.slaga_etiket( 'povreda', lipsva, zamesti= False)

        az.fix_urls( az.etiketi)

        az.opravi_avtori( az.etiketi)

        ss = str2list( az.etiketi.obrabotka)
        if ss: az.etiketi.obrabotka = ss

        az.setup_prevodi()
        az.setup_elementi()
        az.setup_prevodi2()

        az.opis2hora2dejnosti()

        ime = az.ime.lower()
        if ime.lower() == 'стихове': az.etiketi.stihove = True
        #if az.etiketi.stihove:
        #    az.etiketi_element.izp_v_avtor = True
        #    #az.etiketi_element.prev_v_avtor = True
        #    del az.etiketi.izp_v_avtor
        if 'хумор' in ime: az.etiketi.humor = True
        if len(az.soundfiles)<=1:
            for k in 'prefixime prefixavtor prefixnomer'.split():
                if az.etiketi.get(k): prn( '??', az.stoinosti0[ k], az.fname)

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
                assert not r, (e.uchastnici, e)
            elif e.uchastnici:
                def slepiImena( x): return x.replace(' ','')
                def nelepiImena( x): return x

                for dd,v in e.uchastnici.items():
                    if not v: continue
                    #XXX не работи добре за разни оркестри и пр.... затова nelepiImena
                    if isinstance( v, dict): #Aa Bb: rrr ; CcDd: rr
                        vv = [ dict( (nelepiImena(h),r) for h,r in v.items()) ]
                    elif isinstance( v, str):
                        if ',' in v:    #Aa Bb, Cc Dd
                            vv = [ slepiImena( h.strip()) for h in v.split(',') ]
                        else:   #AaBb CcDd
                            vv = v.split()
                    else: #list #Aa Bb ; CcDd ;
                        #vv = list(v)
                        vv = [ dict( (nelepiImena(h),r) for h,r in i.items())
                                if isinstance(i, dict)
                                else nelepiImena( i)
                               for i in v
                             ]

                    #vv = isinstance( v, dict) and [ v ] or ( v.split() if isinstance( v, str) else list(v) )
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
                    if az.options.sykr2dylgo:
                        h = abbr.dai_imepylno( h) or h
                        hh.append( dejnosti2hora.hr2h( h,r))
                    abbr.dobavi( h, e.ime)
                if hh: hora[:] = hh

            if az.options2( 'avtor2dejnosti') and e.avtor:
                dejnost_podrazbirane = None
                if etiket( e, 'pesen') or etiket( e, 'stihove'):
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

            #от съдържание
            uchastnici_syd = az.make_Uchastnici()
            l_uchastnici_syd = []
            dejnost_podrazbirane = 'автор'
            for s in e.sydyrzhanie or ():
                u = None
                if s:
                    r = razglobi( s)
                    if not r.get('avtor'): u = None
                    else:
                        u = az.make_Uchastnici()
                        for a in r.avtor:
                            opis = u.opis2dejnosti( a, e, u.posledna_dejnost or dejnost_podrazbirane)
                        az.uchastnici_vse.dobavi( u, bezplus= True)
                l_uchastnici_syd.append( u)
            az.uchastnici_vse.dobavi( uchastnici_syd, bezplus= True)
            if l_uchastnici_syd:
                #if e is not az.etiketi:
                e._uchastnici_syd = l_uchastnici_syd
                #else: az._uchastnici_syd = l_uchastnici_syd

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
                vse.dobavi( uchastnici_syd, bezplus= True )    #copy
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

        posledna_dejnost = None
        def slaga_dejnost( az, dejnost, hora, bezplus =False):
            az.posledna_dejnost = dejnost
            if not hora: return
            dai_imepylno = az.abbr.dai_imepylno
            for d in isinstance( dejnost, str) and [dejnost] or dejnost:
                i = az.setdefault( d, [])
                for h in hora:
                    if bezplus and h == '+': continue
                    h,r = az.h2hr( h)
                    h = dai_imepylno( h) or h
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
                posledna_dejnost = None
                r.append( [] )
                kalpak = None
                bb = b.split()
                while bb:
                    aa = bb.pop(0)
                    pred_kalpak = kalpak
                    a = aa.rstrip(',.')
                    kalpak = abbr.dai_kalpak( a)
                    #prn( 88999999999, a, kalpak, bb)
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
                                rol = bb.pop(0).strip('.,')
                                rolia.append( rol)
                                if rol[-1]==')': break
                                #if rolia[-1][-1]==')': break
                            rolia = ' '.join( rolia ).strip( '()' )
                    if info.options.sykr2dylgo:
                        kalpak = abbr.dai_imepylno( kalpak) or kalpak
                    #prn( 788999999999, kalpak, bb)
                    hora = abbr.dobavi( kalpak, element.ime)
                    if rolia: hora = [ { h:rolia } for h in hora ]  #TODO io only!
                    for d in abbr.dai_dejnosti( a, posledna_dejnost or dejnost_podrazbirane):
                        az.slaga_dejnost( d, hora)
                        posledna_dejnost = az.posledna_dejnost

            opis = joinif( '; ', [' '.join(a) for a in r if a] )
            return opis



    @classmethod
    def bez_ext1x1( az, fname, exts= ()):
        return super().bez_ext1x1( fname, exts, extra_exts)

    def setup_prevodi( az):
        for p in az.prevodi.values():
            ime = p.ime
            razglobeni = razglobi( ime)
            if razglobeni.get('ime') == ime: del razglobeni['ime']  #?
            for k in razglobeni.pop( 'vid', ()):
                az._slaga_etiket( k, True, p.etiketi)
            p.update_pre( **razglobeni)
            az.opravi_avtori( p)
            az.opravi_vid( p.etiketi)

            p._izdania = az.opravi_izdania( p)

            if not p.etiketi.neotdelno and not az.etiketi.neotdelno and az.etiketi.avtor and p.avtor and not set(p.avtor).issubset( set( az.etiketi.avtor)) :
                az.etiketi.otdelni = True

            az.fix_urls( p)

    def setup_prevodi2( az):
        lipsva_otkoga = len( az.prevodi) == sum( not p.otkoga for p in az.prevodi.values())
        for p in az.prevodi.values():
            fname = p.get( '_fname')
            if fname:
                p._otkoga = otkoga = az.opravi_otkoga( p, join( az.fname, fname),
                                az.etiketi.bez_otkoga and date( az.etiketi.bez_otkoga )
                                    or (not az.etiketi.otdelni or lipsva_otkoga) and az._otkoga,
                                lipsva_otkoga= lipsva_otkoga
                                )
                if az._otkoga < otkoga: az._otkoga = otkoga

    class SoundElement( DictAttr):
        _other = None
        _others = 'uchastnici uchastnici_vse sydyrzhanie opisanie2 otkyde vryzki nagradi povreda etiketi _izdania'.split()

        def __getitem__( az, k):
            try:
                return DictAttr.__getitem__( az, k)
            except:
                if az._other is not None:
                    return az._other.get(k)
                raise
        def __getattr__( az, k):
            try: return az[k]
            except KeyError: raise AttributeError(k)
        #__getattr__ = __getitem___
        def get( az, k, *default):
            if k in az: return DictAttr.__getitem__( az, k)
            if az._other is None: return DictAttr.get( az, k, *default)
            return az._other.get( k, *default)
        def items( az):
            for k,v in DictAttr.items( az): yield k,v
            if az._other is not None:
                for k,v in az._other.items(): yield k,v

    def setup_elementi( az):
        #елементи
        az.soundfiles = [ az.SoundElement( fname=f) for f in soundfiles( az.fname, az.options) ]
        if not az.soundfiles:
            if az.etiketi.papka: return
            prn( '!empty', az.fname)

        for v in az.soundfiles:
            #при 1 ниво bname == name
            v.bname = basename( v.fname)
            v.name = v.fname[ 1+len( az.fname.rstrip('/')):]

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
                v._prevod = p

                #и понеже преводът с :автор може да е скапан с .mp3 в prevedi_elementi..
                v.ime = pnm and az.bez_ext( pnm, extra_exts=extra_exts)
                if not v.ime or v.ime == nm:
                    v.ime = nm
                    if re.search( nm, '[a-zA-Z]') or az.options.podrobno:
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
                bez = [] #['ime']
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
                if 1:
                    v._other = p
                else:
                    for k in SoundElement._others:
                        u = p.get( k)
                        #if u:
                        v[k]=u
                #TODO a tezi?
                v.ime_bez_grupa = bez_pfx( v.ime, grupa_kysa, zaglavie( grupa_kysa) ).strip()
                v.ime_bez_grupa_i_nomer = re.sub( '^\d+\.', '', v.ime_bez_grupa).strip()
                p._fname = v.name

    def setup( az):
        rfname = az.origfname
        rvse_prefix = info.vse_prefix_orig
        az.rname = rfname[ len( rvse_prefix):].strip('/')

        fniva = az.fname.split('/')
        az.vnos = False

        for d in az.options.dirs:
            if az.fname.startswith( d.rstrip('/')+'/'):
                az.rname = az.fname[ len(d)+1:]
                break
        else:
            az.vnos = not az.options.vnosa_e_obiknoven
        if az.vnos:
            if az.options.podrobno: prn( 'vnos', az.fname)

        for v in az.soundfiles:
            v.relname = join( az.rname, v.name)
            if v.ime == '-/-': v.ime = az.ime

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

        az.absurl = join( az.options.url_koren, az.tip.url, *rurl)  #path from root

        az.ikoni = [ i.replace( '.jpg', IKONA) for i in az.etiketi.ikoni.split() if 'jpg' in i]
        az.kartinki = [ i.replace( MIKONA, '.jpg') for i in az.ikoni_vse ]

        orgs_files = az.orgs_files
        orgs_meta1 = set( az.etiketi.proizhod.split())
        orgs_meta2 = set( az.etiketi.proizhod2.split())
        az.orgs = ( (orgs_meta1 | orgs_files ) or { 'svd' } ) | orgs_meta2
        str_orgs = sorted( info.meta_prevodi.get( s, s) for s in az.orgs )
        az.vse_str_orgs.update( str_orgs)
        az.str_orgs = ' '.join( str_orgs)

        def vid4ime( ime, **k):
            vidi = [ az.znak( 'otkys', **k)   and az.stoinosti.otkys, ]
            for a in [
                az.znak( 'muzikal', **k) and az.stoinosti.muzikal,
                #az.znak( 'pesen', **k)   and az.stoinosti_edinstveno[ az.stoinosti.pesen ],
                #az.znak( 'stihove', **k) and 'стихо' not in ime and az.stoinosti.stihove,
                az.znak( 'glas1', **k)   and az.stoinosti.glas1,
                ]:
                    if a:
                        vidi.append( a)
                        break

            return [ a for a in vidi if a]
        az.vid4ime = vid4ime( az.ime)


        #подредба
        if len( az.soundfiles) > 1:
            podredba = az.options.sort_prevodi or az.etiketi.sort_prevodi
            if podredba:
                if isinstance( podredba, bool):
                    def key(v): return v.ime
                else:
                    if isinstance( podredba, str): podredba = podredba.split()
                    def key(v): return tuple( str(v.get( k,'')) for k in podredba)
                az.soundfiles.sort( key= key)
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

        az.avtori2vse( az.etiketi, az.etiketi.uchastnici, az.etiketi.avtor)

        for v in az.soundfiles:
            i = v._izdania or az._izdania
            v.izdanie_kyso_zapis = izdatel_kys( i and i[0].izdatel or '')
            v.nositel = koi_nositel4fname( v.name, nositel, v.izdanie_kyso_zapis)
            v.vid4ime = vid4ime( etiketi= v.get( 'etiketi'), za_elementi=True, ime= v.ime)
            uchastnici_vse = v.get( 'uchastnici_vse')
            az.avtori2vse( v, uchastnici_vse, za_elementi=True)
            extendif( izdania, v._izdania )
            v._godina = listif( i.godina for i in v._izdania or () if i.godina)
            if v._godina: v._godina = min( v._godina)

            v.e_radio = ( radio in v.nositel )
            v.e_teatyr, v.vid = az.vidove( v.get( 'etiketi'), v.get( 'vid'), uchastnici_vse, v.e_radio)

            n+=1
            v.nomer = v.nomer_str = None
            if len( az.soundfiles)!=1 and az.etiketi.nomer or az.etiketi.nomer0 or az.etiketi.prefixnomer:
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

        az.v_zaglavieto = [
            eteatyr and ( radio in az.izdateli and 'радиотеатър' or 'театър' ), #/драматизация
            az.etiketi.dokumentalni and 'док.',
            az.etiketi.litdok   and 'лит-док-комп.',
            az.etiketi.dokkomp  and 'док-комп.',
            az.etiketi.litkomp  and 'лит-комп.',
            az.etiketi.portret  and az.stoinosti.portret not in az.ime.lower() and az.stoinosti.portret,
            az.etiketi.stihove  and 'стихо' not in az.ime.lower() and az.stoinosti.stihove,
            az.etiketi.glas1    and az.stoinosti.glas1,
        ]
        if not (eteatyr and radio in az.izdateli):
            az.v_zaglavieto += az.izdateli
        #az.v_zaglavieto += [ i.nomer for i in az._izdania]
        az.v_zaglavieto = [ a for a in az.v_zaglavieto if a ]

    def vidove( az, etiketi, vid ='', uchastnici_vse =(), eradio =False):
        eteatyr = ( etiketi and etiketi.teatyr
                    or uchastnici_vse and bool(
                          uchastnici_vse.get( 'драматизация')
                       or uchastnici_vse.get( 'адаптация')
                       or uchastnici_vse.get( 'режисьор')
                       #or (len( az.soundfiles)==1  or not eradio) and len( uchastnici_vse.get( 'изпълнение',()))>1
                       ))

        #TODO множ.число/род
        vid = vid and isinstance( vid, str) and vid.split() or list( vid or ())
        extendif( vid, etiketi and sorted( v for v in [
                etiketi.dokumentalni and az.stoinosti.dokumentalni,
                etiketi.stihove      and az.stoinosti.stihove,
                etiketi.pesen        and az.stoinosti.pesen,
                etiketi.glas1        and az.stoinosti.glas1,
                etiketi.humor        and az.stoinosti.humor,
                etiketi.muzikal      and az.stoinosti.muzikal,
                etiketi.portret      and az.stoinosti.portret,
                etiketi.litdok  and 'литературно-документална композиция',
                etiketi.litkomp and 'литературна композиция',
                etiketi.dokkomp and 'документална композиция',
            ] if v) or ()
            )
        if eteatyr:
            if not vid:
                vid = [ eradio and 'радиотеатър/драматизация' or 'театър/драматизация']
            elif vid != [ az.stoinosti.dokumentalni ] or not (etiketi and etiketi.teatyr):
                eteatyr = False
        return eteatyr, vid

    class Prevod( opisvane.info.Prevod):
        _vytr_svoistva = opisvane.info.Prevod._vytr_svoistva + '''
            _izdania _fname _otkoga
            ime_bez_grupa_i_nomer ime_bez_grupa vid4ime
            '''.split()
        _izdania = ()


    @classmethod
    def all( klas):
        vse( sorted( (x for x in klas.vse.values() if not x.etiketi.koren), key= lambda x: x.ime), klas.options)
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
        bb = dictOrder()
        bb[ 'avtor1' ] = v.avtor1 or ()
        bb[ 'avtor'  ] = v.avtor or avtor

        aa = []
        aabezizp = []
        vetiketi = v.get( 'etiketi')
        def znak( t): return az.znak( t, vetiketi, za_elementi)
        if za_elementi and not uchastnici_vse: uchastnici_vse = az.etiketi.uchastnici   #наследи
        if uchastnici_vse:    #ред: текст, музика, изпълнение, всички други
            c = []
            def dejnost( d): appendif( c, d)
            z = DictAttr( (k, znak(k)) for k in '''
                    uch_v_avtor     rez_v_avtor     mt_v_avtor
                    izp_v_avtor     izp_ne_v_avtor  izp_v_avtor_nenasledeni
                    prev_v_avtor    prev_ne_v_avtor
                    pesen   muzikal     stihove
                    '''.split())
            izpylniteli = uchastnici_vse.get( 'изпълнение') or ()
            stih_pesen = z.stihove or z.pesen
            izp = z.izp_v_avtor or z.uch_v_avtor or (za_elementi or len( izpylniteli)<=2) and stih_pesen
            if za_elementi and z.izp_v_avtor_nenasledeni:
                izp = bool( v.get( 'uchastnici', {}).get( 'изпълнение'))
            if z.izp_ne_v_avtor: izp = False
            if izp and stih_pesen: dejnost( 'изпълнение')
            if not stih_pesen and (1 or z.rez_v_avtor) or z.uch_v_avtor: dejnost( 'режисьор')
            if za_elementi and z.pesen or (z.muzikal and (not az.etiketi.otdelni or za_elementi)) or z.mt_v_avtor or z.uch_v_avtor:
                mt = 'либрето текст'.split()
                if not z.prev_ne_v_avtor: mt.append( 'превод')
                m = 'музика'.split()
                if z.muzikal or z.pesen: mt = m+mt
                else:    mt = mt+m
                for d in mt: dejnost( d)
            if not z.prev_ne_v_avtor:
                if z.stihove or z.prev_v_avtor or z.uch_v_avtor: dejnost( 'превод')
            if izp: dejnost( 'изпълнение')
            #if 'kuk' in az.fname or z.pesen: prn( 11111111, v.ime, c, z, uchastnici_vse)


            for a in c:
                ii = uchastnici_vse.get( a)
                if not ii:
                    ii = az.etiketi.uchastnici and az.etiketi.uchastnici.get( a)
                    if not ii:
                        continue
                if 0*a=='изпълнение':
                    if not (z.uch_v_avtor or z.izp_v_avtor):
                        if len(ii)>2:
                            continue    #не повече от 2 изпълнителя
                    else:
                        extendif( aabezizp, ii)
                #extendif( aa, ii)
                bb[a] = ii
            if z.uch_v_avtor:
                for k,u in uchastnici_vse.items():
                    extendif( bb.setdefault( k, []), u)
                    #extendif( aa, u)
                    #extendif( aabezizp, u)

        for k,hh in bb.items():
            bb[k] = [ az.Uchastnici.h2hr(h)[0] for h in hh ]
        v.avtor_s_uchastnici = bb

    def sykrati_avtori( az, aa):
        #dai_kyso = az.abbr.dai_kyso
        #rr = [ dai_kyso( h, original= False) or h for h in aa]
        rr = aa
        r = ','.join( rr)
        r = r.replace( ':,', '') #dejnost
        return r

    def avtor_s_uchastnici( az, element =None, **ka):
        if element is None:
            avtor_s_uchastnici = 0 and az.etiketi.otdelni and dict( avtor= az.etiketi.avtor) or az.etiketi.avtor_s_uchastnici
        else:
            avtor_s_uchastnici = element.avtor_s_uchastnici
        return az._avtor_s_uchastnici( avtor_s_uchastnici, **ka)
    @staticmethod
    def _avtor_s_uchastnici( avtor_s_uchastnici, samo_imena =True, sykr_dejnost =True, edno =False,
            bez_roli =True,
            sykr_avtori =False, sykr_neavtori =False, sykr_vse =False, razdeli_avtor =False ):
        if not avtor_s_uchastnici: return ''

        _dai_kyso = info.abbr.dai_kyso
        def dai( h, sykr):
            h0 = h
            if isinstance( h, dict):
                assert len(h)==1
                k,v = list( h.items())[0]
                if sykr or sykr_vse:
                    k = _dai_kyso( k, original= False) or k
                if razdeli_avtor: k = razdeli_kamila2( k )
                if bez_roli: h = k
                else: h = k + ' ('+ v +')'
                #prn(5555555, repr(k),repr(v), h0)
            else:
                if sykr or sykr_vse:
                    h = _dai_kyso( h, original= False) or h
                    if razdeli_avtor: h = razdeli_kamila2( h )
            return h
        def rhh( hh, sykr):
            return [ dai( h, sykr) for h in hh ]

        r = []
        r0= []
        for d,hh in avtor_s_uchastnici.items():
            if not hh: continue
            h0 = hh
            if d in ('avtor1', 'avtor', 'автор'):
                if edno:
                    if d != 'avtor1': continue
                else:
                    if d == 'avtor1': continue
                #if d != (edno and 'avtor1' or 'avtor'): continue
                hh = rhh( hh, sykr_avtori)
            else:
                hh = h0 = [ h for h in hh
                            if h not in r0 or d not in (info.abbr.dejnost_podrazbirane, 'музика', 'текст', 'либрето', 'режисьор') ]
                if not hh: continue
                hh = rhh( hh, sykr_neavtori)
                #XXX горното не е 100% вярно..
                if not samo_imena:
                   r.append( (sykr_dejnost and dejnost2sykr( d) or d) + ':')
            r += hh
            r0 += h0

        if 0 and razdeli_avtor:
            r = [ razdeli_kamila2(a) for a in r]
        if 0:   #изп и прев и муз, или изп и автор.. може. но автор и прев - не..
            broi = collections.Counter( r)
            for c in broi.values():
                if c > 1:
                    prn( '????', r, c)
                    break
        return r

def kachestva( k, as_dict =False, default ='?'):
    if k and '/' in k:
        qcontent,qrecord = k.split('/')
    else:
        qcontent = qrecord = k or ''
    qcontent = qcontent.strip() or default
    qrecord  = qrecord.strip() or default
    if as_dict: return dict( qcontent= qcontent, qrecord= qrecord)
    return qcontent, qrecord

def save_if_diff( *a,**ka):
    options = ka.pop( 'options', info.options)
    return opisvane.save_if_diff(
        naistina= options.davai,
        podrobno= not options.davai,
        prezapis= options.prezapis,
        *a,**ka)

def etiket( y, k):
    if get_attrib( y, k, False, error= (AttributeError,KeyError) ): return True
    if get_attrib( y, 'etiketi.'+k, False, error= (AttributeError,KeyError) ): return True


def anea( a, t, sep=''): return t and sep.join( ['<'+a+'>',t,'</'+a+'>'])
def bold( t, **k):  return anea( 'b', t, **k)
def ital( t, **k):  return anea( 'i', t, **k)
def h4( t, sep=' '): return anea( 'h4', t, sep)
def h1( t, sep=' '): return anea( 'h1', t, sep)
def blockquote( t, sep= '\n'): return anea( 'blockquote', t, sep)
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

def sglobi( ime, avtor='', vid ='', izdanie ='', godina='', nomer =None, html= True, razdeli_avtor =True):
    ime = zaglavie( ime)
    r = ime
    if vid:
        if isinstance( vid, str): vid = vid.split()
        for i in vid:
            if i.lower() in r.lower(): continue
            #assert i not in r, i
            r += ' -'+ i
    if avtor:
        if isinstance( avtor, str): avtor = [ avtor ]
        j = ','
        if razdeli_avtor:
            avtor = [ razdeli_kamila2(
                info.abbr.dai_imepylno( a) or a
                ) for a in avtor]
            j = ', '
        avtor = j.join( avtor)
        avtor = avtor.replace( ':'+j,' ') #dejnost
        avtor = avtor.replace( '  ',' ')
        if avtor.lower() != ime.lower():
            if html: avtor = ital( avtor)
            if razdeli_avtor:
                r += ' ('+ avtor + ')'
            else:
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
    '(?P<kachestvo>[*~?+-]/[~?+-])$',
    '-(?P<vid>песен|песни(чки)?|мюзикъли?|откъси?)$',
    '/(?P<godina>\d+\??)$',  #(-\d+\??)?
    '/(?P<izdanie>\S+)$',
    #':(?P<avtor>\S+)',
    r':(?P<avtor>\S[^/]+)', #без $ в края, може (
    ]) +')', re.IGNORECASE)

def razglobi( ime ):
    #ime -vid :avtor [extra]/izdanie /godina; opisanie +
    d = DictAttr()
    ime = ime.strip()
    if ime.endswith('+'):
        d.otkoga = '+'
        ime = ime[:-1].rstrip()
    if ';' in ime:
        ime,d.opisanie = (a.strip() for a in ime.split( ';', 1))

    while 1:
        m = re_all.search( ime)
        if not m: break
        for k,v in m.groupdict().items():
            if v: v = v.strip()
            if not v: continue
            #if k == 'avtor':
            d.setdefault( k, []).insert( 0, v )
        ime = ime[0:m.start()] + ' ' + ime[ m.end():]
        ime = ime.strip()
        ime = ime.replace( '  ',' ')

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

def sydyrzhanie2imena( y):
    for a,u in zip( y.sydyrzhanie or (), y.get('_uchastnici_syd') or () ):
        if not a: yield a
        else:
            kk = razglobi( a)
            if kk.get('avtor'):
                x = info._avtor_s_uchastnici( u, samo_imena= False, bez_roli =False )
                kk['avtor'] = x
            yield sglobi( html= False, **kk)

##############

def soundfiles( fn, options ):
    gfn = globescape( fn)
    soundfiles = glob( gfn+'/*.mp3') #+ glob( fn+'/*.wma')
    if options.dveniva:
        innerfiles = glob( gfn+'/*/*.mp3') #+ glob( fn+'/*/*.wma')

        soundfiles += [ i for i in innerfiles
                        if not fnmatch_list( i[len(fn):].lstrip('/').split('/')[0], options.bez) ]
    return sorted( soundfiles)

def proizhod( fn, proizhod_dir):
    return set( basename( d).split('.',1)[-1]
            for d in glob( join( globescape( fn), proizhod_dir))
            if d.rsplit('.',1)[-1] not in info.exts
            )

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
    return re.sub( r'</?[a-z]+>', '', r).rstrip('/ ')

def dejnost2sykr( d):
    g = info.abbr.dejnosti2sykr.get( d)
    return g and g+'.' or d

def html4uchastnici( uchastnici, sykr =False, bez_dejnosti =(), samo_dejnosti =(), bez_roli =False ):
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


    def grupira_dejnosti( d, horа):
        #групиране м.+т.
        if len(hora) !=1: return
        xd = hd.get( hora[0])
        if not xd: return True  #вече изядено
        if len( xd)<2: return
        for x in xd:
            if x == d: continue
            if len( dh.get(x) ) >1: return  #групирана в д:х+х
        del hd[ hora[0] ]
        return '+'.join( dejnost2sykr( x) for x in xd)

    for d,hora in dh.items():
        podrazb = (d == abbr.dejnost_podrazbirane)
        if sykr:
            d0 = d
            d = dejnost2sykr( d)

            #групиране м.+т.
            if not podrazb:
                rd = grupira_dejnosti( d0, hora)
                if rd is True: continue  #вече изядено
                if rd: d = rd

        drugi = None
        hh = []
        for h in hora:
            h,rolia = uchastnici.h2hr( h)
            h0=h
            if sykr:
                h = abbr.dai_kyso( h, original= False, min= False) or h
                if '.' not in h: h = razdeli_kamila2( h)
            else:
                h = abbr.dai_imepylno( h) or h
                h = razdeli_kamila2( h)
                if rolia and not bez_roli: h += ' ('+ rolia +')'
            if 'други' in (abbr.imena.get( h0) or ()):
                drugi = h
            else:
                appendif( hh, h)
        if drugi:
            appendif( hh, drugi)
        hh = ( sykr and (not podrazb and '+' or ', ') or ', ' ).join( hh)
        r.append( (d, hh) )

    if sykr:
        r = '; '.join( d+' '+hh for d,hh in r )
    else:
        r = ' ' + '<br>\n '.join( d+': '+hh for d,hh in r )
    return blockquote( r)


def href( url, ime):
    return '<a href="%(url)s"> %(ime)s</a>' % locals()

re_url = re.compile( r'(url|papka|file)\[ *(\S+?)(?:==| +==*) *(.*?) *\]url'.replace(' ',r'\s') )
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
                if (file_exists( $_SERVER['DOCUMENT_ROOT'] . $i)) echo "<img src=\\"$i\\" height=48>";
                ?>''' % locals()
    return href( url,ime)
def url( x):
    return re_url.sub( repl, x)

def html4opisanie( d):
    if not d: return d
    return blockquote( url( d.replace( '%', '%%')).replace( '\n', '\n <br> ' ))

def otkyde( o):
    if o: o = '(%s)' % ' '.join( info.meta_prevodi.get(x,x) for x in str(o).split())
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
    opisanie12  = joinif( '\n', [ opisanie, x.etiketi.opisanie2,
        #otkyde( x.etiketi.otkyde)
        ])
    eotkyde      = otkyde( x.etiketi.otkyde)
    sydyrzhanie = '\n'.join( a for a in sydyrzhanie2imena( x.etiketi) )

    izdanie = x.etiketi.izdanie
    nositel = x.nositel

    for a in '''
            url2papka
            q size time org
            opisanie opisanie12 sydyrzhanie eotkyde
            nositel
            izdanie kachestvo preporyka izbor prepizbor
            '''.split():    #avtor ime
        x.html[a] = locals()[a]
    return x.html

def html4koloni( redove):
    if not redove: return ''
    nm = len(redove)
    nkoloni = 2
    if 0*'цели елементи':
        nm2 = (nm+1)//2
        if nm2<2: nkoloni = 1
        else:
            for n in nm2, nm2-1, nm2+1, nm2-2, nm2+2:
                if n< nm and redove[n].startswith('<h4>'):  #HACK
                    nm2 = n
                    break
    else:   #редове в елементи
        if nm<=3: nkoloni = 1
        else:
            ll = [ len( [ i for i in e.split('<br>') if i.strip() ]) for e in redove ]
            lkolona = (sum( ll) + nkoloni-1)//nkoloni
            nm2 = 0
            for l in ll:
                nm2 += 1
                lkolona -= l
                if lkolona<=0: break

    if nkoloni>1:
        r = divl( redove[ :nm2], 'kolona1')
        r+= divl( redove[ nm2:], 'kolona2')
    else:
        r = divl( redove, 'kolona0')

    return DictAttr( html= '\n'.join( ['<br>'] + r), nkoloni= nkoloni)


def html4zapisi( x, imeavtor, sykr =False,
        bez_avtor =False,
        avtor_sled_opisanie= False,
        uchastnici      =True,
        uchastnici_vse  =False,
        uchastnici_sykr =False,
        uchastnici_bez_roli= False,
        sydyrzhanie= True,
        vryzki  =True,
        nagradi =True,
        opis2   =True,
        godina  =True,
        izdanie =True,
        vid_v_opisanie =None,
        elementi_bez_vryzki =False,
        vid_v_opisanie_sykr =False,
        izdanie_v_ime =False,
        samo_dejnosti =(),
        eotkyde = True,
        vremena = None,
        ):

    if sykr:
        #bez_avtor = x.etiketi.nakratko_bez_otdelni_avtori
        avtor_sled_opisanie =False
        #uchastnici      =False
        uchastnici_vse  =False
        uchastnici_sykr =False
        #sydyrzhanie =False
        vryzki  =False
        nagradi =False
        opis2   =False
        #godina  =False
        #izdanie =False
        #vid_v_opisanie_sykr =True
        eotkyde = False
        soundfiles = [ y for y in x.soundfiles if not etiket( y, 'neotdelno' ) ]
    else:
        soundfiles = x.soundfiles
        #avtor_sled_opisanie= x.etiketi.avtor_sled_opisanie

    if vid_v_opisanie is None:
        vid_v_opisanie = x.znak( 'vid_v_opisanie', za_elementi=True)

    tx_mode = {
        'mono': 'моно',
        'stereo': 'стерео',
        'joint stereo': 'стерео',
    }
    def linkzapis( fname, imeavtor, vremena =None ):
        r = href( '%(url2papka)s/'+fname, imeavtor )
        if vremena:
            if isinstance( vremena, dict):
                mode = vremena.get( 'mode')
                mode_tx = tx_mode.get( mode, mode) or ''
                sampling_tx = vremena.get( 'sampling') or ''
                if sampling_tx:
                    sampling_tx = str(sampling_tx//1000) + 'кхц'
                kbitrate = vremena.get( 'kbitrate') or ''
                if kbitrate:
                    kbitrate_f = float( kbitrate)
                    kbitrate = int( kbitrate_f)
                    varrate = (kbitrate!=kbitrate_f)
                    kbitrate = (varrate and '~' or '') + str(kbitrate)+'кбит/с'
                rr = ' '.join( str(x) for x in (mode_tx, sampling_tx, kbitrate) if x)
                if rr:
                    r += ' '+font_1( '('+rr+')')
            #else: #int

        return r

    redove = []

    if 0: #TODO fake soundfiles( x.prevodi.values()
        if len( soundfiles) == 1 and len( x.prevodi)>1:
            elementi_bez_vryzki = True
            redove += [ linkzapis( soundfiles[0].name, imeavtor ) ]
            soundfiles = list( x.prevodi.values())

    if len( soundfiles) == 1 and (not x.prevodi or not soundfiles[0]._prevod or sykr) and not x.etiketi.nenakratko:
        if elementi_bez_vryzki: return
        redove += [ linkzapis( soundfiles[0].name, imeavtor,
                        vremena= vremena and vremena.get( soundfiles[0].name)
                        ) ]
    else:
        grupa = ''
        for y in soundfiles:
            g = ''
            if y.grupa != grupa:
                grupa = y.grupa
                redove.append( h4( url( grupa )) )
            avtor = ()
            if not bez_avtor:
                a = y.avtor #or y.avtor_s_uchastnici_bez_izp
                if a and a != x.etiketi.avtor:
                    avtor = a

            ime = sglobi( y.ime_bez_grupa_i_nomer,
                                avtor= not avtor_sled_opisanie and avtor,
                                vid= y.vid4ime,
                                godina= godina and y.godina,
                                izdanie= izdanie and izdanie_v_ime and y.izdanie,
                                )

            if elementi_bez_vryzki:
                r = ime
            else:
                r = linkzapis( y.name, ime,
                        vremena= vremena and vremena.get( y.name)
                )

            qcontent,qrecord = kachestva( y.kachestvo, default='')
            r += ' ' + qcontent

            opisania = [ lipsva_udebeli( url( str( y.opisanie))) ]
            if opis2:
                opisania += [ y.opisanie2 and url( str( y.opisanie2)),
                              #y.otkyde and y.otkyde != x.etiketi.otkyde and otkyde( y.otkyde),
                              y.povreda and lipsva_udebeli( y.povreda) or '',
                              ]

            if vid_v_opisanie:
                v = y.vid
                if not v:
                    for k in 'stihove pesen'.split():   #.. prochit teatyr ???
                        if x.znak( k, za_elementi= True, etiketi= y.etiketi):
                            v = [ x.stoinosti[ k] ]
                            break
                if v:
                    vv = []
                    for i in v:
                        if i in ime.lower(): continue #стихове..
                        i = x.stoinosti_edinstveno.get( i,i)
                        if i in ime.lower(): continue #стих..
                        if vid_v_opisanie_sykr: i = i[0]
                        vv.append( i)
                    if vv: r += ' - ' + ','.join( vv)
                    #v = [ x.stoinosti_edinstveno.get( i,i) for i in v]
                    #if vid_v_opisanie_sykr: v = [ i[0] for i in v]
                    #r += ' - ' + ','.join( v)
                    ##opisania += [ '/'+ v ]

            if avtor_sled_opisanie and avtor:
                opisania += [ ital( ','.join( avtor)) ]
            if y.vryzki and vryzki:
                opisania += [ html4vryzki( y.vryzki) ]
            if y.nagradi and nagradi:
                opisania += [ str( y.nagradi) ]

            opisania = [ html4opisanie( joinif( '\n', opisania )) ]

            uc = None
            if uchastnici or uchastnici_vse or uchastnici_sykr:
                koi = y.uchastnici_vse if uchastnici_vse else y.uchastnici
                uc = html4uchastnici( koi, sykr= uchastnici_sykr, bez_roli= uchastnici_bez_roli, samo_dejnosti= samo_dejnosti)

            if uc and uchastnici_sykr:
                if opisania: opisania += ' ; '
                opisania += [ uc ]

            if y.sydyrzhanie and sydyrzhanie:
                opisania += [ ''.join( '\n<br> '+NBSP+i
                    for i in sydyrzhanie2imena( y)) ]

            if uc and not uchastnici_sykr:
                #if not (r.endswith( 'blockquote>') or r.endswith( 'br>') ): r+= '\n<br>'
                opisania += [ uc ]
            if izdanie and not izdanie_v_ime and y._izdania:
                #if not (r.endswith( 'blockquote>') or r.endswith( 'br>') ): r+= '\n<br>'
                opisania += [ html4opisanie( izdania2text( y)) ]
            if eotkyde:
                eotkyde = y.otkyde and y.otkyde != x.etiketi.otkyde and otkyde( y.otkyde)
                if eotkyde:
                    opisania += [ html4opisanie( eotkyde) ]

            oo = []
            for b in opisania:
                b = b.strip()
                for k in 'blockquote br'.split():
                    k = '<'+k+'>'
                    if b.startswith( k): b = b[len(k):]
                for k in 'blockquote'.split():
                    k = '</'+k+'>'
                    if b.endswith( k): b = b[:-len(k)]
                b = b.strip()
                if b: oo.append( b)

            if oo:
                if not (r.endswith( 'blockquote>') or r.endswith( 'br>') ): r+= '\n<br>'
                r += blockquote( '<br>\n'.join( o.strip() for o in oo))
            else:
                r += '<br>'
            redove.append( ' ' + r )

    return html4koloni( redove)

def html4vryzki( vryzki):
    if not vryzki: return vryzki
    if isinstance( vryzki, str):
        if 'bnr.bg' in vryzki: vryzki = { vryzki: 'БНР' }
        else: #if 'chitanka.info' in vryzki:
            vryzki = { vryzki: 'текст' }
    r = ''
    for k,v in vryzki.items():
        razd = '\n'
        if k[0]=='+':
            razd = ' '
            k=k[1:]
        r += razd + href( k, v)
    return r.strip()

def izdania2text( v, bez_radio =False):
    izdania = [ joinif( ' ', listif( i.izdatel, i.nositel, i.nomer, i.neznajno and '?') ) for i in v._izdania ]
    if not izdania: return
    if bez_radio and izdania == [ radio ]: return
    return 'издания: ' + ', '.join( izdania)

def html4index( x):
    h = DictAttr( x.html, url2papka='.')

    kartinki = [ '''\
 <a href="%(k)s">
  <img src="%(i)s" alt="%(alt)s" hspace=5 align=right vspace=3 style="clear:right" >
 </a>''' % dict( locals(), alt= alt4ikona( i, x.imeavtor, h.nositel, h.izdanie))
        for k,i in sorted( zip( x.kartinki, x.ikoni_vse), key= lambda p: p[0].replace('.jpg','') ) ]

    r= ''
    #r +='<div align=right> '
    r += href( info.options.url_koren, 'Грамофонче-записи') + ':'
    #r += NBSP+NBSP
    for tip in tipove_.values():
        rr = ' ~ '+href( join( info.options.url_koren, tip.url)+'/', tip.ime)
        if tip is x.tip: rr = bold( rr)
        r+= rr
    #r += ' </div>'
    r += ' ~'

    h.razdeli = center( font_1( '\n'+r, sep=' '), sep=' ' ) + '\n'

    r = h1( x.ime) +'\n'

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
                            vremena = info.options.khz and x.timecache,
                            )
    if kartinki: kartinki = divl( kartinki, 'kolona_kartinki')

    izdania = izdania2text( x)
    if not izdania and h.eotkyde:
        izdania = 'издания:'
    if h.eotkyde:
        izdania += ' ' + h.eotkyde

    for a in [
        #'тип нещо = приказки',
        '\n'.join( kartinki),
        ['автор'    , ', '.join( razdeli_kamila2(a) for a in x.etiketi.avtor) ],
        ['вид' , ', '.join( x.vid) ],
        ['година'   , x.godina ],
        joinif( '; ', [
           ( x.etiketi.izbor     and ital('нашият избор') or '' ),
           ( x.etiketi.preporyka and bold('препоръчвам') or '' ),
           ]) or None,
        ['качество' , ' '.join( [x.etiketi.kachestvo, NBSP, kach_opis ])  ],
        ['описание' , html4opisanie( h.opisanie12) % h ],
        ['поредица' , x.etiketi.poredica ],
        ['връзки'   , html4vryzki( x.etiketi.vryzki) ],
        ['награди'  , x.etiketi.nagradi ],
        ['фон'      , x.etiketi.fon, ],
        ['участници', html4uchastnici( x.etiketi.uchastnici, sykr= False) ],
        izdania,
        '',
        [ bold('записи'), zapisi and zapisi.html % h + (zapisi.nkoloni>1 and '<br clear=left>' or '') ],
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

    h.title = x.ime_sglobeno.replace('"',"'")
    #SE optmz
    if x.tip == tipove.prikazki and 'приказк' not in h.title.lower(): h.title += '/приказки'

    return (info.options.html_pred or '''\
<?php
$title="%(title)s за слушане - Грамофонче";
$lang='bg';
$keywords='mp3 слушане детски приказки театър стихове песнички';
$hasnoen=1;
$noh1=1;
$head="
<link rel='image_src' href='/kartinki/gramofonche2.jpg'>
<link rel='stylesheet' type='text/css' href='/detski/zvuk/spisyk.css'>
";

$bodycolor='ddddc0';
include( $_SERVER['DOCUMENT_ROOT'].'/ezik.php' ); ?>

%(razdeli)s
<?php echo $header; ?>
''') % h + r + (info.options.html_sled or '''
<?php bottom() ?> <!-- svilen 2011 -->
''')

def html4spisyk( x, table =False):
    h = x.html
    imgs = [ '<img src="%(url2papka)s/%(i)s" align=right hspace=7 alt="%(alt)s">'
                    % dict( h, i=i, alt= alt4ikona( i, x.imeavtor, h.nositel, h.izdanie) )
                for i in reversed( x.ikoni) ] #reversed because of right align
    imgs_ime = joinif( '\n ', imgs + [ x.ime_sglobeno2 ] )
    content1 = href( h.url2papka+'/', imgs_ime)

    if x.etiketi.nakratko or info.options.nakratko_stihove_pesni and (x.etiketi.stihove or x.etiketi.pesni):  #XXX
        gr = [ g.kyso+' <br>' for g in x.grupi ]
        zapisi = gr and html4koloni( gr) or ''
    else:
        zapisi = html4zapisi( x, imeavtor= '(запис)',
                                sykr= True, #info.options.html_spisyk_sykr,
                                uchastnici_bez_roli= True,
                                elementi_bez_vryzki = info.options.spisyk_samo_papki,
                                sydyrzhanie = not x.etiketi.nakratko_bez_sydyrzhanie,
                                bez_avtor   = x.etiketi.nakratko_bez_otdelni_avtori,
                                uchastnici  = not x.etiketi.nakratko_bez_uchastnici,
                                samo_dejnosti= x.abbr.dejnosti_vazhni,
                            )
    sydyrzhanie = info.options.spisyk_samo_papki and not x.etiketi.nakratko and html4koloni(
                        [ i+' <br>' for i in sydyrzhanie2imena( x.etiketi)] )

    opisanie = joinif( '\n', [
            html4opisanie( h.opisanie),
            html4uchastnici( #x.uchastnici_vse,
                x.etiketi.uchastnici,
                bez_roli= True,
                sykr=  info.options.html_spisyk_sykr,
                samo_dejnosti= x.abbr.dejnosti_vazhni,
                bez_dejnosti= ( x.papka_etiketi.nakratko_bez_otdelni_avtori and
                                (x.papka_etiketi.mt_v_avtor or x.element_etiketi.mt_v_avtor) and
                                'музика текст'.split() or [])
              ),
            html4opisanie( izdania2text( x, bez_radio=True)),
            ])
    content2 = joinif( '\n ', [
                sydyrzhanie and sydyrzhanie.html,
                sydyrzhanie and sydyrzhanie.nkoloni>1 and (opisanie or zapisi) and '<br clear=left>',
                zapisi and zapisi.html,
                zapisi and zapisi.nkoloni>1 and opisanie and '<br clear=left>',
                opisanie,
                ] )

    prepizbor = NBSP*(2-len( h.prepizbor)) + h.prepizbor
    if h.prepizbor: prepizbor = '<span class=p>'+prepizbor+'</span>'
    #qcontent: #'<span class=q>
    sizes = '%(time)sмин' #:%(size)sМб'
    if 0: sizes = '<font size=-1>'+sizes+'</font>'
    else: sizes = '.. '+sizes

    return ('''
<div><hr>
 ''' + prepizbor + ''' %(qcontent)s
 ''' + content1 + '''
 ''' + sizes + '''
 ''' + content2 + '''
</div>
''') % dict( h, prepizbor= prepizbor,
            ** x.kachestva( as_dict=True)
            )

def calc_total( items, options):
    total_time = sum( x.html.time for x in items)  #or x.time??
    total_size = sum( x.size for x in items)
    total_n = len( items)
    total_n_zapisi = sum( len( x.soundfiles) for x in items)
    return DictAttr( time= total_time, size= total_size, n= total_n, n_zapisi= total_n_zapisi)

def sort4time4file( x):
    if not x.soundfiles: return 0
    return max( func( x.soundfiles[0].fname ) for func in (os.path.getmtime, os.path.getctime) )

def e_novo( x, options):
    if isinstance( x, tuple): x,_papka = x
    return (sega - x._otkoga).days < options.kolko_dni_e_novo

def key4novi_el( yx):
    return yx[0]._otkoga, yx[1].ime, yx[0].ime
def key4novi_pap( x):
    return x._otkoga, x.ime

def calc_novi( items):
    za_elementi = items and isinstance( items[0], tuple)
    if not za_elementi:
        return sorted( items, key= key4novi_pap)
    items = [ (y,x) for y,x in items if y is x or not etiket( y, 'neotdelno') ]
    bez_otkoga = [ (y,x) for y,x in items if not y._otkoga]
    if bez_otkoga:
        for y,x in bez_otkoga:
            y._otkoga = sega
            prn( '?? без откога?', y.ime, y.fname, x.ime, x.fname )
    return sorted( items, key= key4novi_el)

def html4novi( items):
    za_elementi = items and isinstance( items[0], tuple)
    for x in items:
        if za_elementi:
            key4novi = key4novi_el( x)
            y,x = x
        else:
            key4novi = key4novi_pap( x)
            y = None
        ri = url_imena( y, x)
        red = href( ri.url, ri.ime)
        yx = y or x
        #red += ' -- ('+ x.str_orgs +')'     #proizhod
        yield red, yx._otkoga, key4novi

def html4novi2li( items, novi_prez_dni):
    items = list( reversed( items))
    otkoga = None
    for red,_otkoga,key in html4novi( items):
        #red += ' ' + str((y or x)._otkoga.date())
        if novi_prez_dni:
            if not otkoga or otkoga >= _otkoga + timedelta( days= int( novi_prez_dni)):
                otkoga = _otkoga #.month
                red += ' - %s.%s.%s' % ( otkoga.day, otkoga.month, otkoga.year)
        yield red

def html_novi( items, options, html4novi ):
    #items = calc_novi( items)
    nz = items
    if options.kolko_dni_e_novo:
        nz = [ x for x in nz if e_novo( x, options) ]
    if options.kolko_sa_novi:
        nz = nz[ -options.kolko_sa_novi:]

    prn( '..new', len(nz))
    if not nz: return '',nz
    r = [ '<ul> Последни придобивки и поправки:' ]
    r+= [ '<li> '+ red for red in html4novi2li( nz, options.novi_prez_dni ) ]
    r+= [ '</ul> <hr width=50%>']
    return '\n'.join(r), nz


def url_imena( element, papka, sglobeno =True):
    y,x = element,papka #t[2:4]
    ime = x.ime_sglobeno3
    r = DictAttr(
        url= x.absurl+'/',
        ime = ime,
        el_ime = None,
        )
    if y is not None and y is not x:
        iime = sglobi( y.ime, avtor= (y.avtor != x.etiketi.avtor) and y.avtor)
        r.pap_ime= ime
        r.el_fname = y.name
        r.el_ime = iime
        r.ime = iime + ' : ' + ime
    return r #(r_pp[0],ime2r_pp,r_el



def rename( x, options):
    #MAXSZ = 82 #64  #dvd/joliet=64, longjoliet=103
    MAXSZ = options.preimenovane_max  #199
    nms = {}

    ime0 = x.ime

    papka = x.etiketi.papka or not x.etiketi.otdelni and len( x.soundfiles)>1
    izdanie = x.etiketi.izdanie
    papka_dir = papka and '--'.join( [
                            a for a in [
                            ime0,
                            x.sykrati_avtori( x.avtor_s_uchastnici( sykr_vse= True) ),
                            #x.godina,
                            koi_izdatel( izdanie, kys=True),
                            ]
                            if a ]) or ''
    papka_dir = fname_filter( papka_dir)

    for v in x.soundfiles:
        avtor_sykr = x.avtor_s_uchastnici( v, edno=True, sykr_vse= True)
        avtor_sykr = x.sykrati_avtori( avtor_sykr)
        izdanie_kyso = koi_izdatel( v.izdanie or izdanie, kys=True)
        grupa = getattr( v, 'grupa', None)
        if grupa:
            grupa = re_url.sub( '', grupa)
            grupa = grupa.split('/')[0].strip()
        nfn = '--'.join(
            str(s) #cyr2lat( s.lower().replace(' ','_'))
            for s in [
                joinif( '', [
                    x.etiketi.prefixime and ime0+'. ',
                    grupa and grupa+'. ',
                    x.etiketi.prefixavtor and avtor_sykr+'- ',
                    x.etiketi.prefixnomer and (v.nomer_str+'.'),
                    v.ime,
                    ] ),
                ] + (v.vid4ime or x.vid4ime) + [
                (not x.etiketi.prefixavtor and avtor_sykr),
                x.znak( 'godina_v_ime', v.get('etiketi'), za_elementi=True) and (v.godina or v._godina or x.godina),
                izdanie_kyso.lower(), #v.izdanie_kyso_zapis.lower(),
                ]
            if s )

        if v.nositel:   #XXX?
            nfn += '.'+ kysi_lat.get( v.nositel, cyr2lat( v.nositel)).lower()
        if '-радио' in nfn and 'lp' in nfn: #XXX?
            print( '!!!!!!!!!!!!!! ', nfn, izdanie_kyso, v.nositel, v.izdanie)
        fnoext,ext = os.path.splitext( v.name) #basename(f) )

        if options.preimenovane_lat:
            nfn = cyr2lat( nfn)
        nfn = fname_filter( nfn)

        maxsz = MAXSZ - len(ext)
        if len(nfn)>maxsz: #try shorten     #XXX len( nfn.encode('utf8') XXX
            nfn0 = nfn
            for rr in [
                ( ', ',','),
                ( '--','-'),
                ( '- ','-'),
                ( ' -','-'),
                papka and v.izdanie and ( '-'+v.izdanie, '') or (),
                ( ': ',':'),
                ( '-мюзикъл', '-мюз'),
                ( '-мюз', ''),
                ]:
                if not rr: continue
                if len(nfn)>maxsz:
                    nfn = nfn.replace( *rr)
            if len(nfn)>maxsz:
                prn( '?', x.rname+'/'+fnoext )
                prn( '?  ', nfn0, len(nfn0) )
                prn( '?? ', nfn, len(nfn),maxsz )

        assert nfn.lower() not in nms, (nfn,sorted(nms))
        nms[ nfn.lower() ]=1

        nfn += ext
        ttfile = join( papka_dir
                        #papka and '--'.join(
                        #    [ime0,
                        #    avtor_sykr,
                        #    #v.godina,
                        #    izdanie_kyso,
                        #    ]) or ''
                        , nfn)

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

        #if options.preimenovane_lat:
        #    ttfile = cyr2lat( ttfile)
        #    ttpfxs = [ cyr2lat(a) for a in ttpfxs ]
        #if options.preimenovane_opis:
            #v1: замяна на речника файлиме:речник-данни със списък от речник-данни+файлимена:имена
            #в2: запазване на речника по файлиме и само допълване на речник-данни с файлимена:имена
        yield v.relname, ttfile, ttpfxs

def rename_all( items, options):
    rename_script = []

    for x in items:
        if x.vnos: continue
        #if x.etiketi.povtorenie:
        #    prn( '!повтаря други:', x.ime)
        #    continue
        try:
            for f,ttfile,ttpfxs in rename( x, options):
                rename_script.append( 'rena2b( '+ ', '.join( '"'+a+'"'
                                                    for a in [f, ttfile]+ ttpfxs
                                                    ) + ' )' )
                if options.preimenovane_prehvyrli:
                    ff = join( *(x.path[ :x.path.index( f.split( '/', 1)[0] )] + [f] ))
                    for ttpfx in ttpfxs:
                        tt = join( options.preimenovane_prehvyrli, ttpfx, ttfile)
                        if exists( tt): continue
                        ttd = dirname( tt)
                        if not isdir( ttd): os.makedirs( ttd)
                        os.link( ff, tt)
        except:
            print( '!!!', x.ime, x.fname)
            raise

    if options.preimenovane_spisyk:
        rename_script.insert( 0, '# rena2b( src, dest, prefixes...)' )
        save_if_diff( options.preimenovane_spisyk, rename_script, prepend_py_enc= True)

def tags4mp3( x, options):
    #nokia: по първите 3 букви се познава кирилица или не... т.е. Аб.Вг не става, Абв.г става

    ikoni = x.ikoni #or x.kartinki
    if ikoni:
        image = ikoni[0].replace('.ikona','')
    else: image = None

    album_title = sglobi( x.ime,
                        x.sykrati_avtori( x.avtor_s_uchastnici( sykr_vse= True, samo_imena= False) ),
                        vid= x.vid4ime,
                        razdeli_avtor= False,
                        html= False) #x.etiketi.izdanie) #??
    izdanie = x.etiketi.izdanie
    for v in x.soundfiles:
        avtor = ','.join( #x.abbr.dai_imepylno( h) or h
                          #  for h in
                            x.avtor_s_uchastnici( v, edno= True, samo_imena= False))
        avtor = avtor.replace( ':,','') #dejnost

        izdanie = koi_izdatel( v.izdanie or izdanie)#, kys=True)
        #izdanie = izdanie.lower()

        title = sglobi(
                    #(x.etiketi.prefixime and x.ime+': ' or '') +
                    v.ime,
                        vid= v.vid4ime,
                        izdanie= izdanie,
                        razdeli_avtor= False,
                        html= False)#, nomer= v.nomer_str ) #avtor=avtor
        artist= avtor or ''
        album = joinif( ' :', [ album_title, izdanie, ] )
        godina= v.godina or v._godina or x.godina
        if godina:
            if isinstance( godina, str): godina = godina.split()
            if isinstance( godina, int): godina = [ str(godina) ]
            godina = [ g.strip('?г.') for g in godina]
            godina = str(int(godina[0]))
        nomer = v.nomer is not None and str(v.nomer) or ''

        comment = 'gramofonche@' #+','.join( x.orgs)

        if 'tags' in options.debug:
            f = v.relname
            prn( '-- %(f)-130s Title=%(title)-50s Artist=%(artist)-40s Album=%(album)s' % locals())

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
    else: cargs += [ '--remove-images' ]

    cargs += [ '$ARGSsled', '%(file)s' ]
    return cargs

apps = dict( eyed3 = tags4eyed3, mp3info = tags4mp3info)

#from svd_util.py.wither import wither

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
from dejnosti import AbbrDejnosti
class Abbr2( AbbrDejnosti):
    def dobavi( az, tt, xime):
        return AbbrDejnosti.dobavi( az, tt, xime, propusni_takiva= nskaPrikazka.syvpada )
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
        изпълнение-песни    изп-песни
        ар*анжимент
        дир*игент
    '''
    dejnosti2 = '''
        хор*майстор     .хорм      хор-дир*игент диригент-хор хордир
        музикално-оформление  .м.оф .муз.оф .м.о  .мо    музикална-картина музикална-среда музикално-оформление муз.оф*ормление муз-оф*ормление музикален-редактор
        звуково-оформление    .зв.оф .зв .з .з.оф*ормление  .зв.еф*екти .з.е*фекти .зе звук звукова-картина звукова-среда звуково-оформление зв.оф*ормление звукови-еф*екти ефекти
        звукор*ежисьор  .зв.р*еж   .з.р*еж      тонр*ежисьор тон.реж*исьор
        звукооп*ератор  .зв.оп     .з.оп        тоноп*ератор тон.оп*ератор
        звукоинж*енер   .зв.инж    .з.инж       тонинж*енер тонм*айстор тон.инж*енер
        звукот*ехник    .зв.т*ехник  .з.т*ехн     тонт*ехник зв.тех*ник тон.т*ехник
        звукозапис      запис
        звукообр*аботка постпр*одукция .зв.обр .з.обр
        ред*актор       .ред
        рис*унка        .рис
        худ*ожник       .худ
        художествено-оформление .худ.оф .х.оф
        фот*ограф       снимки снимка
    '''
    dejnosti3 = '''
       *изп*ълнение                     изпълни*тели изпълня*ват
        сол*ист                         солисти
    '''
    dejnosti = dejnosti1 + dejnosti3 + dejnosti2

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


from svd_util.attr import get_attrib
podredba = dict(
    #ime= 'az',
    #ime_sglobeno= 'az',
    avtor= lambda x: x.etiketi.avtor or [],
    humor= lambda x: bool( x.etiketi.humor),
    stihove= lambda x: bool( x.etiketi.stihove),
    kachestvo= lambda x: (not x.etiketi.preporyka, not x.etiketi.izbor, x.etiketi.kachestvo),
    pored= lambda x: x.etiketi.pored == '' and 999 or int(x.etiketi.pored),
    dokumentalni= lambda x: bool( x.etiketi.dokumentalni),
    teatyr = lambda x: bool( x.e_teatyr),
    portret = lambda x: bool( x.etiketi.portret),
    izdanie= lambda x: x.etiketi.izdanie,
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

def _html_spisyk( items, table =False, gotovi =False):
    if gotovi:
        result = ''.join( items)
    else:
        result = ''.join( html4spisyk( x, table=table) for x in items)
    result += '<br clear=all>'
    return result

def html_spisyk( options, spisyk, izbor, total, novi, gotovi =False, html4novi =html4novi):
    if options.obshto_broi_zapisi: total.n = total.n_zapisi
    htotal = '''
общо: %(n)sброя / %(size)sMb / %(time_h)sчаса ''' % dict( total, time_h= total.time//60)
        #time_h = '%.1f' % (total.time/60.0)

    spisyk = _html_spisyk( spisyk, gotovi= gotovi)
    rt = [spisyk, htotal]
    if options.obshto_otgore: rt.reverse()

    rnovo,najnovi = html_novi( novi, options, html4novi= html4novi)
    if options.html_novi:
        save_if_diff( options.html_novi, rnovo, enc= options.html_enc )
    else:
        rt.insert( options.obshto_otgore and 0, rnovo)
    if options.html_novi_vse:
        save_if_diff( options.html_novi_vse,
            ' <br>\n'.join( html4novi2li( novi, novi_prez_dni=1)),
            enc= options.html_enc )
    rhtml = '\n<hr>\n'.join( rt)

    save_if_diff( options.html_spisyk, rhtml, enc= options.html_enc )

    if options.html_izbrani:
        hubavi = _html_spisyk( izbor, gotovi= gotovi)
        save_if_diff( options.html_izbrani, hubavi, enc= options.html_enc )


def vse( items, options):
    prn( '..zvuci')

    for x in items:
        try:
            x.setup()
        except :
            prn( '? ? ', x.fname, x.ime)
            raise

    #prn( '..proizhod:', ' '.join( sorted( info.vse_str_orgs)))

    sykr_all( items, options)

    if options.ima_etiket:
        e = options.ima_etiket
        def ima_etiket( x, ee):
            if isinstance( ee, str): ee = [ee]
            for e in ee:
                if x.znak( e) or any( x.znak( e, y.get('etiketi'), za_elementi=True) for y in x.soundfiles):
                    return True
            #return x.znak( e) or any( x.znak( e, y.get('etiketi'), za_elementi=True) for y in x.soundfiles)
        items = [ x for x in items if ima_etiket( x, e) ]
    if options.vkl_etiket:
        e = options.vkl_etiket
        items = [ x for x in items if x.etiketi[ e] ]
    if options.izkl_etiket:
        ee = options.izkl_etiket
        if isinstance( ee, str): ee = [ee]
        items = [ x for x in items if not any( x.etiketi[ e] for e in ee) ]

    for x in items:
        try:
            avtor = x.avtor_s_uchastnici( samo_imena= False)
            x.imeavtor = sglobi( x.ime, avtor= avtor, vid= x.vid4ime )
            x.ime_sglobeno = sglobi( x.ime, avtor= avtor, vid= x.vid4ime,
                                    izdanie= ' '.join( x.v_zaglavieto),
                                    html= False )
            x.ime_sglobeno2= sglobi( x.ime, avtor= avtor, vid= x.vid4ime,
                                    izdanie= ' '.join( x.v_zaglavieto),
                                    godina= x.godina
                                    )
            x.ime_sglobeno3= x.ime_sglobeno2
            if x.etiketi.stihove and x.etiketi.uchastnici == x.uchastnici_vse:
                #if sum( bool( y.get('etiketi',{} ).get('stihove')) for y in x.soundfiles) == len( x.soundfiles):
                if all( y.get('etiketi',{} ).get('stihove') for y in x.soundfiles):
                    avtor = x.avtor_s_uchastnici( x.soundfiles[0], samo_imena= False)
                    x.ime_sglobeno3= sglobi( x.ime, avtor= avtor, vid= x.vid4ime,
                                    izdanie= ' '.join( x.v_zaglavieto),
                                    godina= x.godina
                                    )
                #if x.ime_sglobeno3 != x.ime_sglobeno2: prn( 11111111111, x.ime_sglobeno3)
        except :
            prn( '? ? ', x.fname, x.ime)
            raise
        '''
        index   : h1= .ime ; title= .ime_sglobeno
        spisyk  : href.txt= .ime_sglobeno2
        novi    : href.txt= .ime_sglobeno2
        *link   : href.txt= .ime_sglobeno2
        ikoni   : alt= .imeavtor
        zapis   : href.txt= .imeavtor
        '''

    options.podredba = options.podredba.split(',')
    items.sort( key= podredi)

    if 'items' in options.debug:
        for x in items:
            prn( x.ime)
            prn( x.ime_sglobeno)
            prn( x.ime_sglobeno2)
            prn( x.ime_sglobeno3)
            prn( x.uchastnici_vse)
            prn( x.etiketi.avtor_s_uchastnici)
            pprint.pprint( x.etiketi)

            #for c in x.soundfiles: pprint.pprint( c)

            prn( 20*'#')

    items2 = []
    for x in items:
        if x.etiketi.otdelni:
            items2 += [ (v,x) for v in x.soundfiles ]
        else: items2.append( (x,x))

    if options.html_spisyk or options.html_index:
        sizes( items, options)
        times( items, options)
        for x in items:
            try: html(x)
            except:
                prn( '?', x.fname)
                raise


    if options.html_spisyk:
        html_spisyk( options,
            spisyk = items,
            novi = calc_novi( items2),
            total = calc_total( items, options),
            izbor = [ x for x in items if x.html.prepizbor and not x.vnos],
            )

    if options.html_index:
        for x in items:
            if x.vnos: continue
            ofname = join( x.fname, options.html_index)
            try:
                save_if_diff( ofname, html4index( x), enc= options.html_enc )
            except:
                prn( '?', x.fname)
                raise

    if options.html_papka:
        assert len( items)==1
        x = items[0]
        if x.vnos:
            prn( 'vnos', x.fname)
        else:
            data4papka = DictAttr(
                total   = calc_total( items, options),
                html4novi = list( html4novi( calc_novi( items2))),
                izbor   = bool( not x.vnos and (x.etiketi.preporyka or x.etiketi.izbor )),
                spisyk  = html4spisyk( x),
                podredba = podredi( x),
            )
            ofname = join( x.fname, options.html_papka)
            save_if_diff( ofname, pprint.pformat( data4papka), enc= options.html_enc )
            #save_if_diff( 'spisyk', html_spisyk( items), enc= options.html_enc )

    if options.html_hora or options.index_hora:
        index_hora( items2, options)
    if options.preimenovane_spisyk or options.preimenovane_prehvyrli:
        rename_all( items, options)
    if options.tags_app:
        tags4mp3_all( items, options)
    if options.izdania_spisyk:
        izdania_spisyk( items, options)
    if options.otdeli:
        for x in items:
            if x.vnos: continue
            if not x.etiketi.otdelni: continue
            if len( x.soundfiles)<=1: continue
            for y in x.soundfiles:
                avtor_kyso = '-'.join( razdeli_kamila2( h) #x.abbr.dai_imepylno( h) or h)
                            for h in x.avtor_s_uchastnici( y, edno=True, sykr_neavtori =True))
                avtor_kyso = avtor_kyso.replace( '. ','.')
                izdanie_kyso = koi_izdatel( y.izdanie or x.etiketi.izdanie, kys=True)
                nositel = kysi_lat.get( y.nositel, y.nositel)
                nfn = '--'.join( s
                    for s in [
                        joinif( '', [
                            x.etiketi.prefixime and x.ime+': ',
                            x.etiketi.prefixavtor and avtor_kyso+': ',
                            x.etiketi.prefixnomer and (y.nomer_str+'.'),
                            y.ime_kyso or y.ime,
                            ] + [ '-'+k for k in y.vid4ime or x.vid4ime
                            ]
                            ),
                        (not x.etiketi.prefixavtor and avtor_kyso),
                        izdanie_kyso.lower(),
                        ]
                    if s )
                if nositel:
                    nfn += '.'+ nositel
                nfn = nfn.replace(' ', '_')

                oname = os.path.splitext( y.name)[0]
                oname = cyr2lat( nfn.lower())

                ofdir = join( x.fname, oname)
                if not isdir( ofdir): os.makedirs( ofdir)
                ofname = join( ofdir, y.name)
                prn( ofname)
                if not exists( ofname): os.link( y.fname, ofname)

                o = info( fname= ofdir )
                o.slaga_ime( y.ime)
                o.etiketi.update_pre( **dict((k,v) for k,v in dict(
                    avtor   = y.avtor or x.avtor,
                    izdanie = y.izdanie or x.etiketi.izdanie,
                    godina  = y.godina or y._godina or x.godina,
                    uchastnici = y.uchastnici_vse,
                    #uchastnici_vse = y.uchastnici_vse,
                    vid     = extendif( extendif( [], y.vid), x.vid),
                    ).items() if v #and v.strip()
                    )
                )

                def upd_ako_nema( o, i):
                    for k,v in i.items():
                        if k == info.stoinosti.etiketi: continue
                        if k not in info.stoinosti0 and k not in info.stoinosti: continue
                        if not o.get( k) and v:
                            o[ k] = v
                    return o
                upd_ako_nema( o.etiketi, y.etiketi)
                upd_ako_nema( o.etiketi, x.etiketi_element)
                izbegni = 'nomer prefix nakratko otdelni neotdelno sort_prevodi'.split()
                izbegni += [ info.stoinosti[k] for k in izbegni]
                for k,v in x.etiketi.items():
                    if v is True and not o.etiketi.get(k) and k not in izbegni:
                        o.etiketi[k] = v
                upd_ako_nema( o.etiketi, y)

                #o.samopopylva_etiketi()
                razlika, t = o.zapis( naistina= True or options.zapis_opisi )

def izdania_spisyk( items, options):
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
                avtor = az.avtor_s_uchastnici( samo_imena= False) or '',
                vid = az.vid,
                shapka= 1,
                fname = az.rname,
                absurl = az.absurl,
                )]
        if len(az.soundfiles)>1:
            for v in az.soundfiles:
                if re.search( '(страна|част) *[1-9]$', v.ime, re.IGNORECASE): continue
                appendif( ii[0].ime, v.ime )
                if v._izdania:
                    ii+= [ DictAttr(
                            izdanie= v._izdania,
                            godina = v.godina or '',
                            ime   = [ v.ime ],
                            avtor = az.avtor_s_uchastnici( v, samo_imena= False) or '',
                            shapka= 0,
                            fname = v.relname,
                            vid = v.vid or az.vid,
                            absurl = join( az.absurl, v.name),
                            )]

        for d in ii:
            xizdanie = d.izdanie
            assert isinstance( xizdanie, (list,tuple)), xizdanie
            #xgodina  = xizdanie.godina and xizdanie.godina.split() or a2list( d.godina)
            xgodina = a2list( d.godina)
            xavtor  = a2list( d.avtor)

            for i in xizdanie:
                if i.izdatel in (radio, 'avtori.com'): continue
                m = re_izd.match( i.nomer )
                assert m, d
                dd = DictAttr(
                                prednomer= m.group(1),
                                samonomer= m.group(2),
                                slednomer= m.group(3),
                                izdatel= i.izdatel,
                                nomer  = i.nomer,
                                nositel= i.nositel,
                            )
                if not dd.samonomer:
                    neizv-=1
                    dd.samonomer = neizv
                else:
                    dd.samonomer = int( dd.samonomer)
                di = izd.setdefault( (dd.izdatel, dd.nositel, dd.nomer, dd.samonomer), dd)
                di.setdefault( 'godina', set()).update( xgodina)
                extendif( di.setdefault( 'ime', [] ), d.ime)
                extendif( di.setdefault( 'avtor', []), xavtor)
                di.setdefault( 'fname', set()).add( d.fname)
                di.setdefault( 'absurl', set()).add( d.absurl)
                di.setdefault( 'vid', set()).update( d.get( 'vid',()))

    r = []
    for i in sorted( izd.values(),
                key= lambda i: (i.izdatel, i.nositel,
                                    i.samonomer, i.prednomer, i.slednomer) ):
        for a,v in i.items():
            if a in ('avtor', 'vid'): continue
            if isinstance( v,(tuple,set,list)) and len(v)==1: i[a] = list(v)[0]
        o = dictOrder()
        d = attr2item(o)
        d.izdatel = i.izdatel
        d.nositel = i.nositel
        d.nomer = i.nomer or '?'
        d.samonomer = ''
        if i.samonomer>0:
            d.samonomer = str(i.samonomer)
            if i.slednomer.startswith(','):
                d.samonomer += ','+ d.samonomer[ : len(d.samonomer)-len(i.slednomer)+1] + i.slednomer[1:]
        d.ime = i.ime
        #d.avtor = i.avtor and ':'+'+'.join( i.avtor) or ''
        d.avtor = i.avtor and ', '.join( [ razdeli_kamila2(a) for a in i.avtor]) or ''
        d.avtor = d.avtor.replace( ':, ', ' ') #dejnost

        d.godina = i.godina or ''
        #d.vid = i.vid and '('+','.join( i.vid)+')' or ''
        d.vid = i.vid and ' '.join( i.vid) or ''
        d.fname  = isinstance( i.fname, str) and [ i.fname] or list( i.fname )
        d.url    = isinstance( i.absurl, str) and [ i.absurl ] or list( i.absurl )

        r.append( o)

    if options.izdania_spisyk.endswith( '.csv'):
        from io import StringIO
        import csv
        f = StringIO()
        cw = csv.writer( f)
        cw.writerow( [ k for k in r[0]
                         if k not in ['fname', ]
                         ])
        for o in r:
            o['url'] = [ 'http://www.svilendobrev.com' + i for i in o['url'] ]
            cw.writerow( [ isinstance( v, str) and v or '\n'.join( v)
                            for k,v in o.items()
                            if k not in ['fname', ]
                            ] )
        rr = f.getvalue()
    else:
        rr = [' '.join( str( l) for l in o.values()) for o in r]

    save_if_diff( options.izdania_spisyk, rr, enc= options.html_enc )


def index_hora( items2, options):
    uchastnici = []
    for y,x in items2:
        if y.uchastnici_vse:
            for dejnost,hora in y.uchastnici_vse.items():
                for h in hora:
                    uchastnici.append( DictAttr( dejnost= dejnost, ime= info.Uchastnici.h2hr(h)[0], element= y, papka= x))
        for h in y.avtor1 if y is not x else y.etiketi.avtor1:
            uchastnici.append( DictAttr( dejnost= 'автор', ime= h, element= y, papka= x))

    uuchastnici = [ DictAttr( h= a.ime, d= a.dejnost, p= a.papka, e= a.element) for a in uchastnici ] #None if a.element is a.papka else

    #txt = ''.join( str( dict(u))+',\n' for u in uchastnici)
    from itertools import groupby
    for po_dejnost in False, True:
        fkey = po_dejnost and (lambda a: (a.d, a.h, a.e, a.p, a)) or (lambda a: (a.h, a.d, a.e, a.p, a))
        uu = sorted( (fkey(u) for u in uuchastnici), key= lambda t: (t[:2],t[2].ime,t[3].ime) )
                #key= po_dejnost and (lambda a: (a.d, a.h, a.e, a.p)) or (lambda a: (a.h, a.d, a.e, a.p))
                #)
        if options.index_hora:
            if not po_dejnost:
                save_if_diff( options.index_hora + 'hdep', pprint.pformat(
                    [ [ u[0], u[1], url_imena( u[2], u[3]) ]
                        for u in uu],
                    width=120), enc= options.html_enc )
            continue

        key = po_dejnost and 'd' or 'h'
        gg = groupby( uu, key= lambda u: u[0] )
        tt = [ (k, groupby( list(g), key= lambda u: u[1])) for k,g in gg ]
        if 0:
            txt = [ 'array(' ]
            for k,g in tt:
                txt += [ repr(k) + '=> array(' ] #nt( 1111, k)
                for k2,u in g:
                    txt += [ ' '+repr(k2) + '=> array(',
                            ',\n'.join( '  ' + repr( t[2]) for t in u),
                            ' ),' ]
                txt[-1] = txt[-1].rstrip(',')
                txt += [ '),' ]
            txt[-1] = txt[-1].rstrip(',')
            txt += [ ')' ]
            txt = '\n'.join( txt)

        elif 1:
            txt = [ '<ul>' ]
            for k,g in tt:
                txt += [ '<li> '+str(k) + ' <ul>' ]
                for k2,u in g:
                    txt += [ ' <li>'+str(k2) + ' <ul>' ]
                    for t in u:
                        ri = url_imena( *t[2:4])
                        txt += [ '  <li>' + href( ri.url, ri.ime ) ]
                    #txt += [ '  <li>' + str( t[2])
                    txt += [ '  </ul>' ]
                txt += [ ' </ul>' ]
            txt += [ '</ul>' ]
            txt = '\n'.join( txt)

        else:
            txt = 'array(\n  ' + ',\n'.join(
                repr(k) + ' => array(\n    ' +',\n'.join(
                                repr(k2) + ' => array( ' + ', '.join( repr(v) for v in u[2:] ) + ')'
                                for k2,u in list(g)
                                )+ ')'
                for k,g in tt ) + '''
)
'''
        save_if_diff( options.html_hora + (po_dejnost and 'd2h' or 'h2d'), txt, enc= options.html_enc )


if __name__ == '__main__':
    info.main()

# vim:ts=4:sw=4:expandtab

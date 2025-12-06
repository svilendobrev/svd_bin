#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
детски/
    ледена-епоха/
        опис: заглавие=.., етикет:анимация етикет:дълги етикет:градина
        1.бг/
            опис: заглавие + наследява другото
        къси/
            опис: заглавие + етикет:къси + наследява другото
    франклин/
        опис: заглавие=.., етикет:анимация етикет:къси етикет:серийки етикет:ясла

 - разходка по директории, и за всяка, ако има файл опис, се употребява
'''

from svd_util.py3 import *
from svd_util import eutf, optz, lat2cyr
cyr2lat = lat2cyr.zvuchene.cyr2lat
#from svd_util.structs import DictAttr, attr2item
from svd_util.dicts import DictAttr, DictAttr_lower, dict_lower, make_dict_lower
dictOrder_lower = make_dict_lower( dictOrder)
from svd_util.dicts import make_dict_trans, make_dict_attr

import fnmatch, locale
from glob import glob
from svd_util.osextra import globescape
import sys, os.path, re
from os.path import isdir, basename, exists, join, dirname, realpath
#from difflib import unified_diff as diff
from svd_util.diff import unified_diff_ignore_space as diff
from svd_util.lists import appendif, extendif, listif

from instr import meta_prevodi, zaglavie, nezaglavie

_DictAttrTrans = make_dict_attr( make_dict_trans() )

OPIS = 'opis'
OPISI = [ OPIS ]#, OPIS +'.yaml']
OPISIpat = OPISI

def e_opis( fname):
    for pat in OPISIpat:
        pat = globescape( pat)
        if fnmatch.fnmatch( fname, pat): return True
    return False
    return fname in OPISI
    return fname.split('.')[0] == OPIS

use_stderr =False
def err( *a, **kargs):
    stderr = use_stderr or 'use_stderr' in kargs or 'stderr' in kargs
    o = stderr and sys.stderr or sys.stdout
    o.write( ' '.join( unicode(x) for x in a) + '\n')
prn = err

def commonprefix( prefixi):
    pfx = os.path.commonprefix( prefixi)
    #до "цяла" директория
    while pfx and pfx not in prefixi and pfx[-1]!='/':
        pfx = pfx[:-1]
    return pfx

def fnmatch_list( fn, pats):
    for pat in pats:
        if fnmatch.fnmatch( fn, pat):
            return True

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
def ntfs_fname_filter( f, context =None, repl ='.'):
    if not isinstance( repl, dict): repl = { None: repl }
    repl_default = repl[None]
    for n in ntfs_forbids:
        r = repl.get( n, repl_default)
        if r == n: continue
        if context and n in f: err( context, f'-> {f} не може да има {n}, заменям с {r}')
        f = f.replace( n, r)
    f = f.strip()
    f = f.rstrip(' '+repl_default)
    return f

def noslash( fn, *context):
    if '/' in fn:
        err( context, '->', fn, 'не може да има /, заменям с -')
        fn = fn.replace( '/','-')
    return fn

def ili( a,b): return bool(a) or bool(b)
def i( a,b): return bool(a) and bool(b)
def ako( a,b,c=''): return str(b) if a else str(c)
def vyv( a,b):
    if isinstance( b, str): return a.lower() in b.lower()
    return a.lower() in [x.lower() for x in b]
def ne( a): return not a
def joinif( s, *aa): return s.join( str(a) for a in aa if str(a).strip())


#TODO ioformat
def prevodi_parse( a, n ):
    sep = ('==' in a) and '==' or '='
    kvo = [ x.strip() for x in a.split( sep,2) ]
    if not (2<= len(kvo) <=3):
        raise RuntimeError( 'грешен ред %(n)s: %(a)s' % locals())
    if len(kvo)==3:
        l,r,o = kvo
    else:
        l,r = kvo
        o = None
    return l,r,o

#TODO ioformat
def prevodi_file2ime( redove):
    pp = []
    l_utf = r_utf = 0
    n=0
    for a in redove:
        n+=1
        a = a.strip()
        if not a or a[0]=='#': continue
        l,r,o = prevodi_parse( a, n)
        if not l and not r: continue
        pp.append( (l,(r,o)) )
        try: l.encode( 'ascii')
        except: l_utf += 1
        try: r.encode( 'ascii')
        except: r_utf += 1
    if l_utf > r_utf: pp = [ (v,(k,o)) for k,(v,o) in pp ]
    return pp #dict( pp)

def save_if_diff( fname, r, naistina =False, enc ='utf8', podrobno =True, makedirs= True, prepend_py_enc =False, prezapis =False):
    try:
        if isinstance( r, str): r = r.strip().split( '\n')
        r = [ x.rstrip() for x in r ]
        if prepend_py_enc:
            tenc = '# -*- coding: {enc} -*-'.format( **locals())
            if tenc not in r[:2]:
                r.insert( 0, tenc )
        txt = '\n'.join( r)

        if exists( fname):
            org = list( eutf.readlines( fname))
            org = [ x.rstrip() for x in org ]
        else:
            org = []

        razlika = (r != org)
        if razlika:
            if podrobno:
                if not org:
                    prn( 'ново:', fname )
                    prn( txt)
                else:
                    prn( 'разлика:', fname )
                    df = diff( org, r, 'старо', 'ново', lineterm='')
                    ima=0
                    for l in df:
                        ima=1
                        if l.startswith('---') or l.startswith('+++'): continue
                        prn( l)
                    if not ima:
                        for a,b in zip( org,r):
                            if a!=b:
                                prn( '?<'+repr(a))
                                prn( '?>'+repr(b))
        if razlika or prezapis:
            if naistina:
                if makedirs:
                    import os.path
                    fpath = os.path.dirname( fname)
                    if fpath and not os.path.exists( fpath): os.makedirs( fpath )
                prn( '>>>', fname)
                with eutf.filew( enc, fname ) as of:
                    of.write( txt+'\n')
        return razlika, txt
    except:
        prn( '??', fname)
        raise

def str2list( ss, sep ='\n'):
    #ss = e.pop( az.stoinosti.sydyrzhanie, () )
    if isinstance( ss, str):
        ss = ss.strip().split( '\n')
    else:
        ss = list( ss)
    while ss and not (ss[0]  or '').strip(): del ss[0]
    while ss and not (ss[-1] or '').strip(): del ss[-1]
    return ss

class Naslagvane:
    def __init__( az, sloeve, bool =True):
        az._sloeve = sloeve
        az._bool = bool
    def __contains__( az, k):
        for a in az._sloeve:
            if k in a: return True
        return False
    def __getitem__( az, k):
        r = f = None
        for a in az._sloeve:
            try:
                r = a[k]
                f = True
            except KeyError: continue
            if az._bool and r: return r
        if az._bool and f: return r
        raise KeyError( k)
    def __getattr__( az, k):
        try: return az[k]
        except KeyError: raise AttributeError( k)


helplist = ' (може няколко)'

class info:
    '''свойства:
име т.е. заглавие
етикет: стойност
етикет етикет   (символи)

съдържание: #при единичен файл съдържащ няколко неща
преводи:    #при няколко отделни файла
 [група: име]
 файл-име == заглавие
'''
    options = None
    @staticmethod
    def opts():
        optz.help( '''%prog [опции] папка ..
обхожда папките и зарежда данни от файлове именовани "opis", и изпълнява действия с тези данни''')
        gg = optz.grouparg( 'данни')
        optz.str( 'prevodi',        help= 'файл-речник с преводи файл=заглавие или заглавие=файл (lat=cyr)', **gg)
        optz.str( 'prevodi_meta',   help= 'файл-речник с преводи на понятия (lat=cyr) - хора, организации, ..', **gg)
        optz.str( 'filename_enc',   help= 'кодировка на имената на файловете [или това от терминала]', **gg)
        gg = optz.grouparg( 'описи')
        optz.bool( 'zapis_opisi',   help= '(пре)записва описите', **gg)
        optz.append( 'etiket', '-e',help= 'добавя етикета към _всички описи'+helplist, **gg)
        optz.bool( 'sort_prevodi',  help= 'пренарежда преводите по азбучен ред', **gg)
        optz.bool( 'popravi_opisi', help= 'имената в речника с преводи имат превес над местните в описите', **gg)

        optz.bool( 'podravni_po_grupi', help= 'подравнява в описа всяка група за себе си; иначе подравнява всички заедно', **gg)
        optz.bool( 'mnogoredovi_etiketi',   help= 'многоредовите се записват като 1 ключ:: с много редове, без пренасяне (иначе много ключ:реда)', **gg)

        optz.int(  'shirina_tekstove',  default=80, help= 'ширина на пренасяне на текстове; подразбиране- %default', **gg)
        optz.bool( 'yaml')  #ignore
        optz.bool( 'noyaml')
        optz.bool( 'ntfs',  help= 'замества с "-" непозволеното в имена на файлове според NTFS/samba: '+ntfs_forbids)

        #optz.bool( 'vinagi',  '-f',help= 'записва независимо дали има разлики', **gg)

        gg = optz.grouparg( 'обхождане')
        optz.append( 'opisi',           help= 'шаблон за името на описите ['+' '.join( OPISI)+']'+helplist, **gg)
        optz.bool( 'simvolni', '-L',    help= 'обхожда и символни връзки', **gg)
        optz.append( 'bez',             help= 'пропуска (папки) по дадения шаблон'+helplist,  **gg)
        optz.append( 'samo',            help= 'включва само (папки) по дадения шаблон'+helplist,  **gg)
        optz.append( 'papka_s_opisi',   help= 'счита всички файлове вътре за описи (и се прилагат горните шаблони)'+helplist, **gg)

        gg = optz.grouparg( 'действия с папки')
        optz.bool( 'preimenovai_papki', help= 'преименова+превежда папките на място', **gg)
        optz.str(  'prehvyrli_papki',   help= 'прехвърля+превежда папки+съдържание към тук/', **gg)
        optz.bool( 'prehvyrli_simvolno', help= 'прехвърля като символни връзки (иначе са твърди)', **gg)

        optz.bool( 'davai',         help= 'извършва промените', **gg)

        #разни
        optz.bool( 'stderr',        help= 'грешки и съобщения към stderr')
        optz.count( 'podrobno', '-v', help= 'показва подробности')

    #lat2cyr преводи и съкращения на етикети/стойности
    #.stoinosti: всичко към кирилица/първото отдясно
    #.rstoinosti: всичко към latinica/ключа отляво
    stoinosti0 = DictAttr(
        #само папката
        prevodi     = 'пар*чета части превод*и',
        grupi       = 'групи',
        grupa       = 'група',
        grupa_i_nomer= 'група-номер',
        nomer       = 'номер',
        nomervgrupa = 'нг номер-в-група номер-група',
        shablon     = 'шаблон',
        sort_prevodi= 'подреди-парчета подреди-части подреди-преводи подреди',
        #simvoli_papka   = 'етикети-папка   eт-пап*ка   символи-пап*ка',
        #само елементите
        shablon_element = 'шаблон-елемент',
        #simvoli_element = 'етикети-елемент eт-ел*емент символи-ел*ементи',
        #на папката/елемента
        ime         = 'име',
        imena       = 'имена',
        opisanie    = 'опис*ание',
        sydyrzhanie = 'съд*ържание',
        simvoli     = 'ет*икети символ*и',
        zvuk        = 'зв*ук zw*uk zv*uk  език',
        original    = 'оригинал',
        #за/от елементите и в папка
        avtor       = 'ав*тор aw*tor auth*or',
        godina      = 'година г год year y',
        sfx         = 'наставка',
        ########
        element     = 'ел*ементи',
        papka       = 'пап*ка',
        pyt         = 'път',
        )


    ezici = dict(
        bg = 'бг',
        ru = 'ру',
        en = 'ан',
        fr = 'фр',
        ja = 'яп',
        )
    re_ezik_ime = re.compile( r'^\.('+'|'.join( ezici)+'): *(.*) *$' )
    rezici = dict( (v,k) for k,v in ezici.items())

    def _godina( k):
        k= str(k)
        return k.isdigit() and len(k)==4 and k

    zamestiteli_po_stoinost = dict(    #прилагат се в/у стойност без етикет и при успех донасят етикет
        #avtor = avtori_en,  #+ ..
        zvuk  = ezici,
        godina= _godina #lambda k: isinstance( k,str) and k.isdigit() and len(k)==4 and k,
    )

    prevodachi = dict(      #прилагат се по вид етикет в/у стойността; включват zamestiteli_po_stoinost
        ime  = zaglavie,
        #avtor= zaglavie,
    )

    #прилагат се по вид етикет в/у текущата стойност и новата стойност
    @staticmethod
    def smesitel( staro,novo):
        if not isinstance( staro, (list, tuple)): staro = [ staro]
        if not isinstance( novo,  (list, tuple)): novo  = [ novo]
        r = list( staro) + list( novo)
        if len(r)==1: r = r[0]
        return r
    def zalepi_text( staro,novo): return '\n'.join( s for s in [staro, novo] if s.strip() )
    smesiteli = dict(      #прилагат се по вид етикет в/у текущата стойност и новата стойност
        opisanie = zalepi_text,
    )

    #етикети които се наследяват по дървото от папки
    nasledimi       = 'шаблон шаблон_елемент'.split()
    #етикети които са извадени отделно
    izvyn_etiketi   = 'име преводи'.split() #съдържание

    @classmethod
    def ime2imena( az, k, etiketi):
        l = k.split('.')
        if len(l) != 2: return
        a,b = l
        if az.stoinosti.get( a) != az.stoinosti.ime: return
        b = az.rezici.get( az.ezici.get(b,b), b)    #2lat
        if az.stoinosti.imena not in etiketi:
            etiketi.imena = dictOrder()  #ezik:ime
        etiketi.imena[ b] = etiketi.pop( k)
        return k

    _inited =0
    @classmethod
    def _init( klas):
        if info._inited: return
        info._inited = 1

        info.stoinosti = stoinosti = DictAttr_lower()
        info.stoinosti_imena = dict()
        info.rstoinosti = dict_lower()
        def kxv2kvv( d, dict_v0_k_v1 =True):
            if isinstance( d, dict):
                for k,vv in d.items():
                    vv = vv.split()
                    if dict_v0_k_v1: yield [vv[0],k]+vv[1:]
                    else: yield [k] + vv
            else:  #list
                for kvv in d:
                    yield kvv.split()

        #TODO ioformat; обедини тези kxv2kvv с meta_prevodi и може би Abbr и prevodi ??
        for kvv in kxv2kvv( klas.stoinosti0, dict_v0_k_v1= True):
            v0 = kvv[0].replace( '*','')
            k  = kvv[1]
            for v in list(kvv):
                if '-' not in v: continue
                extendif( kvv, [v.replace('-',''), v.replace('-','_')])
            kvv1 = []
            for v in kvv:
                if '*' not in v:
                    appendif( kvv1, v)
                    continue
                l,r = v.split('*')
                extendif( kvv1, [ l+r[:i] for i in range( len(r)+1)] )
            kvv = kvv1
            for v in list(kvv):
                appendif( kvv, cyr2lat( v))

            assert '*' not in k #lat
            assert '*' not in v0 #cyr

            for v in kvv:
                assert '*' not in v, v
                assert v not in stoinosti, v
                info.rstoinosti[ v] = k
                stoinosti[ v] = v0
            info.stoinosti_imena[ v0] = kvv
        #prn( 111111111, stoinosti)
        klas.nasledimi      = [ stoinosti[k] for k in klas.nasledimi ]
        klas.izvyn_etiketi  = [ stoinosti[k] for k in klas.izvyn_etiketi ]
        klas.prevodachi     = dict( (stoinosti[k],v) for k,v in klas.prevodachi.items())

        zamestiteli_po_stoinost = DictAttr()
        for et,zam in klas.zamestiteli_po_stoinost.items():
            if not callable( zam):
                rechnik = dict_lower()
                for kvv in kxv2kvv( zam, dict_v0_k_v1 =True):
                    v0 = kvv[0]
                    for v in kvv:
                        rechnik[ v ] = v0
                zam = rechnik
            etp = stoinosti.get( et,et)     #.lat = .cyr = ...
            zamestiteli_po_stoinost[ et] = zamestiteli_po_stoinost[ etp] = zam
            if etp not in klas.prevodachi: klas.prevodachi[ etp] = zam
        klas.zamestiteli_po_stoinost = zamestiteli_po_stoinost

    @classmethod
    def _slaga_etiket( az, k, v, rechnik, zamesti =True):
        k = k.lower()
        k = az.stoinosti.get( k, k)     #опис-> описание anim-> анимация

        if v is True:   #съкращения и къси форми: 2000-> godina=2000, pixar-> avtor=pixar
            #независими - носят ключ
            for et,zam in az.zamestiteli_po_stoinost.items():
                if callable( zam): vv = zam(k)
                else: vv = zam.get( k )
                if vv:
                    k,v = az.stoinosti[ et],vv
                    break

        else: #if v is not True:   #превод на стойности на етикети - имат ключ
            zam = az.prevodachi.get( k)
            if callable( zam): v = zam( v) or v
            elif zam: v = zam.get( v,v)

        if v or v==0:
            if zamesti or k not in rechnik:
                rechnik[ k ] = v
            else:
                rechnik[ k ] = az.smesiteli.get( k, az.smesitel)( rechnik[ k ], v )
        elif zamesti:
            rechnik.pop( k, None)

        return v

    def slaga_etiket( az, k, v, **kw):
        return az._slaga_etiket( k, v, az.etiketi, **kw)
    def slaga_ime( az, v):
        assert '/' not in v, v+'? '+az.fname
        return az.slaga_etiket( az.stoinosti.ime, v)

    @property
    def ime( az): return az.etiketi.get( az.stoinosti.ime, '??')
    @property
    def imeto( az): return az.etiketi.ime


    vse             = dict_lower()  # { fname: info }
    vse_prevodi     = dict_lower()  # { fname: ime/orig/grupa/fname }
    meta_prevodi    = dict_lower()  # { lat: cyr }

    @classmethod
    def unicode_fname( klas, n):
        if not isinstance(n, unicode): n = n.decode( klas.fenc)
        return n


    def __init__( az, fname, redove =None, origfname =None, isdir =True):
        az._init()
        fname = az.unicode_fname( fname)
        az.fname = fname
        az.isdir = isdir
        az.origfname = origfname or fname
        az.vse[ fname ] = az
        az.imena = dictOrder()  #ezik:ime
        az.etiketi          = az.DictAttrTrans()
        az.etiketi_papka    = az.DictAttrTrans()
        az.etiketi_element  = az.DictAttrTrans()
        az.papka_etiketi    = Naslagvane( (az.etiketi_papka, az.etiketi), bool= True)
        az.element_etiketi  = Naslagvane( (az.etiketi_element, az.etiketi), bool= True)
        az.prevodi = dictOrder_lower()  #fname:(ime,grupa,orig)
        az.grupi   = []                 #група/име,допиме,дългоиме,преводи
        az.redove  = []
        az.komentari= []
        if redove is not None:
            try:
                redove = list( eutf.readlines( redove))
                az.procheti( redove)
            except:
                print( '????', fname)
                raise

    @classmethod
    def DictAttrTrans( az):
        return _DictAttrTrans( _prevodach= az.stoinosti)

    class Prevod( _DictAttrTrans):
        _vytr_svoistva = 'fname grupa roditel uchastnici_vse'.split()
        #_bez_prevod = DictAttrTrans._bez_prevod | set( _vytr_svoistva)

    @classmethod
    def _nov_prevod( klas, *, fname, ime, original =None, grupa =None, roditel =None, **etiketi):
        p = klas.Prevod( fname= fname,
                grupa= grupa, roditel= roditel,
                _prevodach = klas.stoinosti)

        p.etiketi = klas.DictAttrTrans()
        for k in (etiketi.pop( 'simvoli', '') or '').strip().split():
            klas._slaga_etiket( k, True, p.etiketi)

        p.update_pre( ime= zaglavie( ime), original= original, **etiketi)
        for k in list( p.keys()):
            klas.ime2imena( k, p)

        if grupa is not None: grupa.elementi.append( p)

        q = klas.vse_prevodi.get( fname)
        if not q:
            klas.vse_prevodi[ fname] = p
        elif q.ime != ime:
            err( 'повтаря се/все:', fname, '\n', roditel, ':', ime, '\n', q.roditel, ':', q.ime)

        return p

    def nov_prevod( az, *a,**k):
        p = az._nov_prevod( *a,**k)
        az.prevodi[ p.fname] = p
        return p

    def nova_grupa( az, kyso, dylgo, dop):
        kyso = zaglavie( kyso)
        if dop:
            assert kyso
            assert not dylgo
            dylgo = kyso + ' ' + dop
        elif not dylgo: dylgo = kyso
        elif not kyso: kyso = dylgo
        dylgo = zaglavie( dylgo)
        igrupa = DictAttr( ime= dylgo, kyso= kyso, dop= dop, elementi= [] )
        az.grupi.append( igrupa)
        return igrupa

    def __str__( az):
        r = [ az.fname ]
        if az.etiketi.papka: r+= [ 'e_PAPKA' ]
        r+= [ 'ime= ' + az.ime]
        return '\t'.join( r)

    def dump( az):
        r = [ az.fname ]
        if az.etiketi.papka: r+= [ 'e_PAPKA' ]
        r+= [ 'ime= ' + az.ime]
        etiketi = [ k for k in sorted( az.etiketi) if k not in az.izvyn_etiketi]
        if etiketi:
            r+= [ 'etiketi:']
            r+= [ '  %s = %s' % (k,az.etiketi[k]) for k in etiketi]
        if az.prevodi:
            r+= [ 'prevodi:'+str(len(az.prevodi))]
        return '\n   '.join( r)

    class infof( DictAttr):
        def __getattr__( az, k): return ''

    _shabloni = {}
    def _po_shablon( az, shablon, **etiketi):
        if not shablon: return
        eti = az.infof( az.etiketi ) #.copy()
        eti.update( etiketi)
        for k,v in list( eti.items()):     #+varianti
            k = az.stoinosti.get(k)
            if not k: continue
            for kk in az.stoinosti_imena.get( k, ()):
                assert eti.get( kk) in (None, v)
                eti[ kk ] = v
        ops = { 'и':i, 'или':ili, 'в':vyv, 'ако':ako, 'не': ne, 'залепи': joinif }
        #shablon.startswith( 'израз '):
        ss = shablon.split(':',1)
        assert len( ss)==2 and len( ss[0].strip().split())==1 and len( ss[0].split(','))==1
        f = az._shabloni.get( shablon)
        if not f:
            f = az._shabloni[ shablon] = eval( 'lambda '+shablon, ops)
        try:
            return f( eti ).strip()
        except Exception as e: #KeyError as e:
            err( '??????????', e.__class__.__name__, e.args[0], eti)
            raise

    def ime_po_shablon( az, **etiketi):
        try:
            return az._po_shablon(
                    shablon= az.nasledstvo.get( az.stoinosti.shablon),
                    **etiketi) or az.ime
        except:
            err( az.dump())
            raise

    def prevod_po_shablon( az, element, **etiketi):
        p = az.prevodi.get( element, az.vse_prevodi.get( element))
        if p:
            prevod = p.ime
            grupa = p.grupa
        else:
            prevod = element
            grupa = None
        etiketi[ az.stoinosti.element] = prevod
        if grupa:
            gelementi = grupa.elementi
            if len( gelementi) ==1: n = ''
            else:
                n = str( gelementi.index( p)+1)
                n = n.zfill( len( str( len( gelementi))))
            g = grupa.kyso
        else: n = g = ''
        etiketi[ az.stoinosti.nomervgrupa] = n
        etiketi[ az.stoinosti.grupa] = g
        gn = g+':'
        if n: gn += n+'.'
        etiketi[ az.stoinosti.grupa_i_nomer] = gn
        try:
            r = az._po_shablon(
                    shablon= az.etiketi.shablon_element or az.nasledstvo.get( az.stoinosti.shablon_element),
                    **etiketi) or prevod.format( **etiketi)
            r = r.rstrip( ':')
            return r
        except:
            err( element + ': '+ az.dump())
            raise

    @property
    def nasledstvo( az):
        adres = az.fname
        roditeli = []
        while True:
            if not adres: break
            adres = adres.rstrip( '/')
            adres = dirname( adres)
            if not adres: break
            if adres in az.vse: roditeli.append( az.vse[ adres] )
        roditeli.reverse()
        etiketi = {}
        for i in roditeli:
            etiketi.update( (k,i.etiketi[k]) for k in az.nasledimi if k in i.etiketi)
        return etiketi

    def danni( az):
        #dd = dictOrder()
        #d = attr2item( dd)
        d = DictAttr()

        d.ime   = az.ime    #''
        d.imena = az.imena  #{ lang:''}

        #общ речник с обхват:стойност
        dt = {}
        for k,v in az.etiketi.items():
            dt[k] = { '': v}
        for k,v in az.etiketi_papka.items():
            dt.setdefault( k, {})[ 'papka'] = v
        for k,v in az.etiketi_element.items():
            dt.setdefault( k, {})[ 'element'] = v

        #разделяне по обхвати: за-всички, един,друг,..
        detiketi = {}
        for k,vv in dt.items():
            vvv = list( vv.values())
            if len(vv)>1 and all( vvv[0]== vi for vi in vvv[1:]):
                detiketi.setdefault( '',{})[k] = vvv[0]
                continue
            for obhvat,v in vv.items():
                detiketi.setdefault( obhvat,{})[k] = v

        #разделяне по вид стойност - bool или не
        d.etiketi = {}
        for obhvat, et in detiketi.items():
            d.etiketi[ (obhvat, True) ] = e1 = [] #[ k ]
            d.etiketi[ (obhvat, False)] = e2 = [] #[ (k,v) ]
            for k,v in sorted( et.items()):
                if k in az.izvyn_etiketi: continue
                if v is True: e1.append( k )
                else: e2.append( (k,v) )
                #elif not isinstance( v, str): e2.append( (k,v) )
                #else: e2.append( (k,v.splitlines()))

        d.prevodi = ()  #[ (file,prev,org) ] извън групи
        d.grupi = []    #[ { дългоиме или дългоиме,късоиме или късоиме,допиме , [ (file,prev,org) ] } ]
        if az.prevodi:
            pr = [ p for p in az.prevodi.values() if not p.grupa ]
            sort_prevodi = az.options.sort_prevodi or az.etiketi.sort_prevodi
            if sort_prevodi: pr = sorted( pr, key= lambda p: p.fname)
            d.prevodi = pr

            gr = az.grupi
            if sort_prevodi: gr = sorted( gr, key= lambda g:g.ime)
            d.grupi = gr

        d.komentari = az.komentari  #['']
        return d

    def _zapis( az, r, org, naistina =False, ext =''):
        if not az.isdir: fname = az.fname +ext
        else:
            fname = join( az.fname, OPIS)
        #if not fname.endswith( ext): fname += ext
        return save_if_diff( fname, r, naistina=naistina)

    re_godina = re.compile( r' *[-._(]+?(\d{4})\)?$')
    def samopopylva_ot_fname( az):
        fn = basename( az.fname).lower()
        if not az.etiketi.zvuk:
            exs = fn.split('.')
            if len(exs)>1:
                for ex in reversed( exs):
                    if ex in az.ezici:
                        az.slaga_etiket( az.stoinosti.zvuk, az.zamestiteli_po_stoinost.zvuk[ ex ])
                        break

        m = az.re_godina.search( fn)
        if m:
            az.slaga_etiket( az.stoinosti.godina, m.group(1))
            #fn = fn[:m.start(0)]

    def samopopylva_etiketi( az):
        pass

    exts = 'mkv avi mov wmv webm mpg mpeg mp4 ts m2ts flv  mp3 wma flac wav ac3 ogg'.split()
    @classmethod
    def bez_ext( az, fname, exts= (), extra_exts =(), samo1 =False):
        exts = set( exts or az.exts)
        exts.update( extra_exts)
        while 1:
            kk,ext = os.path.splitext( fname)
            if not ext or ext[1:] not in exts: break
            fname = kk.rstrip( '.')
            if samo1: break
        return fname

    @classmethod
    def bez_ext1x1( az, fname, exts= (), extra_exts =()):
        r = [ fname ]
        while 1:
            fname = az.bez_ext( fname, exts, extra_exts, samo1= True)
            if fname == r[-1]: break
            r.append( fname)
        return r

    vse_file_prevodi     = dict_lower()  # { fname: ime/orig/grupa/fname }
    def prevedi_elementi( az):
        r = az.file_prevodi = {}
        k = az.fname
        k = globescape( k)
        for ext in az.exts:
            #така че АБ.В.Г минава преди АБ.В XXX по-дългите първи щото иначе а-б.avi не минава преди а.avi
            for f in reversed( sorted(
                        glob( k+'/*.'+ext)
                        + glob( k+'/*/*.'+ext)     #./grupa1/file1
                        , key= lambda x: (len(x),x) )
                    ):
                az.prevedi_element( f )

        if az.options.podrobno and r:
            prn( '---------file_prevodi-----')
            prn( '\n'.join( '%-50s = %s' % (k,v) for k,v in sorted( r.items())))

    svoistva_ot_fname__shabloni= [ re_godina ]  #всички
    svoistva_ot_fname__red = ()     #само тези се запазват, в този ред

    def svoistva_ot_fname( az, aname):
        red_svoistva_ot_fname = az.svoistva_ot_fname__red or az.svoistva_ot_fname__shabloni
        r = len( red_svoistva_ot_fname) * [ None ]
        for rre in az.svoistva_ot_fname__shabloni:
            try: ix = red_svoistva_ot_fname.index( rre )
            except ValueError: ix = None
            if ix is not None:
                for x in rre.finditer( aname):
                    r[ ix ] = x.group(1)        #вземи последното
                    #if SAMO_PYRVOTO: break
            aname = rre.sub( '', aname)
        return [x for x in r if x], aname

    def prevedi_element( az, f ):
        k = az.fname

        assert isinstance( f, unicode)
        fpath,fname = os.path.split( f)
        if fpath != k:
            if exists( join( fpath, OPIS)):
                return
            fname = f[ len(k):].lstrip('/')

        if az.e_za_propuskane( dirname( fname) ):
            return

        svoistva = ()
        aname = None
        for ime_bez_ext in az.bez_ext1x1( fname):
            if ime_bez_ext in info.vse_prevodi:
                break
        else:
            svoistva,aname = az.svoistva_ot_fname( ime_bez_ext)
            aname = aname.rstrip('.')
            if aname not in info.vse_prevodi:
                for aname in az.bez_ext1x1( aname):
                    if aname in info.vse_prevodi:
                        break
                else:
                    if az.etiketi.sfx and aname.endswith( az.etiketi.sfx):
                        aname = aname[ :-len(az.etiketi.sfx)]
                        if aname not in info.vse_prevodi:
                            if az.options.podrobno: prn( '!!! няма превод:', f, aname)
                            return

        prevod = az.prevod_po_shablon( aname or ime_bez_ext)
        if svoistva: prevod = '.'.join( [prevod] + svoistva )


        oname = join( k, ime_bez_ext)
        lodir = len(k)+1
        loname= len(oname)
        assert isinstance( oname, unicode), repr(oname)
        for s in sorted( glob( globescape( oname)+'*')):
            staro = s[ lodir:]
            kk,ext = os.path.splitext( staro)
            if fname.startswith( kk):
                novo = prevod + ext
            else:
                #това се скапва за приказка с :автор
                novo  = prevod+ s[ loname:]
            assert isinstance( novo, unicode), repr(novo)
            if staro == novo: novo = None
            if staro not in az.file_prevodi:
                az.file_prevodi[ staro ] = novo     #АБ.В.Г е вече там когато минава през АБ.В
            if not az.vse_file_prevodi.get( staro) and novo:
                az.vse_file_prevodi[ staro ] = novo



    @staticmethod
    def fix_std_encoding():
        eutf.fix_std_encoding()

    @classmethod
    def obikoli( klas, paths, e_za_propuskane =None):
        for aa in paths:
            a = realpath( aa)
            klas.options.dirs.append( a)
            for path,dirs,files in os.walk( a, followlinks= klas.options.simvolni):
                if e_za_propuskane and e_za_propuskane( path):
                    dirs[:] = []
                    continue
                dirs[:] = [ d for d in dirs if not (e_za_propuskane and e_za_propuskane( d)) ]
                yield path, dirs, files

    @classmethod
    def zaredi_danni( klas, args):
        ''' - прочита всички описи
            - при преводи, обикаля всички директории и запомня кои имат преводи
              - тези от тях които нямат описи, им се правят нови
            - за всички описи
              - ако нямат име, се слага от преводи ако има
              - самопопълва звук/година от името-на-директорията
              - добавя поисканите етикети
        '''
        options = klas.options

        #################
        #зареждане на данни, заявки, и пр. - четене/оправяне на ОПИСИте

        if options.prevodi:
            if options.podrobno: prn( 'prevodi:', options.prevodi)
            for k,(v,o) in prevodi_file2ime( eutf.readlines( options.prevodi)):
                klas._nov_prevod( fname= k, ime= zaglavie(v), original= zaglavie(o), roditel= options.prevodi)
                if options.podrobno: prn( '%-40s = %s' % (k,v) )

        if options.prevodi_meta:
            info.meta_prevodi.update( meta_prevodi( options.prevodi_meta, dict= dict_lower,
                        prn= options.podrobno and prn, zaglavie= 'мета-преводи', razdelitel_v_nachaloto=True
                        ))

        info.fenc = options.filename_enc or (eutf.e_utf_stdout() and 'utf-8' or locale.getpreferredencoding())
        if options.podrobno:
            prn( 'filename_enc:', info.fenc)
            prn( 'stdout.enc:', sys.stdout.encoding, sys.stdout)
            prn( 'stderr.enc:', sys.stderr.encoding, sys.stderr)

        etiketi = {}
        for e in options.etiket or ():
            klas.procheti_etiket( e, etiketi)

        options.dirs = []
        za_pravene = {}
        for path,dirs,files in klas.obikoli( args, klas.e_za_propuskane ):
            if options.prevodi:
                for dname in dirs:
                    pname = join( path, dname)
                    if not options.simvolni and os.path.islink( pname): continue
                    p = klas.vse_prevodi.get( dname)
                    if p:
                        rpname = realpath( pname)
                        za_pravene[ rpname] = p.ime, pname

            pname = realpath( path)
            for fname in files:
                if not e_opis( fname): continue
                i = klas( pname, redove= join( path, fname), origfname= path)
                if options.podrobno: prn( i.fname)
                if options.podrobno>1: prn( i.dump() )

        for path,dirs,files in klas.obikoli( options.papka_s_opisi or () ):
            pname = realpath( path)
            for fname in files:
                if klas.e_za_propuskane( fname): continue
                i = klas( join( pname, fname), redove= join( path, fname), origfname= join( path, fname), isdir=False)
                if options.podrobno: prn( i.fname)

        for pname,(ime,fpath) in za_pravene.items():
            if pname not in info.vse:
                i = klas( pname)
                i.slaga_ime( ime)

        for k,i in sorted( info.vse.items()):
            try:
                i.samopopylva_ot_fname()
                fname = basename( i.fname)
                p = klas.vse_prevodi.get( fname)
                if p:
                    if not i.imeto or options.popravi_opisi:
                        i.slaga_ime( p.ime)
                    if p.original and not i.etiketi.original:
                        i.slaga_etiket( i.stoinosti.original, p.original )

                i.etiketi.update_pre( **etiketi)
                i.samopopylva_etiketi()
                razlika, t = i.zapis( naistina= options.zapis_opisi )
                #if razlika: print( '-----------')
            except:
                print( '????', fname)
                raise

    @classmethod
    def e_za_propuskane( klas, fn):
        fn = basename( fn)
        if klas.options.samo:
            if not fnmatch_list( fn, klas.options.samo):
                return True
        return fnmatch_list( fn, klas.options.bez)

    #TODO ioformat
    @classmethod
    def procheti_etiket( az, red, rechnik):
        if ':' in red:
            k,v = [ x.strip() for x in red.split(':',1)]
            az._slaga_etiket( k,v,rechnik, zamesti= False )
        else:
            rechnik.update( (k.lower(),True) for k in red.split() )

    @classmethod
    def main( klas, optz2 =None, args2 =None):
        klas.fix_std_encoding()
        klas._init()
        klas.opts()
        if optz2 or args2:
            options,args = optz.oparser.parse_args( args2 or ())
            if optz2: options._update_loose( optz2)
        else:
            options,args = optz.get()

        for o in optz.iter_opt_defs():
            if o.action != 'append': continue
            k = o.dest
            #uniq
            setattr( options, k,
                listif( p.strip() for p in (getattr( options, k) or ()) ))

        if options.opisi:
            OPISIpat[:] = options.opisi
        global use_stderr
        if options.stderr: use_stderr = True

        info.options = options
        info.args = args
        klas.zaredi_danni( args)
        info.vse_prefix      = commonprefix( [ dirname( i.fname)     for i in info.vse.values() ]) #_real
        info.vse_prefix_orig = commonprefix( [ dirname( i.origfname) for i in info.vse.values() ])

        klas.all()

    @classmethod
    def all( klas):
        #използване на ОПИСИте за преименоване/прегрупиране
        if klas.options.preimenovai_papki:
            klas.preimenovai_papki()
        elif klas.options.prehvyrli_papki is not None:
            klas.prehvyrli_papki( klas.args)


    @classmethod
    def ime_filter( klas, f, *ctx):
        if not klas.options.ntfs: return noslash( f, *ctx)
        return ntfs_fname_filter( f, context= ctx, repl= {'"':"'", '*':'+', '?':'?', None:'-'} )

    @classmethod
    def preimenovai_papki( klas):
        for k,i in sorted( info.vse.items()):
            i.prevedi_elementi()

        ime_filter = klas.ime_filter
        spisyk = []
        for k,i in sorted( info.vse.items()):
            spisyk += [ (join( k,o), join( k, ime_filter(n, k,o)) )
                        for o,n in i.file_prevodi.items() if n ]
            #след вътрешностите
            fpath,fname = os.path.split( k)
            spisyk.append( (k, join( fpath, ime_filter( i.ime_po_shablon(), k) )))

        for k,v in reversed( sorted( spisyk)):
            pfx = commonprefix( (k,v))
            prn( '%-60s -> %s' % (k,v[len(pfx):]))
            if klas.options.davai:
                os.rename( k,v)

    @classmethod
    def prehvyrli_papki( klas, args):
        options = klas.options
        kyde = options.prehvyrli_papki or 'KYDE'
        davai = options.davai and options.prehvyrli_papki

        for k,i in sorted( info.vse.items()):
            i.prevedi_elementi()

        if options.podrobno: prn( '==>', kyde)

        def prevodach( orig, novo, elementi):
            'return prevedeno novo, prevedeni elementi'
            rorig = realpath( orig)
            i = info.vse.get( rorig)
            fpath,fname = os.path.split( novo)
            if i is None:
                rnovo = join( fpath, klas.ime_filter( fname))
                return rnovo, () #няма info/превод
            #elif rorig == orig:
            #    rnovo = None #пропусни самите info-та
            else:
                rnovo = join( fpath, klas.ime_filter( i.ime_po_shablon( **{ info.stoinosti.pyt: fpath} )) )
            rimena = {}
            for n in elementi:
                #if join( orig, n) in info.vse:
                #    continue    #пропусни info-та
                rimena[ n] = klas.ime_filter( i.file_prevodi.get( n) or klas.vse_file_prevodi.get( n) or n)

            return rnovo, rimena

        from shutil import Error
        def linktree( src, dst, symlink =False, error_immediately =True, fake =False, translator =None, _root =True):
            'Recursively link a directory tree, e.g. cp -rl or cp -rs. symlinks are dereferenced'
            link = symlink and os.symlink or os.link
            src = info.unicode_fname( src)
            names = [ e for e in os.listdir( src) if not klas.e_za_propuskane( e)]
            rnames = ()
            if translator:
                rdst,rnames = translator( src, dst, names)  #rnames: only those to copy
                if not _root:
                    if rdst is None: return  #ignore whole
                dst = rdst

            pfx = fake and '?' or ''
            def dali( src, dst, what, condition):
                if condition or options.podrobno:
                    if src.startswith( info.vse_prefix): src = '$/'+src[len(info.vse_prefix):]
                    prn( pfx+ what, src)
                    prn( pfx+ '=>'.rjust(len(what)), '@'+dst[len(kyde):] )
                return not fake and condition

            if dali( src, dst, 'linktree'+ (_root and '/R' or ''), not isdir( dst)):
                os.makedirs( dst, exist_ok=True)
                stat = os.stat( src)
                tms =  stat.st_atime, stat.st_mtime
                os.utime( dst, tms)

            errors = []
            for name in names:
                if rnames and name not in rnames: continue
                srcname = os.path.join( src, name)
                dstname = os.path.join( dst, rnames and rnames[ name] or name)
                try:
                    #if os.path.islink( srcname):
                    #    linkto = os.readlink( srcname)
                    #    if dali( linkto, dstname, 'slink', not os.path.islink( dstname)):
                    #        os.symlink( linkto, dstname)
                    #el
                    if isdir( srcname):
                        linktree( srcname, dstname, symlink=symlink, error_immediately=error_immediately, fake=fake, translator=translator, _root= False)
                    elif dali( srcname, dstname, 'link', not exists( dstname)):
                        srcname = realpath( srcname)
                        link( srcname, dstname)

                except (IOError, os.error) as why:
                    err( srcname, dstname)
                    if error_immediately: raise
                    errors.append((srcname, dstname, str(why)))
                # catch the Error from the recursive copytree and continue
                except Error as er:
                    errors.extend( er.args[0])
            if errors:
                raise Error( errors)

        for a in args:
            a = realpath( a)
            linktree( a, join( kyde, basename( a)), symlink= options.prehvyrli_simvolno, fake= not davai, translator= prevodach)


    def procheti( az, redove):
        if io_yaml.opis_io.otgatni( az, redove):
            io = io_yaml
        else: io = io_moi
        return io.opis_io.procheti( az, redove)

    def zapis( az, **kargs):
        if not az.options.noyaml or OPIS.endswith( '.yaml'):
            io = io_yaml
        else: io = io_moi
        return io.opis_io.zapis( az, **kargs)

import io_moi
import io_yaml

def pokazhi_imena_po_shablon():
    'plosko'
    for k,i in sorted( info.vse.items()):
        prn( k, '\t\t', i.ime_po_shablon())

def vse_etiketi( klas):    # { etiket: { stoinost:[info] }
    r = {}
    for i in klas.vse.values():
        for k,v in i.etiketi.items():
            #if k in klas.stoinosti.values(): continue  ???
            r.setdefault( k, {} ).setdefault( v, []).append( i)
    return r

def pokazhi_grupirane_po_etiketi():
    #etiket : imena
    for e,vi in sorted( vse_etiketi( info).items() ):
        for v,ii in sorted( vi.items() ):
            all = '; '.join( i.ime_po_shablon( **{e:None} ) for i in ii)
            prn( e+(v is not True and '/'+v or ''), ':', all)

if __name__ == '__main__':
    info.main()

# vim:ts=4:sw=4:expandtab

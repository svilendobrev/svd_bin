#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import latcyr_ednakvi

#lats = dict.fromkeys( chr(x),x for x in range( ord('A'),ord('Z')+1))
_kiri = dict.fromkeys( ord(y) for x,y in latcyr_ednakvi.lc2 )
def ima_kir(t): return len( t.translate( _kiri)) != len(t)
_tablica = latcyr_ednakvi.lc1 + latcyr_ednakvi.i_drugi

def razdeli_kamila( t):
    t = latcyr_ednakvi.lc_subst( t, _tablica if ima_kir(t) else latcyr_ednakvi.i_drugi)
    assert ' ' not in t, t
    r = ['']
    u = None
    for c in t:
        if c in '_.':       #е прекъсване
            if c == '.': r[-1] += c
            if r[-1]:       #ако не е вече прекъснато
                r.append( '')
                u = None
            continue
        if c == '-':        #не е прекъсване
            u = cu = None
        else:
            cu = True if c.isupper() else False if c.islower() else None
        if u is not None:
            if not u and cu:    #малки->големи е прекъсване
                r.append( '')
        u = cu
        r[-1] += c
    if not r[-1]: r.pop(-1)
    return r

def razdeli_kamila2_( t):
    return '_'.join( razdeli_kamila(t) )

def razdeli_kamila2( t):
    r = ' '.join( razdeli_kamila( t))
    r = r.replace( '- ','-')
    r = r.replace( '_ ',' ')
    r = r.replace( '_',' ')
    #r = r.replace( '. ','.')
    return r

glasni0 = 'аъоуеи'
glasni = glasni0+'юяй'
glasni += 'ь'  #избегни Маргь-орит, Пь-отр

import itertools
def powerset( iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = tuple( iterable)
    return itertools.chain.from_iterable( itertools.combinations( s, r) for r in range(len(s)+1))


def sykrashtenia( t, samo_pred_glasna_sled_syglasna =False, ako_pochva_s_glasna =False, min_ostatyk =2, vse =True, bez_lipsi =False, dbg =0):
    imena = razdeli_kamila(t)
    ime = imena[0]

    if (len(imena)==1           #Нещо
        or len(imena)==2 and ime.endswith('-')    #заю-баю
        #or '_' in t         #хор_Някакъв    ?
        #or ime.islower()       #хорНякакъв    #XXX слабо
        #or len(ime)<=2         #ИвМонтан ХюЛофтинг
        ):
        return [ '' ] #t

    if imena[-2].endswith('-'):
        imena[-2] += imena[-1]
        del imena[-1]

    imena = tuple( imena)
    sykr = []
    for ime in imena[:-1]:
        im = bukva = ime[0]
        bukva_e_glasna = bukva.lower() in glasni0
        spisyk = [ im +'.' ]    #Х. /Петров
        spisyk2 = []            #Хри. /Петров

        dylgo = len(ime)>3
        if dylgo:
            skyseno = False
            for b in ime[1:]:
                im += b
                ostatyk = len(ime)-len(im)
                if not vse and min_ostatyk > ostatyk: break
                if b in glasni:
                    if samo_pred_glasna_sled_syglasna:
                        if not skyseno and not ako_pochva_s_glasna or bukva_e_glasna:
                            #if len(im)>=2 and 'ь' == im[-2]: #Пь - избегни
                            #    pass #print( 7775, spisyk )
                            #else:
                                spisyk = spisyk[-1:]    #poslednoto e hubavoto
                                skyseno = True
                    if not vse: break
                if not dylgo or b in glasni or min_ostatyk > ostatyk and not (len(ime)==4 and ostatyk==2):
                    ss = spisyk2
                else:
                    ss = spisyk
                ss.append( im +'.' )   #Хр.Петров Андр.Ангелов
        else:
            spisyk2.append( ime +'.' ) #Ива.Петрова - но без Ив.Петрова

        spisyk.insert( 0, ime)  #цялото
        sykr.append( (spisyk, spisyk2) )

    # всякакви комбини и междинни липси, Ернст_Теодор_Амадеус_Хофман Ернст_Т.Амад.Хофман Е.Т.А.Хофман Ерн.Ам.Хофман .. Е.Хофман
    spisyk = list( itertools.product( *(s for s,s2 in sykr ) ))
    spisyci = [spisyk]
    if vse:
        spisyk2= [ x for x in itertools.product( *(s+s2 for s,s2 in sykr ) ) if x not in set( spisyk) ]
        spisyci.append( spisyk2)
    if not bez_lipsi:
        for ss in spisyci:
            spis_lipsi = set()
            for s in ss:
                spis_lipsi.update( s[:1]+x for x in powerset( s[1:] ))
            spis_lipsi.difference_update( spisyk)
            ss += spis_lipsi

    spisyk.remove( imena[:-1] )  #цялото име
    spisyk = [ '_'.join( x+ imena[-1:] ) for x in spisyk]
    assert spisyk, ime
    if not vse: return spisyk

    spisyk2= [ '_'.join( x+ imena[-1:] ) for x in spisyk2]
    if dbg:
        for s in spisyk,spisyk2:
            print( *[ x.replace('._','.') for x in s])
    return spisyk, spisyk2

from svd_util.dicts import dict_lower

class set_lower( dict_lower):
    'keeping original (first-time) inputs, and (order of) 1st+2nd entry'
    first = None
    second= None
    def __init__( me, xx =()):
        dict_lower.__init__( me)
        me.update( xx)
    def update( me, xx):
        xx = tuple( xx) #copy
        sz = len(me)
        if xx and not me:
            me.first = xx[0] if not isinstance( xx[0], (tuple,list)) else xx[0][-1]
        dict_lower.update( me, ( ((k,k) if not isinstance( xx[0], (tuple,list)) else k) for k in xx))
            #XXX above may overwrite original inputs
        if me.second is None and  sz < len(me) >= 2:   #changed
            first = me[ me.first ]
            for x in xx:
                v = x if not isinstance( x, (tuple,list)) else x[-1]
                if me[ v ] is not first:
                    me.second = v
                    break
    def add( me, x):
        if not me: me.first = x
        elif x in me: return    #dont overwrite original input !
        second = len(me)==1
        me[x] = x
        if second: me.second = x
    #def __getstate__( me): return tuple( me.values() )
    #__setstate__ = update

class Abbr:
    dbg=0
    def __init__( az, avto_sykrashtenia =False):
        az.imena = dict_lower()     #име : set_lower[име + всички варианти]    впоследствие тези които са измислими, се махат?
        az.rychni= dict_lower()     #съкр: [имена] ; ръчно сложени, имат превес над автоматични ; възможна е многозначност!
        az.avto = dict_lower()      #съкр: [имена] ; автоматични, по-старите имат превес
        az.avto2= dict_lower()      #съкр: [имена] ; автоматични, невалидни
        az.komentari = []
        az.komentari_po_ime = dict_lower()

    def _eto_ime( az, ime, neime =False):
        znaini = az.imena.get( ime)
        if znaini is None:
            znaini = az.imena[ ime] = set_lower([ ime ])
            znaini.neime = bool( neime)
        elif neime is not None:                                         #първия печели, другите следват
            assert neime is znaini.neime, (ime, neime, znaini.neime)
        return znaini

    def eto_imena( az, ime, *varianti):   #ръчни
        'нарочно не попълва автоматичните/eto_imepylno - отлагат се за след всички ръчни'
        ime = ime.strip()
        varianti = [ v.strip() for v in varianti ]
        neime = ime.startswith('_')     #_Сатиричен_театър _хор_Бодра_смяна _Софийски_камерен_хор
        ime = razdeli_kamila2_( ime)
        znaini = az._eto_ime( ime, neime)
        dbg = az.dbg
        for v in varianti:
            v = razdeli_kamila2_( v)
            if v in znaini: continue
            znaini.add( v)
            rychni = az.rychni.setdefault( v, set() )
            if dbg: print( 3331, 'ръчно', ime, ':', v, *sorted(rychni))
            rychni.add( ime )
            #if dbg and
            if len(rychni)>1:
                print( 3334, '!ръчно многозначни', ime, ':', v, *sorted(rychni))     #assert?
        return ime

    def eto_imepylno( az, ime, ime_za_sykr ='', neime =None, dbg=0):    #закача съкращенията на име-за-съкр към име
        ime = ime.strip()
        #neime = ime.startswith('_')
        ime = '_'.join( ime.split())    #XXX
        ime = razdeli_kamila2_( ime)
        ime_za_sykr = ime_za_sykr.strip() or ime
        if ' ' in ime_za_sykr: return True  #XXX ?
        znaini = az._eto_ime( ime, neime)
        neime = znaini.neime
        dbg = dbg or az.dbg
        validni = []
        sdylgo = set([ ime ])
        #TODO това ще се счупи / стане многозначно ако се пусне с ЕдноДве и едноДве .. ???
        sp = sykrashtenia( ime_za_sykr, vse= True, bez_lipsi= neime)
        sp2= []
        if len(sp)>1: sp,sp2 = sp
        if dbg: print( 5550, ime_za_sykr, ':', sp, sp2)
        for ss,azavto in [[sp,az.avto], [sp2,az.avto2]]:
          for s in ss:
            if not s or '.' not in s and '_' not in s: return True    #несъкратимо
            avto = azavto.setdefault( s, [] )
            if dbg: print( 5551, ime, s, avto)
            if avto and ime in set_lower( avto):    #set_lower: да не стане многозначно при ЕдноДве и едноДве ..
                continue      #вече е там ..
            rychni = az.rychni.get( s, ())
            if dbg: print( 5552, ime, s, avto, rychni)
            #if s in sp2: nevalidni.append( s)
            if azavto is az.avto and not avto and (not rychni or rychni == sdylgo):
                validni.append( s)
            elif dbg:
                ss = (set(avto) | set(rychni)) - sdylgo
                if ss: print( 5553, 'автоматично но многозначно', s, ime, ime_za_sykr, ':', sorted(ss))
            avto.append( ime)

        if dbg and validni: print( 5554, 'автоматични', ime, ':', *sorted(validni))
        znaini.update( validni)
        if dbg: print( 55555, *az.imena[ ime].values())

    def dai_imepylno( az, kyso):
        kyso = '_'.join( kyso.split())  #XXX
        kyso = razdeli_kamila2_( kyso)
        r = az.rychni.get( kyso) or az.avto.get( kyso) or az.avto2.get( kyso) or ()
        return tuple(r)[0] if r else getattr( az.imena.get( kyso), 'first', None)

    def dai_kyso( az, ime, original =False, dbg =False, min =False, vse =False):
        ime = razdeli_kamila2_( ime)
        ime0 = az.dai_imepylno( ime) or ime #АсенКисимов -> АсенАнгелов -> ..
        r = az.imena.get( ime0)
        dbg = dbg or az.dbg
        if dbg: print( 666, ime, ime0, r)
        if not r: return r  #несъкратимо или съкращението заето
        if not original: ime = ime0     #XXX за кво ми е трябвало original=True?? не се ползва

        #най-късото валидно за име0 (АсенАнгелов) И направено от име (А.Кисимов) И валидно за оригинала
        ss = list( sykrashtenia( ime, samo_pred_glasna_sled_syglasna= not min, vse= vse, bez_lipsi= r.neime ))   #??? XXX бавно?
        r = sorted( r.values(), key= lambda x: (len(x),x) )  #азбучно при еднаква дължина
        if ss:
            for x in r:
                if x in ss:
                    return x
        return r[0] #най-късото

    def mnogoznachni( az):
        return dict( (k,v) for k,v in az.rychni.items() if len(v)>1 )

    def popylni_avto( az):
        for i in az.imena.values():
            ime,neime = i.first,i.neime
            az.eto_imepylno( ime, neime= neime )
            for v in list( i.values()):
                if '.' not in v and v != ime:
                    az.eto_imepylno( ime, v, neime= neime )

    def mahni_izmislimi( az):
        izmislimi = []
        dbg = az.dbg
        for s,imena in sorted( az.rychni.items()):
            ravni = imena == set( az.avto.get(s) or ())
            if dbg: print( 11100, s, ravni, imena, az.avto.get( s) )
            if len(imena)>1:
                if dbg: print( 11101, s, 'ccccccccyk', len(imena))      #няколко правила за едно и съшо?
                continue
            if ravni:
                izmislimi.append( s)
        if dbg:
            print( 11111, len(izmislimi), *izmislimi)
            print( 11112, len( az.rychni))
        for s in izmislimi: del az.rychni[s]
        if dbg:
            print( 11113, len( az.rychni), az.rychni)
            for i in az.imena.values():
                print( 11114, *i.values())

    def cheti_eutf( az, fl, **ka):
        from svd_util import eutf
        vid = None

        REDIS = 'http://localhost:6379/9'
        if 0*REDIS:
            import redis
            #   redis://[:password]@localhost:6379/0
            #   unix://[:password]@/path/to/socket.sock?db=0
            rd = redis.Redis.from_url( REDIS) #Redis(host='localhost', port=6379, db=0)
            _dbname = 'abbr'
            if not rd.dbsize():
                rd[ '_dbname'] = _dbname
            else:
                dbname = rd.get( '_dbname')
                if dbname is not None: dbname = dbname.decode( 'utf8')
                assert dbname == _dbname, dbname
            vid = 'redis'

        import pickle
        import os.path
        try:
            fpikle = fl+'.pikle'
            if os.path.getmtime( fpikle) > os.path.getmtime( fl):
                cache = pickle.load( open( fl+'.pikle', 'rb'))
                for k in az._cache:
                    v = cache[ k]
                    if isinstance( v, list): upd = setattr( az, k, v)
                    else: getattr( az, k).update( v)
                vid = 'pikle'
        except:
            #try:
            #    cache = eval( open( fl+'.cache').read(), dict( set_lower= set_lower, dict_lower= dict_lower, dict= dict))
            #    for k in az._cache: setattr( az, k, cache[k])
            #    vid = 'pprint'
            #except:
            #    pass
            pass
        if not vid:
            print( 'abbr=', fl)
            az.cheti( eutf.readlines( fl), **ka)

        az.cache( fl, vid)

    _cache = 'imena rychni avto avto2 komentari komentari_po_ime'.split()
    def cache( az, fl, vid =None):
        r = dict()
        for k in az._cache:
            v = getattr(az,k)
            if isinstance( v, dict_lower): v = dict(v)
            r[k] = v

        if vid != 'pikle':
            import pickle
            with open( fl+'.pikle', 'wb') as w:
                pickle.dump( r, w )
        return
        if vid != 'pprint':
            import pprint
            pprint.PrettyPrinter._dispatch[ set_lower.__repr__] = pprint.PrettyPrinter._pprint_set
            pprint.PrettyPrinter._dispatch[ dict_lower.__repr__] = pprint.PrettyPrinter._pprint_ordered_dict
            with open(fl+'.cache', 'w') as w:
                pprint.pprint( r, w, indent=2)

    def cheti( az, fl, moin =False, popylni_avto =True, mahni_izmislimi =True):
        for a in fl:
            a = a.strip()
            if not a: continue
            if a[0] == '#':
                if 0:
                    if a.startswith( '#='):     #moin
                        kvv = a[2:].split()
                        az.eto_imena( *kvv, **ka)
                        continue
                az.komentari.append( a)
                continue

            #if a[0] == '+':
            #    az.eto_imepylno( a[1:])
            #    continue
            if 0:
                lr = a.split('::',1)    #moin
                if len(lr) == 2:
                    v,k = [x.strip() for x in lr]
                    if '.' not in v and '_' not in v:
                        az.komentari.append( '###??? '+a)
                        continue
                    az.eto_imena( k,v)
                #else:
                #   assert ':' not in a
                # ...
            else:
                ak = a.split('#',1)
                a = ak[0].strip()
                kvv = a.split()
                ime = az.eto_imena( *kvv)
                if len(ak)==2 and ak[1].strip():
                    az.komentari_po_ime.setdefault( ime, set()).add( ak[1].strip())

        #накрая, след всички ръчни
        if popylni_avto:    az.popylni_avto()
        if mahni_izmislimi: az.mahni_izmislimi()

    def pishi_moin( az, k,vv):
        for v in sorted( vv):
            if '.' in v:
                yield ' %(v)-20s :: %(k)s' % locals()  #space at start and after ::
            else:
                yield '#= %(v)-20s  %(k)s' % locals()

    def pishi( az):
        b = ''
        for varianti in sorted( az.imena.values(), key= lambda x: (x.neime, x.first)):   #подреждане: големи букви после малки букви ; неимената накрая
            k = varianti.first
            if k[0] != b:
                yield ''
                b = k[0]
            vv = sorted( (x for x in varianti.values() if x != k and x in az.rychni) ,
                    key = lambda x: (x != varianti.second, x)
                    )
            kom = az.komentari_po_ime.get( k)
            if varianti.neime: k = '_'+k
            r = k if not vv else (k.ljust(25) +' '+ ' '.join( v.replace('._','.') for v in vv ))
            if kom:
                N=10
                r = r.ljust(N*((len(r)+N-1)//N)) + ' #'+' '.join( sorted(kom))
            yield r

    def zapishi( az):
        for x in az.komentari:
            for p in ['#2+', '#?']:
                if x.startswith( p): break
            else:
                yield x

        for x in az.pishi():
            yield x
        for k,v in az.mnogoznachni().items():
            yield '#2+ '+k+ ' : ' + ' '.join( sorted(v))


if __name__ == '__main__':
    import sys
    from svd_util import eutf
    eutf.fix_std_encoding()
    if '--sykr' in sys.argv:
        sykrashtenia( 'АзБукиВеди', dbg=2 )
        print('--')
        sykrashtenia( 'Алфа_Бета_Гама', dbg=2 )
        print('--')
        sykrashtenia( 'АзБукиВеди', dbg=2, bez_lipsi=True )

    elif '--test' not in sys.argv:

        a = Abbr()
        a.cheti_eutf( sys.stdin)
        a.dbg=0
        if a.dbg:
            for k,vv in sorted( a.rychni.items()):
                print( 3333, k.ljust(25) +' '+ ' '.join( sorted(vv)))
        if a.dbg:
            for k,vv in sorted( a.rychni.items()):
                print( 3333, k.ljust(25) +' '+ ' '.join( sorted(vv)))
        for x in a.zapishi():
            print( x)

    else:

        #прекъсване: при _ / преход малки към големи / след .
        #след разделяне, малки-големи букви нямат значения
        rk = '''
            Аз / Дух    = АзДух  = Аз_дух = Аз__дух = аз__дух = азДух
            Аз / Дух    = АзДУх  = Аз_ДУх = азДУх = азДУХ
            Аз / Ду / х = АзДуХ  = Аз_ДУ_х = азДУ_х = азДуХ = аз_дуХ
            Аз./ Дух    = Аз.Дух = Аз._дух = Аз.дух = аз.дух

            Аз / . / Дух  = Аз_._дух
            Аз / . / Ду / Х  = Аз_._дуХ

            Аз / Д / Ух  = аз_дУх = аз__дУх

            Аз-Дух    = Аз-Дух = Аз-дух
            Аз.       = Аз.
            Аз / .    = Аз_.
            Аз / ./.  = Аз_.. = Аз_._.
            А. / А. / Милн = А.А.Милн
            A. / A. / Miln = A.A.Miln
            вокалната / група / „Радиодеца”     =    вокалната_група_„Радиодеца”
            Аз / "Дух"  = Аз_"Дух"
            '''
        def razdeli_kamila_lower( t): return [ a.lower() for a in razdeli_kamila(t) ]
        for t in rk.strip().split('\n'):
            t = t.split('#')[0].strip()
            if not t: continue
            t = [ i.strip() for i in t.split('=') ]
            exp = [ a.strip() for a in t[0].split('/') ]
            loexp = [ a.lower() for a in exp ]
            for i in t[1:]:
                r = razdeli_kamila_lower( i)
                assert r==loexp, '''
                    вход  : {i} : {t}
                    очаква: {loexp}
                    изход : {r}'''.format(**locals())

        txt = '''
АланМилн                А.А.Милн А.Милн Ал.Милн
АлександърЙосифов       А.Йосифов Ал.Йосифов
АнгелГенов              Анг.Генов
АнтониГенов             Ан.Генов А.Генов                                #в този ред! тест на .second
_хор_Бодра_песен  хор_Бодра_песен-Шумен ХорБодраПесен хор_песен         #хор_песен остава - тест на bez_lipsi=neime=True
ЕрнстХофман             Е.А.Хофман Е.Т.А.Хофман Е.Т.Хофман ЕТА.Хофман ЕрнстТеодорАмадеусХофман  #остават ЕТА.* и дългото: другите са автоматик, bez_lipsi=neime=False
ЕлиТопалова-Дреникова   Е.Топалова-Дреникова
ЕлиТопаловаДреникова    Е.ТопаловаДреникова ЕлиТ.Дреникова Е.Т.Дреникова Е.Дреникова ЕлиДреникова
НелиТопалова            НелиТопалова-Дреникова Н.Топалова-Дреникова Н.ТопаловаДреникова НелиТопаловаДреникова НелиТ.Дреникова Н.Т.Дреникова
Ханс_Андерсен           Андерсен Х.Кр.Андерсен Ханс_Кристиан_Андерсен Ханс_Кристиян_Андерсен
'''.strip().split('\n')
        res = '''
Алан_Милн               А.А.Милн
Александър_Йосифов
Ангел_Генов
Антони_Генов            Ан.Генов А.Генов                                #в този ред! тест на .second
Ели_Топалова-Дреникова
Ели_Топалова_Дреникова
Ернст_Хофман            ЕТА.Хофман Ернст_Теодор_Амадеус_Хофман          #остават ЕТА.* и дългото: другите са автоматик, bez_lipsi=neime=False
Нели_Топалова           Нели_Топалова-Дреникова Нели_Топалова_Дреникова
Ханс_Андерсен           Андерсен Ханс_Кристиан_Андерсен Ханс_Кристиян_Андерсен
_хор_Бодра_песен  хор_Бодра_песен-Шумен хор_песен                       #хор_песен остава - тест на bez_lipsi=neime=True
'''.strip().split('\n')
        novi = '''
АсенГенов
АсенЙосифов
АлдинЙосифов
АлдоМилн
НинаСтамова
НияСтамова
НинаСтамова
НияСтамова
Нина_Стамова
хор_Бодра_песен
Хор_Песен
'''.strip().split('\n')
        def t( vh, izh):
            a = Abbr()
            a.dbg=1
            a.cheti( vh)
            r = [ x.split() for x in a.pishi() if x.strip() ]
            o = [ i.split() for i in izh ]
            if o != r:
                print( 'вход  :', '\n\t'.join( vh))
                print( 'чака  :', '\n\t'.join( ((x in r) and '  ' or '- ')+'  '.join(x) for x in o))
                print( 'изход :', '\n\t'.join( ((x in o) and '  ' or '+ ')+'  '.join(x) for x in r))
            assert o == r

            for n in novi:
                a.eto_imepylno( n)
            for n in novi:
                print( 'ново', n, a.dai_kyso( n) )
            #print( a.rychni)
            #print( a.avto)
            for i in a.zapishi():
                print( 99, i)
            for t in txt:
                vkk = t.split()
                ime = razdeli_kamila2_( vkk[0])
                print( 1333, *vkk)
                for k in vkk[1:]:
                    if k[0]=='#': break #komentar
                    p = a.dai_imepylno( k)
                    assert p == ime, (k,p,ime)
        t( txt, res)
        t( res, res)

# vim:ts=4:sw=4:expandtab

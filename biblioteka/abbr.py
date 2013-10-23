#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from svd_util.py3 import dictOrder

def razdeli_kamila( t):
    #r = ''
    r = ['']
    u = None
    for c in t:
        cu = c.isupper()
        if u is not None:
            if not u and cu:    #malki->golemi
                r.append( '')
                #yield r
                #r = ''
        u = cu
        r[-1] += c
    return r
    #    r += c
    #if r: yield r

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

def sykrashtenia( t, samo_pred_glasna_sled_syglasna =False, ako_pochva_s_glasna =False, min_ostatyk =2, vse =True):
    r = razdeli_kamila(t)
    ime = r[0]

    if (len(r)==1           #Нещо
        or len(r)==2 and ime.endswith('-')    #заю-баю
        #or '_' in t         #хор_Някакъв    ?
        #or ime.islower()       #хорНякакъв    #XXX слабо
        #or len(ime)<=2         #ИвМонтан ХюЛофтинг
        ):
        return [ '' ] #t

    if r[-2].endswith('-'):
        r[-2] += r[-1]
        del r[-1]

    bukva = ime[0]
    im = bukva
    spisyk = [ im +'.'+ r[-1] ]           #Х.Петров
    spisyk2 = []  #Hri.Petrov
    #yield
    dylgo = len(ime)>3
    if dylgo:
        skyseno = False
        for b in ime[1:]:
            im += b
            ostatyk = len(ime)-len(im)
            if not vse and min_ostatyk > ostatyk: break
            if b in glasni:
                if samo_pred_glasna_sled_syglasna:
                    if not skyseno and not ako_pochva_s_glasna or bukva.lower() in glasni0:
                        #if len(im)>=2 and 'ь' == im[-2]: #Пь - избегни
                        #    pass #print( 7775, spisyk )
                        #else:
                            spisyk = spisyk[-1:]    #poslednoto e hubavoto
                            skyseno = True
                if not vse: break
            if not dylgo or b in glasni or min_ostatyk >=ostatyk and not (len(ime)==4 and ostatyk==2):
                ss = spisyk2
            else:
                ss = spisyk
            ss.append( im +'.'+ r[-1] )   #Хр.Петров Андр.Ангелов
    else:
        spisyk2.append( ime +'.'+ r[-1] ) #Ива.Петрова - но без Ив.Петрова

    im = bukva
    for p in r[1:-1]:   #E.T.A.Hoffman
        im += '.'+p[0]
        spisyk.append( im +'.'+ r[-1] )
    assert spisyk, ime
    #spisyk += spisyk2  #трябва да се ползва отделно от нормалните!
    #if '000' in ime: print( 766666, spisyk, spisyk2)
    if vse: return spisyk, spisyk2
    return spisyk

from svd_util.dicts import dict_lower

class Abbr:
    dbg=0
    def __init__( az, avto_sykrashtenia =False):
        az.imena = dictOrder()   #име : [всички варианти]    впоследствие тези които са измислими, не се записват
        az.rychni = {}  #съкр: имена ; ръчно сложени, имат превес над автоматични ; възможна е многозначност!
        az.avto = dict_lower()    #съкр: имена ; автоматични, по-старите имат превес
        az.avto2= dict_lower()    #съкр: имена ; автоматични, невалидни
        az.komentari = []

    def eto_imena( az, ime, *varianti):   #ръчни
        ime = ime.strip()
        varianti = [ v.strip() for v in varianti ]
        az.imena.setdefault( ime, set() ).update( varianti )
        dbg = az.dbg
        #az.eto_imepylno( ime)
        for v in varianti:
            rychni = az.rychni.setdefault( v, set() )
            if dbg: print( 3333333, 'ръчно', v, ime, ' '.join( sorted(rychni)) )
            rychni.add( ime )
            #if dbg and
            if len(rychni)>1:
                print( 2222, '!ръчно многозначни', ime, v, ' '.join( sorted(rychni)) )    #assert?
            if '.' not in v:
                az.eto_imepylno( ime, v )

    def eto_imepylno( az, ime, ime_za_sykr ='', dbg=0):    #закача съкращенията на име-за-съкр към име
        ime = ime.strip()
        ime_za_sykr = ime_za_sykr.strip() or ime
        if ' ' in ime_za_sykr: return True
        dbg = dbg or az.dbg
        validni = []
        sdylgo = { ime }
        sp = sykrashtenia( ime_za_sykr, vse=True)
        sp2= []
        if len(sp)>1: sp,sp2 = sp
        for s in sp+sp2:
            if not s or '.' not in s: return True    #несъкратимо
            azavto = az.avto if s in sp else az.avto2
            avto = azavto.setdefault( s, [] )
            if dbg: print( 444444, ime, s, avto)
            if ime in avto: continue      #вече е там
            rychni = az.rychni.get( s, ())
            if dbg: print( 555555, ime, s, avto, rychni)
            #if s in sp2: nevalidni.append( s)
            if azavto is az.avto and not avto and (not rychni or rychni == sdylgo):
                validni.append( s)
            elif dbg:
                ss = (set(avto) | set(rychni)) - sdylgo
                if ss: print( 44, 'автоматично но многозначно', s, ime, ime_za_sykr, ':', ' '.join( sorted(ss)) )
            avto.append( ime)

        if dbg and validni: print( 55, 'автоматични', ime, ' '.join( sorted(validni)))
        az.imena.setdefault( ime, set() ).update( validni)
        if dbg: print( 555, az.imena[ ime])

    def dai_vse( az, kyso):
        return az.rychni.get( kyso) or az.avto.get( kyso) or az.avto2.get( kyso) or ()

    def dai_imepylno( az, kyso):
        kyso = kyso.replace( '_','')
        r = az.dai_vse( kyso)
        return r and list(r)[0] or kyso in az.imena and kyso

    def dai_kyso( az, ime, original=True, dbg =False, min =False, vse =False):
        ime0 = az.dai_imepylno( ime) or ime #АсенКисимов -> АсенАнгелов -> ..
        r = az.imena.get( ime0)
        if dbg: print( 666, ime, ime0, r)
        if not r: return r  #несъкратимо или съкращението заето
        if not original: ime = ime0
        if '_' in ime: return ime         #хор_Някакъв    ?
        #else
        #най-късото валидно за име0 (АсенАнгелов) И направено от име (А.Кисимов) И валидно за оригинала
        ss = list( sykrashtenia( ime, samo_pred_glasna_sled_syglasna= not min, vse= vse))
        r = sorted( r, key= lambda x: (len(x),x) )  #азбучно при еднаква дължина
        if ss:
            for x in r:
                if x in ss:
                    return x
        return r[0] #най-късото



    def mnogoznachni( az):
        return dict( (k,v) for k,v in az.rychni.items() if len(v)>1 )

    def popylni_avto( az):
        for i in az.imena:
            az.eto_imepylno( i)

    def mahni_izmislimi( az):
        izmislimi = []
        dbg = az.dbg
        for s,imena in sorted( az.rychni.items()):
            ravni = imena == set( az.avto.get(s) or ())
            if dbg: print( 111, s, ravni, imena, az.avto.get( s) )
            if len(imena)>1: continue
            if ravni:
                izmislimi.append( s)
        if dbg: print( 11111, ' '.join( izmislimi))
        for s in izmislimi: del az.rychni[s]

    def cheti_eutf( az, fl):
        from svd_util import eutf
        return az.cheti( eutf.readlines( fl))

    def cheti( az, fl, moin =False):
        for a in fl:
            a = a.strip()
            if not a: continue
            if a[0] == '#':
                if a.startswith( '#='):     #moin
                    kvv = a[2:].split()
                    az.eto_imena( *kvv)
                    continue
                az.komentari.append( a)
                continue

            #if a[0] == '+':
            #    az.eto_imepylno( a[1:])
            #    continue

            lr = a.split('::',1)    #moin
            if len(lr) == 2:
                v,k = [x.strip() for x in lr]
                if '.' not in v and '_' not in v:
                    az.komentari.append( '###??? '+a)
                    continue
                az.eto_imena( k,v)
            else:
                assert ':' not in a
                a = a.split('#')[0].strip()
                kvv = a.split()
                az.eto_imena( *kvv)

    def pishi_moin( az, k,vv):
        for v in sorted( vv):
            if '.' in v:
                yield ' %(v)-20s :: %(k)s' % locals()  #space at start and after ::
            else:
                yield '#= %(v)-20s  %(k)s' % locals()

    def pishi( az, moin =True):
        b = ''
        for k,vv in sorted( az.imena.items()):
            if k[0] != b:
                yield ''
                b = k[0]
            if moin:
                for p in az.pishi_moin( k,vv):
                    yield p
            else:
                vv = [ v for v in vv
                        if '.' not in v         #ne-sykr
                        or v in az.rychni       #rychno-sykr/izbrano
                        #or v not in az.avto     #rychno-sykr ??
                        #or len( az.avto[v])>1   #rychno-izbrano
                        ]
                r = not vv and k or (k.ljust(25) +' '+ ' '.join( sorted(vv)))
                yield r

    def zapishi( az, moin =False ):
        for x in az.komentari:
            for p in ['#2+', '#?']:
                if x.startswith( p): break
            else:
                yield x

        for x in az.pishi( moin= moin):
            yield x
        for k,v in az.mnogoznachni().items():
            yield '#2+ '+k+ ' : ' + ' '.join(v)


if __name__ == '__main__':
    import sys
    from svd_util import eutf
    eutf.fix_std_encoding()
    if '--test' not in sys.argv:

        a = Abbr()
        a.cheti_eutf( sys.stdin)
        a.dbg=0
        if a.dbg:
            for k,vv in sorted( a.rychni.items()):
                print( 3333, k.ljust(25) +' '+ ' '.join( sorted(vv)))
        a.popylni_avto()
        a.mahni_izmislimi()
        if a.dbg:
            for k,vv in sorted( a.rychni.items()):
                print( 3333, k.ljust(25) +' '+ ' '.join( sorted(vv)))
        for x in a.zapishi():
            print( x)

    else:

        txt = '''
АланМилн            А.А.Милн А.Милн Ал.Милн
АлександърЙосифов   А.Йосифов Ал.Йосифов
АнгелГенов          Анг.Генов
АнтониГенов         А.Генов Ан.Генов
'''.strip().split('\n')
#АсенГенов           Ас.Генов
        res = '''
АланМилн            А.А.Милн
АлександърЙосифов
АнгелГенов
АнтониГенов         А.Генов Ан.Генов
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
'''.strip().split('\n')
        def t( vh, izh):
            a = Abbr()
            #a.dbg=1
            a.cheti( vh)
            a.popylni_avto()
            a.mahni_izmislimi()
            r = [ x.split() for x in a.pishi( moin= False) if x.strip() ]
            izh = [ i.split() for i in izh ]
            if izh != r:
                print( 'e:', '\n'.join( ' '.join(i) for i in izh))
                print( 'r:', '\n'.join( ' '.join(i) for i in r))
            assert izh == r, r

            for n in novi:
                a.eto_imepylno( n)
            for n in novi:
                print( n, a.dai_kyso( n) )
            #print( a.rychni)
            #print( a.avto)
            for t in txt:
                vkk = t.split()
                #print( 333, ' '.join( vkk))
                for k in vkk[1:]:
                    p = a.dai_imepylno( k)
                    assert p == vkk[0], (k,p)
                    p = a.dai_imepylno( k)
        t( txt, res)
        t( res, res)

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from svd_util.py3 import *
from svd_util import lat2cyr
cyr2lat = lat2cyr.zvuchene.cyr2lat
from svd_util.dicts import dict_lower
from svd_util.lists import appendif, extendif, listif

from abbr import Abbr

class AbbrDejnosti( Abbr):
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
            #return
            pass

        kalpak = az.re_dejnost.sub( '', a)
        return kalpak

    tyrseni = {}
    def dobavi( az, tt, xime, fname, propusni_takiva =None):
        r = []
        for a in tt.split('+'):
            a = a.strip().rstrip(',')
            i = a.rstrip(',? ')
            if not i: continue
            if '.' in i: # or '?' in a:
                az.tyrseni.setdefault( a, set()).add( (xime,fname) )
            else:
                if not( propusni_takiva and propusni_takiva( i) or az.dai_imepylno( i)):
                    if '?' in a:
                        az.tyrseni.setdefault( a, set()).add( (xime,fname) )
                    else:
                        az.eto_imepylno( i)
            appendif( r, a)
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
        изпълнение-песни    изп-песни
        ар*анжимент
        дир*игент
    '''
    dejnosti2 = '''
        хор*майстор     .хорм      хор-дир*игент диригент-хор хордир
        музикално-оформление  .м.оф  .м.о  .мо    музикална-картина музикална-среда музикално-оформление муз.оф*ормление
        звуково-оформление    .зв.оф .зв .з .з.оф*ормление  .зв.еф*екти .з.е*фекти .зе звук звукова-картина звукова-среда звуково-оформление зв.оф*ормление звукови-еф*екти ефекти
        звукор*ежисьор  .зв.р*еж   .з.р*еж      тонр*ежисьор тон.реж*исьор
        звукооп*ератор  .зв.оп     .з.оп        тоноп*ератор тон.оп*ератор
        звукоинж*енер   .зв.инж    .з.инж       тонинж*енер тонм*айстор тон.инж*енер
        звукот*ехник    .зв.т*ехник  .з.т*ехн     тонт*ехник зв.тех*ник тон.т*ехник
        звукозапис      запис
        звукообр*аботка постпр*одукция .зв.обр .з.обр
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

# vim:ts=4:sw=4:expandtab

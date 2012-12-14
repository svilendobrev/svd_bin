#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from svd_util.yamls import usability
from svd_util.struct import DictAttr
from svd_util import dbg, optz, lat2cyr
#cyr2lat = lat2cyr.zvuchene.cyr2lat

from svd_util.osextra import save_if_different, globescape

import rec2dir

from distutils.dep_util import newer

import os
from glob import glob
import os.path as ospath

def log( bez_localz =False ):
    if not optz.log: return
    if bez_localz:
        print( dbg.dbg_funcname( 1+2), '(..)')
    else:
        print( dbg.dbg_funcname_locals( 1))

#TODO === dbg.funcwrap
class obvivka:
    naistina = True
    log = True
    def __init__( me, func): me.func = func
    def __call__( me, *a, **k):
        if me.log: print( me.func, a, k)
        if me.naistina: return me.func( *a, **k)

from svd_util.osextra import makedirs
makedirs = obvivka( makedirs)
link = obvivka( os.link)
rename = obvivka( os.rename)
join = ospath.join

class cyr:
    parcheta = 'парчета'
    srezove = 'срезове'
    otkyde = 'откъде'
    chast = 'част'
    ime = 'име'

def diropis2srez( dirime, opis, optz):
    log()

    srezove = []
    def dobavi( **k): return srezove.append( DictAttr( **k))
    parcheta = opis.get( cyr.parcheta)
    if parcheta:
        for fime, p in parcheta.items():
            s = dai_srezove( p)#.get( cyr.srezove)
            if not s: continue
            for f in dirime+'/'+fime, dirime+'/0/'+fime:
                if ospath.exists( f):
                    r = razglobi_ime( fime)
                    dobavi( fime= f, srez= s, nomer= p.get( cyr.chast, r.get('nomer')), ime= dai_ime( p) )
                    break
            else:
                print( '! липсва', f)
    else:
        s = dai_srezove(opis)#.get( cyr.srezove)
        if s:
            dirimena = dirime+'/0/*wav'
            fimena = glob( dirimena)
            if len( fimena) == 1:
                dobavi( fime= fimena[0], srez= s)
            elif not fimena:
                print( '! липсва', dirimena)
            else:
                print( '!!!! няколко:', fimena)

    for p in srezove:
        assert ospath.exists( p.fime)
        # ако срезове != стари срезове или звуковия файл е по-нов от дир/опис: режи, и парчетата към дир/
        if 1: #newer( fime, fopis):
            izvadi( p.fime, p.srez, dirime, nomer= p.get('nomer'), ime= dai_ime(p))


def zapis2dir2srez2opis( fime, opis, optz):
    log()

    # разглоби име
    ot_ime = razglobi_ime( fime )    #predavane, ime, avtor, chast, vreme
    #print( '\n'.join( ': %s: %r' % kv for kv in ot_ime.items()) )

    # направи дириме
    #dirime = cyr2lat( sglobi( ot_ime.ime, ot_ime.avtor, ot_ime.chast, 'radio') )
    dir_ot_ime = ot_ime.get( 'dirname')
    dirime = dir_ot_ime or ot_ime.f

    # направи дир/ дир/0/
    mkdir( dirime)

    fopis = dirime+'/opis'

    #входящ опис
    nov_opis, srezove = popylni_opis( opis, ot_ime )

    '''
        c: 12 - 34
        c:
           1a:
               13 - 45
           2d: 55 - 65
    '''

    star_opis = dai_opis( fopis) or {}
    stari_srezove = ()
    if star_opis:
        parcheta = star_opis.get( cyr.parcheta)
        if parcheta:
            if fime in parcheta:
                stari_srezove = parcheta[ fime].get( cyr.srezove)
        else:
            stari_srezove = star_opis.get( cyr.srezove)

        #if stari_srezove: print( 6666666, stari_srezove, srezove)

    if ospath.exists( fime):
        # ако срезове != стари срезове или звуковия файл е по-нов от дир/опис: режи, и парчетата към дир/
        if 1: # stari_srezove != srezove or newer( fime, fopis):
            ime = dai_ime( opis)
            #if not dir_ot_ime: ime = '-'.join( [ot_ime.f, ot_ime.data, ime or ''])
            izvadi( fime, srezove, dirime, nomer= ot_ime.get('nomer'), ime= ime, opfx= not dir_ot_ime and fime)
    else:
        print( '!!!! липсва', fime)

    if optz.parcheta:
        nov_opis = { cyr.parcheta: { fime: nov_opis }}

    # направи + попълни дир/опис - стария има предимство за всичко освен в срезовете
    print( 333333333, usability.dump( nov_opis))
    smesi_opisi( nov_opis, star_opis)
    #print( 444444444, usability.dump( nov_opis))

    if optz.zapis or optz.opis:
        r = usability.dump( nov_opis)
        VIMtail = '# v' + 'im:ts=4:sw=4:expandtab:ft=yaml' #separated!
        if VIMtail: r += '\n'+VIMtail
        save_if_different( fopis, r)

    # премести файл.* в дир/0/
    premesti_v_0( fime, dirime)

def razglobi_ime( fime):
    ot_ime = rec2dir.razglobi( fime )    #predavane, ime, avtor, chast, vreme
    return DictAttr( ot_ime)

#def sglobi( ime, avtor):
#    return '--'.join( [c2l( ime), c2l(avtor), 'radio'] ).replace(' ', '.')

def mkdir( dir):
    log()
    makedirs( dir, exist_ok =True)

def dai_opis( fopis):
    log()
    star_opis = {} #None
    try:
        with open( fopis) as f:
            star_opis = DictAttr( usability.load( f ) )
    except IOError: pass
    return star_opis

s_srezove = 'srezove srez s срезове срез с @@ c cut cuts'.split()    #свободни: $ ^
def dai_srezove( opis):
    srezove = ()
    for k in s_srezove:
        srez = opis.pop( k, None)
        if srez is not None: srezove = srez
    return srezove

s_ime = 'ime име'.split()
def dai_ime( opis):
    for k in s_ime:
        v = opis.get(k)
        if v: break
    return v

def smesi_opisi( nov_opis, star_opis):
    # новия има предимство само за срезовете, парчета се смесват
    for k,v in star_opis.items():
        if k == cyr.srezove:
            continue
        if k == cyr.parcheta:
            smesi_opisi( nov_opis.setdefault( cyr.parcheta, {}), v)
            continue
        nov_opis[ k] = v

def popylni_opis( opis, ot_ime):
    log( bez_localz= 1)

    if isinstance( opis, dict) and len(opis)>1:
        opis = DictAttr( opis)
        srezove = dai_srezove( opis)
    else:
        srezove = opis
        opis = DictAttr()

    for k,kk in dict( ime= 'ime име', avtori= 'avtor автор').items():
        if not ot_ime.get(k): continue
        kk = kk or k
        for ko in kk.split():
            if opis.get(ko): break
        else:
            opis[ ko] = ot_ime[ k]

    etiketi = []
    for k,v in dict( zagolemi= 'възрастни', dok= 'док').items():
        if ot_ime.get( k):
            etiketi.append( v)
    if etiketi: opis[ 'етикети'] = ' '.join( etiketi )

    opis[ 'издание' ] = 'радио'
    otkyde = ' '.join( x for x in [
                            ot_ime.get( 'rubrika') or optz.rubrika or '',
                            ot_ime.data
                        ] if x)
    if otkyde.isdigit(): otkyde = int( otkyde)

    if ot_ime.get( 'nomer'):
        tova = { 'част': ot_ime.nomer, cyr.otkyde: otkyde }
        if srezove: tova[ cyr.srezove] = srezove
        opis[ cyr.parcheta ] = { fime: tova }
    elif srezove:
        opis[ cyr.srezove ] = srezove
        opis[ cyr.otkyde ] = otkyde

    return opis, srezove

def premesti_v_0( fime, dirime):
    log()
    dir = dirime + '/0'
    mkdir( dir)

    bezext,ext = ospath.splitext( fime)

    if 0:
        #stari
        import time
        sega = str( time.mktime( time.localtime()) )
        dirstari = join( dir, sega)
        for f in glob( globescape( join( dir, ospath.basename( bezext))) +'.*'):
            makedirs( dirstari)
            rename( f, join( dirstari, ospath.basename( f) ))

    #novi
    davai = optz.premesti
    for f in glob( bezext+'.*'):
        of = join( dir, ospath.basename( f))
        if not ospath.exists( of):
            if davai: rename( f, of)
            else: link( f, of)
        else:
            assert ospath.samefile( f, of), of
            if davai: os.remove( f)

from cutter import Cutter

def izvadi( fime, srezove, dirime, nomer =None, ime ='', opfx =''):
    log()
    c = Cutter()
    if isinstance( srezove, str):
        c.name = 'c'
        srezove = [s.split('#',1)[0] for s in srezove.split('\n')]
        c.readcuts( ' '.join( srezove))
    elif isinstance( srezove, dict):
        for k,v in srezove.items():
            c.name = k
            c.readcuts( v)
            c.add()
    else:
        assert 0, (srezove, fime)
    c.save( infile= fime, path= dirime,
        ofile= '-'.join( str(f) for f in [opfx or dirime.rstrip('/'), ime, nomer] if f),
        do_nothing= not optz.zapis,
        #verbose= True
        )

def izvadki2zapis2dir2srez2opis( izvadki):
    with open( izvadki ) as f:
        d = usability.load( f)
    #print( usability.dump( d ))
    for fime, opis in d.items():
        print( '\n\n------------', fime )#, opis)
        zapis2dir2srez2opis( fime, opis, optz)


if __name__ == '__main__':
    optz.bool( 'zapis')
    optz.bool( 'opis')
    optz.bool( 'premesti')
    optz.bool( 'izvadki')
    optz.bool( 'parcheta')
    optz.bool( 'log')
    optz.str( 'rubrika')
    optz,args = optz.get()
    obvivka.naistina = optz.zapis
    obvivka.log = optz.log #False
    if optz.izvadki or ospath.isfile( args[0] ):
        izvadki2zapis2dir2srez2opis( args[0])
    else:
        for d in args:
            assert ospath.isdir( d)
            fopis = d+'/opis'
            if not ospath.exists( fopis): continue
            print( d)
            with open( fopis) as f:
                opis = usability.load( f)
            print( dai_ime( opis))
            diropis2srez( d, opis, optz)


# vim:ts=4:sw=4:expandtab

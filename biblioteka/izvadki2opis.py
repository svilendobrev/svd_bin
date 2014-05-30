#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from svd_util.yamls import usability
from svd_util.struct import DictAttr
from svd_util import dbg, optz, lat2cyr
cyr2lat = lat2cyr.zvuchene.cyr2lat
l2c     = lat2cyr.zvuchene.lat2cyr

from svd_util.osextra import save_if_different, globescape, makedirs

import rec2dir

from distutils.dep_util import newer

import os, re
from glob import glob
import os.path as ospath
import operator, functools

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

makedirs = obvivka( makedirs)
link = obvivka( os.link)
rename = obvivka( os.rename)
remove = obvivka( os.remove)
join = ospath.join
basename = ospath.basename
exists = ospath.exists

class cyr:
    _parcheta = 'пар*чета части'.split()
    parcheta = _parcheta[0].replace('*','')
    _srezove = 'срез*ове @@ cut*s срез0'.split()    #свободни: $ ^
    srezove = _srezove[0].replace('*','')
    otkyde = 'откъде'
    chast = 'част'
    ime = 'име'

def multiglob( dirimena):
    return functools.reduce( operator.add, [ glob( d) for d in dirimena ] )

def diropis2srez( dirime, opis, optz):
    log()
    fdirime = (not dirime or dirime.rstrip('/')=='.') and '_' or dirime

    srezove = []
    def dobavi( **k): return srezove.append( DictAttr( **k))
    parcheta = dai( opis, *cyr._parcheta)
    #for p in [ cyr.chasti ] + [ cyr.parcheta[:i] for i in range( 3, 1+len(cyr.parcheta))]:
    #    parcheta = opis.get(p)
    #    if parcheta: break
    if parcheta:
        for fime, parche in parcheta.items():
            fime = str(fime)
            pp = isinstance( parche, str) and [ dict(srez=parche) ] or not isinstance( parche, (list,tuple) ) and [ parche ] or parche
            for n,p in enumerate( pp,1):
                ss = dai_srezove( p, mnogo= True)
                if not ss: continue
                if not isinstance( ss, (list,tuple)): ss = [ss]
                for s in ss:
                    if not s: continue
                    print( '  ', fime, s)
                    dirimena = [ dirime+'/'+fime, dirime+'/0/'+fime ]
                    fimena = dirimena + multiglob( [ globescape( d)+'.*wav' for d in dirimena])
                    if len(pp)==1: n=None
                    for f in fimena:
                        if exists( f):
                            try:
                                nomer = razglobi_ime( fime).get('nomer')
                            except:
                                mnomer = re.search( '(\d+)', fime)
                                if mnomer: nomer = int( mnomer.group(1) )
                                else: nomer = fime
                            ime = dai_ime(p)
                            dobavi( fime= f,
                                nomer= p.get( cyr.chast, nomer) or n,
                                srez = ime and { ime: s } or s,
                                )
                            break
                    else:
                        print( '! липсва парче:', fime)
    else:
        ss = dai_srezove( opis, mnogo= True)
        if isinstance( ss, dict):
            for fime, srez in ss.items():
                dobavi( fime= fime, srez= srez)

        elif ss:
            if not isinstance( ss, (list,tuple)): ss = [ss]
            dirimena = [ globescape( dirime+ ex)+ '*wav' for ex in ['/', '/0/'] ]
            fimena = multiglob( dirimena )
            if len(fimena)==2:
                if basename( fimena[0]).replace( '.1.c.wav', '.wav' ) == basename( fimena[-1]):
                    del fimena[0]
            if len( fimena) == 1:
                for srez in ss:
                    dobavi( fime= fimena[0], srez= srez)
            elif not fimena:
                print( '! липсва', dirimena)
            else:
                print( '!!!! няколко:')
                for i in fimena: print( ' ?', i)

    for p in srezove:
        assert exists( p.fime)
        # ако срезове != стари срезове или звуковия файл е по-нов от дир/опис: режи, и парчетата към дир/
        if 1: #newer( fime, fopis):
            izvadi( p.fime, p.srez, fdirime, nomer= p.get('nomer'), ime= dai_ime(p))


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

    if exists( fime):
        # ако срезове != стари срезове или звуковия файл е по-нов от дир/опис: режи, и парчетата към дир/
        if 1: # stari_srezove != srezove or newer( fime, fopis):
            ime = isinstance( opis, dict) and dai_ime( opis)
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

def dai_srezove( opis, **ka):
    return dai( opis, *cyr._srezove, **ka) #, mnogo= True

from instr import zaglavie
def dai_ime( opis):
    return zaglavie( dai( opis, cyr.ime))
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

def popylni_opis( opis0, ot_ime):
    log( bez_localz= 1)

    srezove = None
    opis = opis0
    if isinstance( opis, dict) and len(opis)>1:
        opis = DictAttr( opis)
        srezove = dai_srezove( opis)
    if not srezove:
        srezove = opis0
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
        for f in glob( globescape( join( dir, basename( bezext))) +'.*'):
            makedirs( dirstari)
            rename( f, join( dirstari, basename( f) ))

    #novi
    davai = optz.premesti
    for f in glob( globescape( bezext) +'.*'):
        of = join( dir, basename( f))
        if not exists( of):
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
        srezove = [s.split('#',1)[0] for s in srezove.split('\n')]
        v = ' '.join( s for s in srezove if s.strip())
        v = rec2dir.opravi_tireta( v, spc=' ')
        c.readcuts( v)
    elif isinstance( srezove, dict):
        for k,v in srezove.items():
            c.name = str(k)
            v = rec2dir.opravi_tireta( v, spc=' ')
            c.readcuts( v)
            c.add()
    else:
        assert 0, (srezove, fime)

    c.save( infile= fime, path= dirime,
        ofile_as_sfx = ''.join( '-'+str(f) for f in [
            #opfx or dirime.rstrip('/'),
            #fime,
            ime, nomer]
            if f),
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


from svd_util.lists import appendif

def varianti( v):
    dd = [ v.replace('*','') ]
    if '*' in v:
        l,r = v.split('*')
        for d in [ l+r[:i] for i in range( len(r))]:    #len+1 == v
            appendif( dd, d)
    appendif( dd, *[ v.replace('-','') for v in dd if '-' in v ])
    appendif( dd, *[ cyr2lat( v) for v in dd])
    if v.isdigit(): appendif( dd, int(v))
    return dd

def dai( o, *kk, **ka):
    mnogo = ka.get('mnogo')
    r = []
    for k in kk:
        for ki in k.split():
            for v in varianti( ki):
                if v in o:
                    if mnogo: r.append( o[v])
                    else: return o[v]
    return r

import datetime
dnes = datetime.date.today().isoformat().replace('-','')

def obnovi( pyt, opis):
    cel = dai( opis, *'0 стар*о обнови цел замести вместо'.split())
    assert cel
    cel = cel.replace('/op/','/')
    if not cel.endswith('.mp3'): cel+='.mp3'
    assert exists( cel) and ospath.isfile( cel)
    celpyt,celfile = ospath.split( cel)

    elementi = []
    for d in '','0':
        elementi += glob( join( pyt, d, '*.mp3'))
    if len(elementi)!=1:
        print( ' ???', cel, '<<?', elementi)
        return

        #mv obnovi dir(obnovi)/0
    rename( cel, join( celpyt, '0', '-'.join( ['старо', dnes, celfile]) ))

        #mv d/*flac+wav dir(obnovi)/0
        #mv d/0/*flac+wav dir(obnovi)/0
    for ext in 'wav','flac':
        for d in '','0':
            for f in glob( join( pyt, d, '*.'+ext)):
                rename( f, join( celpyt, '0', basename(f)))

        #mv d/*mp3 obnovi ako e edin
    rename( elementi[0], cel)
    print( ' ok:', d, '->', cel)


def gotovo( pyt, opis, kym =None, ime =None):
    d = pyt
    assert ospath.isdir( kym), kym
    ime = ime or dai_ime( opis)
    avtori  = dai( opis, 'ав*тор', 'awtor')
    izdanie = dai( opis, 'изд*ание', 'издания').lower()
    izdaniecyr= l2c( izdanie.lower())
    izdaniecyr2= re.sub( '^б([аеоскхнт][анмк])', r'в\1', izdaniecyr)
    if 'lat':
        izdanie = cyr2lat( izdaniecyr2)
        if izdaniecyr2 != izdaniecyr:
            izdanie = (izdanie
            ).replace( 'v','b'
            ).replace( 'h','x'
            ).replace( 'n','h'
            )
    etik    = dai( opis, 'ет*икети') or ''
    avtori = (avtori or '').split()
    stihove = ime.lower() == 'стихове' or 'стих' in etik
    izp = []
    if stihove:
        izp = (dai( dai( opis, 'уч*астници') or opis, 'изп*ълнение') or ()) #.split()
        if izp and isinstance( izp, str): izp = [ izp]
        if len(izp)==1:
            izp = [ i.rstrip('?') for i in izp ]
            #avtori += [ i.rstrip('?') for i in izp ]
        else: izp = []
    from abbr import razdeli_kamila2
    def imena( l):
        return '-'.join( [ razdeli_kamila2(a).replace(' ','.') for a in l])

    if stihove: # and izdaniecyr == 'радио':
        fname = [ imena( avtori), ime, imena( izp) ]
    else:
        fname = [ ime, imena( avtori + izp) ]
    fname = '--'.join( f.strip() for f in fname if f)
    fname = fname.replace('..','.')
    #mau ROOT=d/
    fname = fname.replace(' ', '_')
    fname = fname.replace('-_', '-')
    fname = fname.replace('_-', '-')
    fname_lat = cyr2lat( fname.lower())
    if izdaniecyr:
        fname     += '--'+izdaniecyr
        fname_lat += '--'+izdanie #cyrre.sub( '--v([aeoskhnt]a)$','--b\1', fname_lat)
    fname     = fname.replace( '?','')
    fname_lat = fname_lat.replace( '?','')
    print( ' ', fname_lat, '///', fname )

    elementi = glob( join( d, '*.wav'))
    if not elementi: elementi = glob( join( d, '*.mp3'))
    if len(elementi)==1:
        mkdir( join( d, '0'))
        def kym0( e, d, fname, ext):
            if exists( e+ext):
                rename( e+ext, join( d, '0', fname+ext))
        e,_ext = ospath.splitext( elementi[0])
        kym0( e,d, fname, '.wav')
        kym0( e,d, fname, '.flac')
        rename( e+'.mp3', join( d, fname+'.mp3'))
        print( 'ok:', join( d, fname+'.mp3'))
    else:
        print( ' ??', elementi)

    cel = join( kym, fname_lat)
    if d.rstrip('/') == '.':
        print( 'md + mv * >>', cel)
        makedirs( cel)
        for g in glob( join( d, '*')):
            if g == cel: continue
            rename( g, join( cel, basename(g)))
    else:
        iztrij = None
        if ospath.islink(d):
            iztrij = d
            d = ospath.realpath( d)
        rename( d, cel)
        if iztrij: remove( iztrij)
    #cd ~/azcom/zdetski/`basename $gotovo`
    #m lnfrom ; m sym2; m
    #m zl
    # . e3*
    print( '')

if __name__ == '__main__':
    optz.bool( 'zapis')
    optz.str( 'gotovo')
    optz.bool( 'obnovi')

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
        for d in appendif( [], *args):  #uniq
            assert ospath.isdir( d), d
            d = d.rstrip('/')
            fopis = d+'/opis'
            if not exists( fopis): continue
            print( d)
            with open( fopis) as f:
                opis = usability.load( f)
            ime = dai_ime( opis)
            print( ime)

            if optz.gotovo:
                gotovo( d, opis, kym= optz.gotovo, ime=ime)
            elif optz.obnovi:
                obnovi( d, opis)
            else:
                diropis2srez( d, opis, optz)
# vim:ts=4:sw=4:expandtab

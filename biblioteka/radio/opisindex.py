#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys
import os, glob
import rec2dir
from svd_util.yamls import usability
l2c = rec2dir.lat2cyr.zvuchene.lat2cyr
import difflib

def junk( x): return not x.isalpha()
def tyrsi_podobni( ime, nalichni, min_ratio =0.7):
    podobni = [ (not s.set_seq1( ime.lower()) and 1-s._ratio(), s._item )
        for s in nalichni
        ]
    podobni.sort( key= lambda x: (x[0],)+x[1][:2])
    min_ratio1 = 1-min_ratio
    return [ (round(r,3),i) for r,i in podobni if r <= min_ratio1 ]

def nalichni_imena( nalichni_opisi, nalichni_vremena, quick =0):
    if not nalichni_opisi: return
    nalichni_imena = [] #s(ime).(ime,dir,file)
    def dobavi( x):
        s = difflib.SequenceMatcher( junk )
        if not quick:  ratio = s.ratio
        elif quick==2: ratio = s.real_quick_ratio
        else:          ratio = s.quick_ratio
        s._ratio = ratio
        s._item = x
        s.set_seq2( x[0].lower() )
        nalichni_imena.append( s)
        #if 'Валер' in x[0]: print( '#++ ', x, file= sys.stderr)

    def kym_imeto( opis):
        avtor = opis.get( 'автор')
        if avtor:
            if isinstance( avtor, (list,tuple)): avtor = ' '.join( avtor)
            avtor = avtor.strip()
        return avtor and ' : '+avtor or ''

    fname2vreme = dai_fname2vreme( nalichni_vremena)
    print( '#налични времена:', len( fname2vreme), file= sys.stderr)

    for fn in glob.glob( nalichni_opisi):
        try:
            with open( fn) as f:
                opis = dict( usability.load( f ) )
                ime = opis.get( 'име')
                ime = ime and str(ime).strip()
                if not ime or not ime.strip('?'):
                    ime = l2c( os.path.basename( fn))
                avtor = kym_imeto( opis)
                ime += avtor
                vr = None
                fp = fn.split('/op/')
                if len(fp)==2:
                    fp[0] = fp[0].rsplit('/',1)[-1]
                    vr = fname2vreme.get( '/'.join( fp).rstrip('/'))
                vr = vr and round(vr,2) or ''
                #print( '#--- ', '/'.join( fp).rstrip('/'))
                dobavi( (ime, fn, vr))
                parcheta = opis.get( 'парчета')
                if not parcheta: continue
                for fnp,p in parcheta.items():
                    if isinstance( p, str):
                        ime = p
                        avtor1 = avtor
                    else:
                        ime = p.get( 'име')
                        avtor1 = kym_imeto( p) or avtor
                    ime = ime and str(ime).strip()
                    ime = ime or l2c( fnp)
                    ime += avtor1
                    vr = None
                    if len(fp)==2:
                        vr = fname2vreme.get( '/'.join( fp+[fnp]))
                    vr = vr and round(vr,2) or ''
                    #print( '#--- ', vr, '/'.join( fp+[fnp]))
                    dobavi( (ime, fn, fnp, vr ))
        except IOError: pass
        except Exception as e:
            print( fn, ':', str(e), file= sys.stderr)
            raise
    print( '#налични описи:', len( nalichni_imena), file= sys.stderr)
    def tyrsach( ime):
        return tyrsi_podobni( ime, nalichni_imena,
                min_ratio= 0.7 )
    return tyrsach


def dai_fname2vreme( nalichni_vremena):
    fname2vreme = {}
    if nalichni_vremena:
        try:
            f = open( nalichni_vremena)
        except:
            print( '#??? ', nalichni_vremena, file= sys.stderr)
        else:
            for line in f:
                line = line.strip()
                if not line or line[0] != '=': continue
                vr,fn = line.strip('+= ').split( None,1)
                for p in 'prikazki pesnicki zagolemi'.split():
                    p+='/'
                    if '/'+p in fn:
                        fn = p + fn.split('/'+p)[-1]
                        break
                else:
                    continue
                fn = fn.rsplit('.',1)[0]    #.mp3
                m,s = [float(v) for v in vr.split(':')]
                vr = 60*m+s
                fname2vreme[ fn ] = vr
                fp = fn.rsplit('/',1)[0]
                fname2vreme.setdefault( fp,0)
                fname2vreme[ fp ] += vr
    return fname2vreme

if __name__ == '__main__':
    #print( dai_fname2vreme( 'vremena'))
    t = nalichni_imena( '/home/svilen/azcom/detski/zvuk/*/op/*', './vremena')
    print( t( 'Стихове : ВалериПетров'))

# vim:ts=4:sw=4:expandtab

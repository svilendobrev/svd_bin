#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys
import os, glob, traceback
import rec2dir
from svd_util.yamls import usability
from svd_util.dicts import DictAttr
l2c = rec2dir.lat2cyr.zvuchene.lat2cyr
import difflib

def junk( x): return not x.isalpha()
def tyrsi_podobni( ime, nalichni, min_ratio =0.7):
    podobni = [ dictAttr( ratio= not s.set_seq1( ime.lower()) and 1-s._ratio(), **s._item )
        for s in nalichni
        ]
    podobni.sort( key= lambda x: (x.ratio, x.fp, x.get('fnp','')))
    min_ratio1 = 1-min_ratio
    return [ (round( i.ratio,3), i.vreme, i.ime, i.fp, i.get('fnp',''))
                for i in podobni if i.ratio <= min_ratio1 ]

def nalichni_imena( nalichni_opisi, nalichni_vremena, quick =0, min_ratio =0.7):
    if not nalichni_opisi: return
    if '*' in nalichni_opisi:
        nalichni_opisi = glob.glob( nalichni_opisi)
    else:
        try:
            nalichni_opisi = [a.strip() for a in open( nalichni_opisi).readlines()]
        except Exception as e:
            print( '#??? '+repr(e), nalichni_opisi, file= sys.stderr)
            traceback.print_exc()
            return
    nalichni_imena = [] #s(ime).(ime,dir,file)
    def dobavi( ime, avtor, fn, fp, fnp=''):
        ime = ime and str(ime).strip().strip('?') or l2c( fnp or os.path.basename( fn))
        itempath = '/'.join( fp+[fnp]).rstrip('/')
        vreme = ''
        if 1: #or len(fp)==2:
            vreme = fname2vreme.get( itempath.lower())
        vreme = vreme and round(vreme,1) or ''
        #print( '#--- ', vreme, itempath)
        ime += avtor
        x = dict( ime= ime, vreme= vreme, fn= fn, fp= fp, fnp= fnp)
        s = difflib.SequenceMatcher( junk )
        if not quick:  ratio = s.ratio
        elif quick==2: ratio = s.real_quick_ratio
        else:          ratio = s.quick_ratio
        s._ratio = ratio
        s._item = x
        s.set_seq2( ime.lower() )
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

    for fn in nalichni_opisi:
        try:
            with open( fn) as f:
                opis = dict( usability.load( f ) )
                ime = opis.get( 'име')
                avtor = kym_imeto( opis)
                fp = fn.split('/op/')
                if len(fp)==2:                          #src/gramo/zagolemi/op/edikvosi -> zagolemi,edikvosi
                    fp[0] = fp[0].rsplit('/',1)[-1]
                elif fn.endswith( '/opis'):
                    fp = fn.rsplit( '/',1)[:1]
                #elif fn.startswith( '/zapisi/gramo/'):  #/zapisi/gramo/zagolemi/edikvosi/opis
                #    fp = fn.split( '/', 4)[3:]
                #elif fn.startswith( '/zapisi/'):        #/zapisi/zagolemi/edikvosi/opis
                #    fp = fn.split( '/', 3)[2:]
                #elif fn.startswith( '/okradio/'):       #/okradio/dok/edikvosi0/edikvosi1/opis
                #    fp = fn.split( '/', 3)[2:]
                dobavi( ime, avtor=avtor, fp=fp, fn=fn)
                ime2 = opis.get( 'име2')
                if ime2: dobavi( ime2, avtor=avtor, fp=fp, fn=fn)

                parcheta = opis.get( 'парчета')
                if not parcheta: continue
                for fnp,p in parcheta.items():
                    if isinstance( p, str):
                        ime = p
                        avtor1 = avtor
                    else:
                        ime = p.get( 'име')
                        avtor1 = kym_imeto( p) or avtor
                    dobavi( ime, avtor=avtor1, fp=fp, fn=fn, fnp=fnp )
        except IOError: pass
        except Exception as e:
            print( fn, ':', str(e), file= sys.stderr)
            raise
    print( '#налични описи:', len( nalichni_imena), file= sys.stderr)
    def tyrsach( ime):
        return tyrsi_podobni( ime, nalichni_imena, min_ratio= min_ratio)
    return tyrsach


def dai_fname2vreme( nalichni_vremena):
    fname2vreme = {}
    if nalichni_vremena:
        try:
            lines = open( nalichni_vremena).readlines()
        except Exception as e:
            print( '#??? '+repr(e), nalichni_vremena, file= sys.stderr)
            traceback.print_exc()
            return fname2vreme
    for line in lines:
        line = line.strip()
        if not line or line[0] != '=': continue
        line = line.strip('+= ')
        vr,fn = line.split( '/',1)
        fn = '/'+fn
        vr = vr.split('=')[0]
        m,s = [float(v) for v in vr.split(':')]
        vr = 60*m+s
        fn = fn.lower()
        fn = fn.rsplit('.',1)[0]    #.ext
        fname2vreme[ fn ] = vr
        fn2 = fn.rsplit('.',1)
        if fn2[-1] in ('lp','cd','vbr','mc') or fn2[-1].startswith( 'mc-'):   #.ext
            fname2vreme[ fn2[0] ] = vr      #also
        fp = fn.rsplit('/',1)[0]
        fname2vreme.setdefault( fp,0)
        fname2vreme[ fp ] += vr
    return fname2vreme

if __name__ == '__main__':
    #print( dai_fname2vreme( 'vremena'))
    from svd_util import optz
    #optz.float( 'min_ratio', default='0.7', help='min_ratio [default]')
    optz.float( 'max_error', default='0.3', help='max_error [default]')
    #optz.list( 'glob')
    #optz.list( 'walk')
    #optz.list( 'walk')
    optz,args = optz.get()
    optz.min_ratio = 1 - optz.max_error
    import sys
    import os, glob
    if not args:
        opisite = glob.glob( '/home/svilen/src/gramo/*/op/*')
        stdin = None
    else:
        def walk4opis( dir):
            for path,dirs,files in os.walk( dir, followlinks= False):#klas.options.simvolni):
                #if e_za_propuskane and e_za_propuskane( path):
                #    dirs[:] = []
                #    continue
                #dirs[:] = [ d for d in dirs if not (e_za_propuskane and e_za_propuskane( d)) ]
                #yield path, dirs, files
                if 'opis' in files:
                    yield path + '/opis'
        stdin = '-' in sys.argv
        if stdin: sys.argv.remove('-')

        def opisite():
            for f in args:
                if '*' in f:
                    yield from glob.glob( f)
                elif os.path.isdir( f):
                    yield from walk4opis( f)
                else:
                    yield f
        opisite = opisite()
    t = nalichni_imena( opisite, './vremena', min_ratio= optz.min_ratio)

    if not stdin:
        for r in t( 'Стихове : ВалериПетров'): print( r)
    else:
        for i in sys.stdin:
            i = i.strip()
            print(i)
            r0 = None
            for r in t( i):
                if r0 is None: r0 = r[0]
                print( ' ', r)
                if r0 < 0.2 and r[0]>0.3: break #HACK
            print()

# vim:ts=4:sw=4:expandtab

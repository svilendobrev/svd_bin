#!/usr/bin/env python3
# -*- coding: utf8 -*-
from util import optz
optz.usage( '%prog [optz] ot-dir < ren-script-stdin')
#optz.optany( 'ot')
optz.text(  'link_kym',  help= 'направи ново дърво от връзки с този корен')
optz.bool( 'rename',     help= 'преименувай на място')
optz.bool( 'rename_alt', help= 'преименувай на място и остави символна връзка към старото име.alt')
optz.append( 'opis', help= 'подменя имена в опис ; може няколко пъти')
optz.bool( 'link_zagolemi_pootdelno', help= 'връзки: раздели заголеми/ на /moze /neizv ..')
optz.bool( 'nothing', '-n')
optz,args = optz.get()

import os, sys, stat
from os.path import join, exists, dirname, basename, splitext

allfiles = {}
def link( ot, ikym, *pfxs):
    print( ot, ikym)
    ot = join( dir_ot, ot)
    assert exists( ot)
    if not optz.link_zagolemi_pootdelno and sum('zagolemi' in p for p in pfxs):
        pfxs = ['zagolemi']
    for pfx in pfxs:
        kym = join( optz.link_kym, pfx, ikym)
        ss = list( os.stat( ot) )   ## dict( size= ss[ stat.ST_SIZE], ..
        for ix in stat.ST_CTIME, stat.ST_NLINK:
            ss[ix] = None
        if kym in allfiles:
            old = allfiles[kym]
            print( old)
            print( ss)
            if old == ss:
                print( ' !ignore dup')
                return
        assert kym not in allfiles, kym
        allfiles[kym] = ss
        if not exists( kym):
            if optz.nothing: print( 'os.link', ot, kym)
            else:
                d = dirname( kym)
                if not os.path.isdir( d): os.makedirs( d)
                os.link( ot, kym )

def rename( ot, kym, *pfxs):
    ot = join( dir_ot, ot)
    assert exists( ot)
    kym = join( dirname( ot), kym)
    if not exists( kym):
        if optz.nothing: print( 'os.rename', ot, kym)
        else: os.rename( ot,kym)
    if optz.rename_alt:
        kymalt = ot+'.alt'
        if exists( kymalt):
            if optz.nothing: print( 'os.del', kymalt)
            else: os.remove( kymalt)
        kym = basename(kym)
        if optz.nothing: print( 'os.symlink', kym, kymalt)
        else: os.symlink( kym, kymalt)

dorename = optz.rename or optz.rename_alt
if not (optz.link_kym or dorename or optz.opis):
    optz.oparser.print_help()
    optz.oparser.error( 'deistvie?')


opisi = dict( (opis, open( opis).read()) for opis in (optz.opis or ()) )
def renopis( ot, kym, *pfxs):
    otf  = splitext( basename(ot))[0]
    kymf = splitext( basename(kym))[0]
    for k,opis in opisi.items():
        opisi[ k] = opis.replace( otf,kymf)

def rena2b( *a):
    if optz.opis: renopis( *a)
    if optz.link_kym: link( *a)
    elif dorename: rename( *a)

if len(args)<1:
    optz.oparser.error( 'ot') #print_help()
dir_ot = args[0]

exec( sys.stdin.read() ) #'ren-script')


for k,opis in opisi.items():
    print( k, opis)

# vim:ts=4:sw=4:expandtab

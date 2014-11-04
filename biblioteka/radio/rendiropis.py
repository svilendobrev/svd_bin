#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, io
import rec2dir
from svd_util.yamls import usability
from svd_util.struct import DictAttr
from svd_util import optz

'''
име:           Как щастието се скри в четирилистна детелина
автор:         ИринаКарадимчева
откъде:        ВзаП 20140801
издание:       радио
ориг_описание: >-
  „Как щастието се скри в четирилистна детелина“ от Ирина Карадимчева
ориг_рубрика:  Време за приказка

===>
hb-0801-1820+ВзаП+Как_щастието_се_скри_в_четирилистна_детелина--Ирина_Карадимч
'''

optz.bool( 'move',    help= 'преименувай към новото име')
optz.bool( 'link',    help= 'направи символна връзка = новото име')
optz.str(  'target',  help= 'къде да сложи горните')
#optz.str(  'prefix',  help= 'слага пред новото име')

optz,argz = optz.get()
for dir in argz:
    fn = dir + '/opis'
    print( '... ', dir)
    f = open(fn).readlines()
    f = [
            'автори_отделни: "'+ l.split(':',1)[-1].strip()+'"'
            if l.startswith( '#автори_отделни:')
            else l.rstrip()
            for l in f
        ]
    f = io.StringIO( '\n'.join( f))
        #f.replace( '\n#автори_отделни:', '\nавтори_отделни:' ))
    if 1:
        opis = dict( usability.load( f ) )
        ime = opis.get( 'име')
        ime = ime and str(ime)
        if not ime or not ime.strip('?'):
            ime = ''#l2c( os.path.basename( fn))
        #avtor_dylyg = opis.get( 'автор')
        avtor_dylyg = opis.get( 'автори_отделни')
        try:
            rubrika_kysa = (opis.get( 'откъде') or '').split()[0]
        except: rubrika_kysa = ''
        rubrika_orig = opis.get( 'ориг_рубрика')

    ime = rec2dir.filt_er( ime)
    if ime in (rubrika_kysa, rubrika_orig): ime = ''
    ldirname = rec2dir.filt_er( '--'.join( a for a in [ ime, avtor_dylyg, ] if a ))
    fname_kanal_vreme = dir.strip('/').split('/')[-1]
    ldirname = '+'.join( n for n in [
                    fname_kanal_vreme,
                    rubrika_kysa,
                    ldirname[:60] ]
                    if n )

    #if optz.prefix: ldirname = optz.prefix + ldirname

    cmd = print
    if optz.move: cmd = os.rename
    if optz.link: cmd = os.symlink
    if optz.target: ldirname = os.path.join( optz.target, ldirname)
    try:
        cmd( dir, ldirname)
    except FileExistsError as e:
        print( e)

# vim:ts=4:sw=4:expandtab

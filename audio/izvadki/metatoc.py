#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from svd_util import optz
optz.usage( '%prog [options] < metatoc-script-stdin')
optz.text( 'outpath2opispath', help= 'какво да се добави към outpath за да се стигне до .../opis')
optz.bool( 'opis', help= 'състави опис')
optz.bool( 'toc',  help= 'състави .toc за CDTEXT')
optz.bool( 'cyr2lat',   help= 'ако cd-toc приема само латиница')
opts,args = optz.get()

import sys
import os.path
from svd_util import struct, py3
dictOrder = py3.dictOrder
DictAttr = struct.DictAttr

#allitems = []
#paths = dictOrder()
albumi = dictOrder()

def add( *items, **ka):
    #global allitems
    for i in items:
        i = DictAttr( i)
        #allitems.append( i)
        path = i.path
        opis = os.path.join( path, opts.outpath2opispath or '', 'opis')
        i.opis = opis
        ialbum = i.album or i.title
        try:
            album = albumi[ ialbum]
            for k,v in ka.items():
                album[k] += v
        except KeyError:
            album = albumi[ ialbum] = DictAttr( album= ialbum, items= [], **ka)
        album.items.append( i)
        #paths.setdefault( i.path, []).append( i)

exec( sys.stdin.read() ) #*metatoc.py


opisi = dictOrder()
def daiopis(x):
    o = opisi.get(x)
    if not o:
        o = opisi[x] = open( x).read()
    return o

def opis():
    for a in albumi.values():
        print( '\nгрупа:', a.album)
        for n,i in enumerate( a.items):
            #opis = daiopis( i.opis)
            #print( i.fname, '==', i.title.replace(': ', ': '+str(1+n)+'.', 1 ))
            if i.title == a.album: t = ''
            else:
                t = i.title.split(':',1)[-1]
            print( i.fname, '==', '{групаномер}'+t )


from svd_util.minsec import sec2minsec, prnsec, minsec2sec
from svd_util import lat2cyr
def zaglavie(x): return x and x[0].upper() + x[1:]

def toc( cyr2lat =False):
    if 0:
        print( '''
CD_DA
 CD_TEXT {
  LANGUAGE_MAP { 0 : EN }
  LANGUAGE 0 {
    TITLE "Title"
    PERFORMER "Performer"
  } }
''')
    allsize = 0
    for a in albumi.values():
        print( '\n//group=', a.album )
        groupsize = 0
        for i in a.items:
            d = dict( i,
                pause   = i.pause and 'PREGAP 0:%(pause)s:0' % i or '',
                psecs   = prnsec( i.secs),
                )
            if cyr2lat:
                d['title'] = zaglavie( lat2cyr.zvuchene.cyr2lat( i.title))

            print( '''\
 TRACK AUDIO
  COPY
  CD_TEXT { LANGUAGE 0 {
    TITLE "%(title)s"
   } }
  %(pause)s
  FILE "%(fname)s" 0
  //size= %(psecs)s
  //secs= %(secs).1f
''' % d )
            ssize = i.secs + i.pause
            allsize += ssize
            groupsize += ssize
        print( '//groupsize=', prnsec( groupsize), a.album )
        print( '//allsize=', prnsec( allsize) )
    print( '\n//allsize=', prnsec( allsize) )

if __name__ == '__main__':
    if opts.toc:
        toc( opts.cyr2lat )
    else: opis()

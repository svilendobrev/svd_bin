#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

import sys, os, subprocess, argparse
if 0:
    from sumtim2 import filesize, minsec
    from svd_util import optz
    optz.help( '''\
     convert input audio files into output type, pcm16, resampling-down to 44100 if needed.
     inputs are renamed into *.org.whatever
     Преобразува входни звукови файлове към изходния формат, pcm16, сваляйки на 44100 ако трябва.
     Ако няма нужда от преобразуване, изхода е твърда връзка към входа.
     Изходящите файлове се казват като <вход-без-тип>.out.otype, и се презаписват ако ги има.
    ''')
    optz.text( 'otype', '-t', default= 'flac', help= 'изходящ формат, като flac wav mp3 .. виж sox -t')
    optz.bool( 'nothing', '-n', help= 'само наужким')
    #optz.bool( 'delete',    help= 'изтрива оригинала при успех (с еднакви продължителности)')
    optz,inputs = optz.get()
else:
    ap = argparse.ArgumentParser( description= '''\
 convert input audio files into output type, pcm16, resampling-down to 44100 if needed.
 inputs are renamed into *.org.whatever
 Преобразува входни звукови файлове към изходния формат, pcm16, сваляйки на 44100 ако трябва.
 Ако няма нужда от преобразуване, изхода е твърда връзка към входа.
 Изходящите файлове се казват като <вход-без-тип>.out.otype, и се презаписват ако ги има.
''') #, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    def apbool(*a,**ka): return ap.add_argument( action='store_true', *a,**ka)
    ap.add_argument( '--otype', '-t', default= 'flac', help= 'изходящ формат, напр. flac wav mp3 .. виж sox -t; подразбира се %(default)s')
    apbool( '--nothing', '-n',  help= 'само наужким')
    #apbool( '--delete',         help= 'изтрива оригинала при успех (с еднакви продължителности)')
    #apbool( '--force', '-f',   help= 'презаписва винаги')
    ap.add_argument( 'inputs', nargs='+', )
    optz = ap.parse_args()

otype = optz.otype
for fi in optz.inputs:
    info = subprocess.check_output( ['soxi', '-V0', fi ] ).decode( sys.stdout.encoding)
    print( info)
    info = dict( [x.lower().strip() for x in a.split(':',1)]
                    for a in info.strip().split('\n') )
    '''
    Input File     : 'hb/hb2016-1017-1820//vreme_za_pr--radio-20161017.18.15.01.44100.wav'
    Channels       : 2
    Sample Rate    : 44100
    Precision      : 16-bit
    Duration       : 00:20:34.26 = 54430925 samples = 92569.6 CDDA sectors
    File Size      : 218M
    Bit Rate       : 1.41M
    Sample Encoding: 16-bit Signed Integer PCM
    '''
    rate = info[ 'sample rate' ]
    enco = info[ 'sample encoding' ]

    name,ext = os.path.splitext( fi)
    fi2 = fi #name+'.org'+ext
    fo = name+'.out.'+otype
    doit = optz.nothing and print or subprocess.call
    sox = 'sox --temp .'.split()
    r = None
    if enco != '16-bit signed integer pcm' or int(rate) > 44100:
        #if doit: os.rename( fi, fi2)
        print(fo, rate, 'resample', otype)
        r = doit( sox + [ '-G', fi2, ]
                            + '-b 16 -e signed-integer -t'.split()
                            + [ otype, fo ]
                            + 'rate 44100 dither -s'.split() )
    elif ext != otype:
        #if doit: os.rename( fi, fi2)
        print(fo, rate, otype)
        r = doit( sox + [ fi2, '-t', otype, fo ] )
    else:
        print(fo, 'link')
        if doit: os.link( fi2, fo)
    print(fo, 'ok', r)

# vim:ts=4:sw=4:expandtab

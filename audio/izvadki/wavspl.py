#!/usr/bin/env python3
'''
extract pieces from .wav as of cutfile, as separate .wavs
+ makes a toc.py file
results are named (input-file-name).nomer.(piece-name)

grammar:
=========
input-file-name

piece1-name
fromtime -
fromtime - totime
         - totime
         - +deltatime

nopause
fps = float_framepersecond
offset= min:sec
scale= float_time_scaler
title= instead-of-input-file-name
'''

from cutter import Cutter
from svd_util import optz, struct, eutf

optz.usage( '''%prog cutfile
 cutfile can be - for stdin
''')
optz.bool( 'do_nothing', '-n')
optz.bool( 'verbose', '-v')
optz.bool( 'makedir', '-d')
optz.text( 'path',      help= 'out-path' )
optz.text( 'metafname', help= 'out-metadata-filename' )
optz.text( 'infile',    help= 'input .wav if not in cutfile' )
#optz.text( 'inpath',    help= 'path for input files if relative, default=dirname(cutfile)-or-.' )
#optz.text( 'encoding',  default='utf8', help= 'default=%default' )
optz.text( 'album',     help= 'common title of all inputs' )
optz.text( 'offset',    help= 'mm:ss.s or ssss.s' )
optz.add(  'fps',   type=float, default=1, help= 'frame-per-second float for time-as-frames, default=%default' )
optz.add(  'scale', type=float, default=1, help= 'float coef to scale the times' )

import sys, re
from os.path import dirname, join

from svd_util.minsec import sec2minsec, prnsec, minsec2sec

def zaglavie(x): return x and x[0].upper() + x[1:]

options,args = optz.get()


class Cutter( Cutter):

    def add2toc( me, **item):
        item = struct.DictAttr( item, album= options.album )
        me.toc.append( item)

    def save( me):
        me.toc = []
        super().save(
            maketoc = options.metafname,
            **options.__dict__
            )
        if me.toc: me.makemeta( me.toc)

    def walktoc( me, toc):
        groupsize = 0
        #re_intnum = re.compile( '\d*(\.(lp|mc|cd)(\.\d+)?)?[.:]\d+\.')  #end-of-wholename start-of-piecename
        src = None
        for item in toc:

            album = item.album or item.src
            album = album.strip("'")

            title = album
            if title: title += ': '
            title += item.name
            tfname = item.fname
            dname = dirname( tfname)

            album = zaglavie( album)
            title = zaglavie( title)
            pause = not item.nopause and 2 or 0
            src = item.src

            yield struct.DictAttr(
                album   = album,
                title   = title,
                pause   = pause,
                fname   = tfname,
                offset  = groupsize,    #
                secs    = item.size,

                nomer   = item.nomer,

                src     = src,
                path    = dname,
                )

            ssize = item.size + pause
            groupsize += ssize

        yield struct.DictAttr(
            groupsize   = groupsize,
            )

    mfnames = {}
    def mfile( me, what):
        name = getattr( options, what, None)
        if not name: return
        fl = 'w'
        if name[0]=='+':
            fl = 'a'
            name = name[1:]
        if me.mfnames.get( what) == name: fl = 'a'
        me.mfnames[ what] = name
        return eutf.filew_utf( name, fl)

    def makemeta( me, toc):
        f = me.mfile( 'metafname')
        if f is None: return
        with f:
            all = list( me.walktoc( toc))
            whole = all.pop(-1)
            f.write( '\n'.join( [
                '# -*- coding: utf8 -*-',
                'add( ',
                ]+[ '    '+repr(a)+',' for a in all ]+[
                '  %s= %r,'% kv for kv in whole.items() ]+[
                ' )',''
                ]))


#re_ext2wav = re.compile( '\.(wav|flac|mp3)')

params_re = [
    [ 'fps scale',   float, '[\d.]+'],
    [ 'offset',      minsec2sec, '[\d:]+' ],
#   [ 'offset0',     None , '[\d:.]+' ],  #minsec2sec
    [ 'album title', None,  '.+' ],
]
def assign_params( line):
    for keys,converter,patrn in params_re:
        oo = re.match( '('+ '|'.join( keys.split())+ ') *= *(' +patrn+ ')', line)
        if not oo: continue
        optname = oo.group(1)
        optvalue= oo.group(2)
        if converter: optvalue = converter( optvalue)
        setattr( options, optname, optvalue)
        print( optname,':', optvalue)
        return True

allsize = 0
cutter = None
for cutfile in args:
    print( 'new-cutfile=', cutfile)
    if cutfile=='-':
        options.inpath = '.'
        cutfile = sys.stdin
    else:
        options.inpath = dirname( cutfile)
        cutfile = open( cutfile)

    for c in eutf.readlines( cutfile):
        c = c.strip()
        if not c or c.startswith( '#'): continue
        if assign_params( c): continue
        if not c.replace( '=',''):  #only ===== ; force filename follows
            if cutter:
                cutter.save()
                cutter = None
            #print '======'
            options.infile = None
            continue
        if sum( c.endswith( '.'+ext) for ext in 'flac wav mp3'.split()):
            if cutter:
                cutter.save()
                cutter = None
            print( 'new-infile=', c)
            options.infile = c
            continue
        if not cutter: cutter = Cutter()
        if options.verbose: print( '<', c)
        cutter.readline( c)

    if cutter:
        cutter.save()
        cutter = None

# vim:ts=4:sw=4:expandtab

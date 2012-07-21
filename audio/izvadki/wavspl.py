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

from util import optz, struct, eutf
optz.usage( '''%prog cutfile
 cutfile can be - for stdin
''')
optz.bool( 'do_nothing', '-n')
optz.bool( 'verbose', '-v')
optz.bool( 'makedir', '-d')
optz.text( 'path',      help= 'out-path' )
optz.text( 'metafname', help= 'out-metadata-filename' )
optz.text( 'infile',    help= 'input .wav if not in cutfile' )
optz.text( 'inpath',    help= 'path for input files if relative, default=dirname(cutfile)-or-.' )
#optz.text( 'encoding',  default='utf8', help= 'default=%default' )
optz.text( 'album',     help= 'common title of all inputs' )
optz.text( 'offset',    help= 'mm:ss.s' )
optz.add(  'fps',   type=float, default=25, help= 'frame-per-second float for time-as-frames, default=%default' )
optz.add(  'scale', type=float, default=1,  help= 'float coef to scale the times' )

import sys, os, re
from os.path import basename, dirname, join, splitext, exists

from util.minsec import sec2minsec, prnsec, minsec2sec

def zaglavie(x): return x and x[0].upper() + x[1:]

options,args = optz.get()

offset = 0
if options.offset:
    offset = minsec2sec( options.offset)
    print( 'offset:', prnsec( offset))
opath = options.path

def point2sec( p):
    if ':' in p:
        s = minsec2sec(p)
        if options.scale and options.scale != 1:
            s *= options.scale
        return s
    return float(p)/float( options.fps)  #video frames

class Cutter:
    def __init__( me):
        me.cuts = []
        me.newcut()

    def newcut( me):
        me.start = me.end = None
        me.nopause = False
        me.name = ''

    def add( me):
        name = me.name
        #name = name.replace(' - ', '--').replace(' ','_')
        name = name.replace('/','--')
        rec = (name, me.start, me.end, me.nopause)
        if None not in rec:
            me.cuts.append( rec)
            me.newcut()
        elif rec[:3] != ('',None,None):
            print( ' ?what is this', ' '.join( str(s) for s in rec), '/infile=', me.infile)

    def readline( me, c):
        istime = False
        lr = c.split('-')
        if len(lr)==2:
            l,r = (s.strip() for s in lr)
            if l and l[0].isdigit():
                istime = True
                if me.end:
                    me.add()
                if not me.start:
                    me.start = l
                    me.end = None
            if r and re.match( '\+?\d+', r) and istime or not l:
                istime = True
                if r[0]=='+':
                    if not me.end: me.end = me.start
                    me.end += r
                else:
                    me.end = r
        if not istime:
            if c.lower() == 'nopause':
                me.add()
                me.nopause = True
            else:
                me.add()
                me.name = c

    def save( me):
        if me.end is None: me.end = '9999999:9'
        me.add()
        toc = me.write()
        if toc: me.makemeta( toc)

    def write( me):
        infile = me.infile
        if not infile.startswith( '/') and infile != options.infile: #relative
            infile = join( me.inpath, infile)

        if options.verbose:
            print( infile)
            for c in me.cuts: print( *c) #' '.join( str(s) for s in c))

        for a in infile, splitext( infile)[0]:
            a += '.wav'
            if exists( a):
                infile = a
                break
        else:
            print( '!!! nema go', infile)
            return

        import wave
        i = wave.open( infile, 'r')
        cur = 0
        params = (nchannels, sampwidth, framerate, nframes, comptype, compname) = i.getparams()
        #params = dict( (k, getattr(i, 'get'+k)()) for k in 'nchannels sampwidth framerate nframes comptype compname'.split() )
        #nframes = params['nframes']
        #framerate = params['framerate']
        size = nframes/float(framerate)
        #print nframes, framerate

        def sec2frames(sec):
            return int(sec * framerate)

        fname = ofile = basename( infile)    #no dirs
        for a in 'wav avi flac mp3'.split():
            if ofile.endswith( '.'+a): ofile = ofile[:-1-len(a)]
        if opath:
            try: os.makedirs( opath)
            except Exception as e: print( e)
            ofile = join( opath, ofile)
        if options.makedir:
            try: os.makedirs( ofile)
            except Exception as e: print( e)
            ofile += '/'
        else:
            ofile += '.'

        toc = []

        nfmt = len(me.cuts)>=10 and '%02d' or '%d'
        n=0
        oname = ''
        for name,start,end,nopause in me.cuts:
            #print '> %(name)r : %(start)s - %(end)s  %(nopause)s' % locals()
            nopause = nopause and 'nopause' or ''

            if not name:
                assert oname
                oname = oname + '.x'
            else:
                oname = name
            ss = point2sec( start)
            se = sum( point2sec(x) for x in end.split('+'))
            ss += offset
            se += offset
            fs,fe = [sec2frames(x) for x in (ss,se) ]
            print( ' ', oname, '>', prnsec(ss),':', prnsec(se), nopause)

            n+=1
            ooname = ofile + '.'.join( [ nfmt % n, oname, 'wav'] )
            print( '      ', ooname)
            toc.append( struct.DictAttr( album= options.album, nomer= n, src= ofile, name= oname,
                                fname= ooname, nopause= nopause,
                                size= se-ss,
                                ))

            if options.do_nothing and (not options.metafname or fe <= nframes): continue

            i.readframes( fs - cur) #skip
            data = i.readframes( fe - fs )
            cur = fe

            toc[-1].size = len(data)/float( nchannels* sampwidth *framerate)
            if options.do_nothing: continue

            o = wave.open( ooname, 'w')
            o.setparams( params)
            o.writeframes( data)
            o.close()
        return toc

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
    [ 'fps scale',  float,      '[\d.]+'],
    [ 'offset',     minsec2sec, '[\d:]+' ],
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
        Cutter.inpath = '.'
        cutfile = sys.stdin
    else:
        Cutter.inpath = dirname( cutfile)
        cutfile = open( cutfile)
    Cutter.infile = options.infile

    for c in eutf.readlines( cutfile):
        c = c.strip()
        if not c or c.startswith( '#'): continue
        if assign_params( c): continue
        if not c.replace( '=',''):  #only ===== ; force filename follows
            if cutter:
                cutter.save()
                cutter = None
            #print '======'
            Cutter.infile = None
            continue
        if sum( c.endswith( '.'+ext) for ext in 'flac wav mp3'.split()):
            if cutter:
                cutter.save()
                cutter = None
            print( 'new-infile=', c)
            Cutter.infile = c
            continue
        if not cutter: cutter = Cutter()
        if options.verbose: print( '<', c)
        cutter.readline( c)

    if cutter:
        cutter.save()
        cutter = None

# vim:ts=4:sw=4:expandtab

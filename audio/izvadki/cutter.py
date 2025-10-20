#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
extract pieces from .wav as of cutfile, as separate .wavs
results are named (input-file-name).nomer.(piece-name)

grammar:
=========

piece1-name
fromtime -
fromtime - totime
         - totime
         - +deltatime

nopause
offset0

'''

from svd_util.structs import DictAttr

import os, re
from os.path import basename, join, splitext, exists

from svd_util.minsec import sec2minsec, prnsec, minsec2sec
from svd_util.osextra import makedirs

def point2sec( p, scale =None, fps =1):
    if ':' in p:
        s = minsec2sec(p)
        if scale and scale != 1:
            s *= scale
        return s
    return float(p)/float( fps)  #frames-per-second

class Cutter:

    def __init__( me):
        me.cuts = []
        me.newcut()

    def newcut( me):
        me.start = me.end = None
        me.nopause = False
        me.name = ''

    offset0 = ''

    def add( me):
        me.offset0 = ''
        name = me.name
        #name = name.replace(' - ', '--').replace(' ','_')
        name = name.replace('/','--')
        rec = DictAttr( name= name or 'cut', start= me.start, end= me.end, nopause= me.nopause)
        if None not in rec.values():
            me.cuts.append( rec)
            me.newcut()
        elif not (me.start == me.end == None ): #name == '' and
            print( ' ?what is this', rec )#, '/infile=', me.infile)

    re_time = re.compile( '\+?\d+')

    def readline( me, c):
        istime = False
        lr = c.split('-')
        if len(lr)==2:
            l,r = (s.strip() for s in lr)
            if l and me.re_time.match(l): #[0].isdigit():
                istime = True
                if me.end:
                    me.add()
                if not me.start:
                    #if l[0] == '+':
                    #    l = me.start0 + l
                    me.start = l
                    if me.offset0: me.start += '+' + me.offset0
                    me.end = None
            if r and me.re_time.match( r) and istime or not l:
                istime = True
                if r[0]=='+':
                    if not me.end: me.end = me.start
                    me.end += r
                else:
                    me.end = r
                if me.offset0: me.end += '+' + me.offset0
        if not istime:
            if c.lower() == 'nopause':
                me.add()
                me.nopause = True
            elif c.lower() == 'offset0':
                me.offset0 = me.start
            else:
                me.add()
                me.name = ' '.join( a for a in [me.name, c] if a)

    def readcuts( me, c):
        print( '....:', c)
        isstart = True
        for t in c.split():
            #a- -b
            #a- b
            #a -b
            #a - b
            #: a- b c-d  --> раздели, и c-d в нов срез
            if t == '-':    #-
                isstart = False
                continue
            if isstart:
                if me.end or me.start: isstart = False
                if me.end and me.start: isstart = True
            #print( t, isstart)
            if '-' not in t:
                if me.re_time.match( t):  # a / b
                    if isstart: t = t+'-'
                    else: t = '-'+t

            me.readline( t)
            #assert me.name != t, t ???
            isstart = True


    def save( me, **kargs):
        if not (not me.name and me.start == me.end == None):
            if me.end is None: me.end = '9999999:9'
        me.add()
        me.write( **kargs)

    def add2toc( me, **item): pass

    def write( me,
            maketoc =False,
            scale   =1,
            fps     =1,
            offset  =0,
            do_nothing  =False,
            verbose     =False,
            makedir = False,
            path    = '',
            ofile   = None,
            ofile_as_sfx =None, #priority over ofile
            infile  = None,
            inpath  = '.',
            **kargs_ignore
            ):
        options = DictAttr( locals())

        if not infile.startswith( '/') :
            infile = join( inpath, infile)

        if options.verbose:
            print( infile)
            for c in me.cuts: print( ' '.join( k+'='+str(v) for k,v in c.items()))

        for a in infile, splitext( infile)[0]:
            a += '.wav'
            if exists( a):
                infile = a
                break
        else:
            print( '!!! nema go', a)
            return

        import wave
        i = wave.open( infile, 'r')
        cur = 0
        p = DictAttr()
        params = (p.nchannels, p.sampwidth, p.framerate, p.nframes, p.comptype, p.compname) = i.getparams()
        #size = p.nframes/float(p.framerate)
        #print nframes, framerate
        if verbose: print( '%sHz %s x %sbit' % (p.framerate, p.nchannels, p.sampwidth*8))

        def sec2frames(sec):
            return int(sec * p.framerate)

        ofile = basename( ofile or infile)    #no dirs
        for a in 'wav avi flac mp3'.split():
            if ofile.endswith( '.'+a): ofile = ofile[:-1-len(a)]
        if ofile_as_sfx: ofile += ofile_as_sfx
        opath = options.path
        if opath:
            makedirs( opath)
            ofile = join( opath, ofile)
        if options.makedir:
            makedirs( ofile)
            ofile += '/'
        else:
            ofile += '.'

        nfmt = len(me.cuts)>=10 and '%02d' or '%d'
        n=0
        oname = ''
        for rec in me.cuts:
            #print '> %(name)r : %(start)s - %(end)s  %(nopause)s' % rec
            nopause = rec.nopause and 'nopause' or ''

            if not rec.name:
                assert oname
                #oname = oname + '.x'   #има номерация и без това
            else:
                oname = rec.name
            ss = sum( point2sec( x, options.scale, options.fps ) for x in rec.start.split('+'))
            se = sum( point2sec( x, options.scale, options.fps ) for x in rec.end.split('+'))
            if options.offset:
                ss += options.offset
                se += options.offset
            fs,fe = [sec2frames(x) for x in (ss,se) ]
            print( ' ', oname, '>', prnsec(ss),':', prnsec(se), nopause)

            n+=1
            ooname = ofile + '.'.join( [ nfmt % n, oname, 'wav'] )
            print( '      ', ooname)

            if options.do_nothing and (not maketoc or fe <= p.nframes): continue

            skip = fs-cur
            while skip:
                sk = min( 9*60, skip)    #11mb/min
                i.readframes( sk)
                skip -= sk
            data = i.readframes( fe - fs )
            assert data
            cur = fe

            size = se-ss if fe <= p.nframes else len(data)/float( p.nchannels * p.sampwidth * p.framerate)
            me.add2toc( nomer= n, src= ofile, name= oname, fname= ooname, nopause= nopause, size= size,)

            if options.do_nothing: continue

            o = wave.open( ooname, 'w')
            o.setparams( params)
            o.writeframes( data)
            o.close()

#re_ext2wav = re.compile( '\.(wav|flac|mp3)')

if __name__ == '__main__':
    for l in '''
        1- -2           : 1,2
        3- 4            : 3,4
        5 -6            : 5,6
        7 - 8           : 7,8
        9- 10 11-12     : 9,10 11,12
        21- 22-  -23    : 21,23
        31- 32-  33     : 31,33
        41- 42- - 43    : 41,43
        51- 52- 54 - 55 : 51,55
        61- 62- -63 - 64: 61,64
        71- 72  73 - 74 : 71,72 73,74
        81- 82  83- 84  : 81,82 83,84

    '''.strip().split('\n'):
        inp,out = (a.strip() for a in l.split(':'))
        c = Cutter()
        c.readcuts( inp )
        c.add()
        res = [ [a.start, a.end] for a in c.cuts ]
        exp = [ a.split(',') for a in out.split() ]
        print( c.cuts )
        print( res,exp )
        assert res == exp


# vim:ts=4:sw=4:expandtab

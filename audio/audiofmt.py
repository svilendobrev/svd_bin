#!/usr/bin/env python
# -*- coding: utf-8 -*-
#$Id: audiofmt.py,v 1.2 2007-03-16 15:17:42 sdobrev Exp $

'is this abandoned extension of sumtim2.py ?????????'

import os, os.path
import subprocess, wave

class config:
    verbose = 0
    touch = 0
    wav =0
    mp3 =0

def output( *args):
#    print args
    return subprocess.Popen( args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]

def minsec( s):
    m = int(s/60)
    ss = s-m*60
    return '%(m)2d:%(ss)02.0f' % locals()
    return '%(m)2d:%(ss)4.1f = %(s).1fs ' % locals()


class fmt:
    def __init__( me, input, output ='', options= ()):
        me.input = input
        me.output = output
        me.options = options

    def time( me): raise NotImplementedError
    def multitime( me):
        r = 0
        for a in me.input:
            r += me.__class__( a).time
        return r
    def run( me, cmds):
        if not cmds: return
        if isinstance( cmds, str): cmds = [cmds]
        if not isinstance( cmds[0], (tuple,list)): cmds = [cmds]
        p = None
        for i in range( len(cmds)):
            c = cmds[i]
            assert isinstance( cmds, (tuple,list))
            if isinstance( c, str): c = c.split()
            #print c
            p = subprocess.Popen( c, stdin= p and p.stdout, stdout= i<len(cmds)-1 and subprocess.PIPE or None)
        #output = p.communicate()[0]
        p.wait()

    def wav( me):
        me.output = me.input + '.wav'
        me.run( me.towav())
    def towav( me):  raise NotImplementedError
    def fromwav( me):  raise NotImplementedError
    def mp3( me):
        me.output = me.input + '.mp3'
        me.run( me._mp3())
    def _mp3( me):
        return [ me.__class__( me.input, '-').towav(), mp3( '-', me.output).fromwav() ]

class wav( fmt):
    def time( me):
        i = wave.open( me.input, 'r')
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = i.getparams()
        i.close()
        return float( nframes) / float( framerate)
    def towav( me):     print 'wav to wav', me.input
    def fromwav( me):   print 'wav from wav', me.input
    def _mp3( me):
        return mp3( me.input, me.output)._mp3()

class mp3( fmt):
    def time( me):
        out = output( 'mp3info', '-p', '%m:%s', me.input )
        m,s = out.split(':')
        return 60*int(m) + float(s)
    def multitime( me):     #има ли нужда от това?
        out = output( 'mp3info', '-p', '%m:%s ', *me.input )
        r = 0
        for a in out.split():
            m,s = out.split(':')
            r += 60*int(m) + float(s)
        return r

    def towav( me):
        return 'lame -S --decode'.split() + [ me.input, me.output ]
    def fromwav( me):
        return 'lame --nohist'.split() + list( me.options) + [ me.input, me.output ]

class flac( fmt):
    def time( me):
        samples = output( 'metaflac', '--show-total-samples', me.input)
        rate = output( 'metaflac', '--show-sample-rate', me.input)
        return float( samples) / float( rate)
        #mplayer ID_LENGTH is 20% bigger!!
    def towav( me):
        return ['flac', '-d', me.input, '-o', me.output]
    def fromwav( me):
        return ['flac', me.input, '-o', me.output]

class ape( fmt):
    def time( me):
        out = output( 'macinfo', me.input)       #made by mac*/src/Examples/Sample1/
        for l in out.split('\n'):
            if 'Length of' in l:
                return float(l.split(':')[1].strip())
        assert 0, 'cant find size of '+me.input
    def towav( me):
        return [ 'mac', me.input, me.output, '-d' ]

class wv( fmt):
    def time( me):
        out = output( 'wvunpack', '-s', me.input)
        for l in out.split('\n'):
            if 'duration' in l:
                return float(l.split(':')[1].strip())
        assert 0, 'cant find size of '+me.input
    def towav( me):
        return [ 'wvunpack', me.input, '-o', me.output]

class mplayer( fmt):
    #греши за VBR mp3, Flac, ..?
    def time( me):
        out = output( *( 'mplayer -nosound -vc null -vo null -ao /dev/null -identify'.split() + [me.input]))
        for l in out.split('\n'):
            if 'ID_LENGTH' in l:
                return float(l.split('=')[1].strip())
        assert 0, 'cant find size of '+me.input
    def towav( me):
        return 'mplayer -nosound -vc null -vo null -ao'.split() + [ 'pcm:waveheader:fast:file='+me.output, me.input ]

mpegaudio = mplayer

__issubclass = issubclass
def issubclass( obj, klas):
    from types import ClassType
    return isinstance( obj, (type, ClassType)) and __issubclass(obj, klas)

ext2klas = dict( (k,v)
                    for k,v in locals().items()
                    if issubclass(v, fmt)
            )
#print ext2klas

def dirsize( curdir, config =config):
    total = 0
    if os.path.isdir( curdir):
        all = os.listdir( curdir)
    else:
        all = [ curdir ]
        curdir = None
    for fn in all:
        size = 0
        name,ext = os.path.splitext(fn)
        ext = ext[1:].lower()
        fp = curdir and os.path.join( curdir, fn) or fn
        klas = ext2klas.get( ext )
        if not klas: continue
        k = klas( fp)
        if config.mp3: k.mp3()
        elif config.wav: k.wav()
        else:
            size = k.time()
            if size:
                if config.verbose: print '+',minsec(size), fn
                total += size

    print '=',minsec(total), curdir or all[0]
    if config.touch and total:
        import time
        s = time.localtime()
        tm_year = s.tm_year
        tm_mon = tm_mday = 1
        tm_hour= int(total/3600)
        tm_min = int((total+29)/60)
        tm_sec = 0#int(total-tm_min*60)
        tm_wday= tm_yday= tm_isdst= -1

        s = tm_year, tm_mon, tm_mday,  tm_hour, tm_min, tm_sec,  tm_wday,tm_yday,tm_isdst
        tm = time.mktime(s)
        os.utime( curdir or all[0], (tm,tm) )
    return total

if __name__ == '__main__':
    import optz
    optz.add1( 'verbose',   '-v')
    optz.add1( 'touch',     '-t')
    optz.add1( 'mp3', )
    optz.add1( 'wav', )
    options,args = optz.get()

    total=0
    for curdir in (args or [os.getcwd()]):
        total += dirsize( curdir, config= options)

    print 'total:', minsec(total)

# vim:ts=4:sw=4:expandtab

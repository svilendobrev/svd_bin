#!/usr/bin/env python
from __future__ import print_function
import os, os.path
import subprocess, wave
class config:
    verbose = False
    mp3info = False
    bytesize = False

def output( *args):
    return subprocess.Popen( args, stdout=subprocess.PIPE).communicate()[0]

def minsec( s):
    m = int(s/60)
    ss = s-m*60
    return '%(m)3d:%(ss)02.0f' % locals()
    return '%(m)2d:%(ss)4.1f = %(s).1fs ' % locals()

def bytesize( size, show =True):
    if not show: return ''
    return '%5dM' % (size//1024//1024)

def filesize( fn, curdir =None, config =config):
    duration = 0
    name,ext = os.path.splitext(fn)
    ext = ext[1:].lower()
    fp = curdir and os.path.join( curdir, fn) or fn
    #if config.verbose>1: print( 'ext:', ext)
    try:
        sz = os.path.getsize( fp)
    except Exception as e:
        sz = None
        fn += ' : ' + str(e)
    if not sz:
        print( '? 0', fn)
        return 0,0
    if ext == 'flac':
        samples = output( 'metaflac', '--show-total-samples', fp)
        rate = output( 'metaflac', '--show-sample-rate', fp)
        duration = float( samples) / float( rate) #???
        #mplayer ID_LENGTH is 20% bigger!!
    elif ext == 'wav':
        i = wave.open( fp, 'r')
        params = (nchannels, sampwidth, framerate, nframes, comptype, compname) = i.getparams()
        duration = float( nframes) / float( framerate)
        i.close()
    elif ext == 'ape':
        out = output( 'macinfo', fp)       #made by mac*/src/Examples/Sample1/
        for l in out.split('\n'):
            if 'Length of' in l:
                duration = float(l.split(':')[1].strip())
                break
        else:
            assert 0, 'cant find duration of '+fn
    elif ext == 'wv':
        out = output( 'wvunpack', '-s', fp)
        for l in out.split('\n'):
            if 'duration' in l:
                duration = float(l.split(':')[1].strip())
                break
        else:
            assert 0, 'cant find duration of '+fn
    elif ext == 'ogg':
        out = output( 'ogginfo', fp)
        r = out.split( 'Playback length:')[1].strip().split()[0]
        m,s = r.split(':')
        m = m.strip('m')
        s = s.strip('s')
        duration = 60*int(m)+float(s)
    elif ext == 'mp3':
        duration = None
        #won't work for files made from joining multiples into one, via mp3wrap, qmp3join, mpgtx
        if 'MP3WRAP' not in fp and not config.mp3info:
            try:
                import mad
                mf = mad.MadFile( fp)
                track_length_in_milliseconds = mf.total_time()
                duration = track_length_in_milliseconds//1000
                mf = None
            except: pass
        if duration is not None: pass
        elif 10:
            out = output( 'mp3info', '-p', "%m %s", fp )
            m,s = out.split()
            duration = 60*int(m)+float(s)
        else:
            out = output( 'filmid.sh', fp)
            for l in out.split('\n'):
                if 'ID_LENGTH' in l:
                    duration = float(l.split('=')[1].strip())
                    break
            else:
                assert 0, 'cant find duration of '+fn

    elif ext in 'mpegaudio mpc wma'.split():
        out = output( 'filmid.sh', fp)
        for l in out.split('\n'):
            if 'ID_LENGTH' in l:
                duration = float(l.split('=')[1].strip())
                break
        else:
            assert 0, 'cant find duration of '+fn

    size = os.path.getsize( fp)
    if duration:
        if config.verbose:
            print( '+', minsec(duration), bytesize( size, config.bytesize), fn)
    return duration, size

def dirsize( curdir, config =config):
    total_time = total_size = 0
    if os.path.isdir( curdir):
        all = sorted( os.listdir( curdir))
    else:
        all = [ curdir ]
        curdir = None
    for fn in all:
        try:
            time,size = filesize( fn, curdir, config=config)
        except:
            print( '??', fn)
            raise
        total_time += time
        total_size += size

    print( '=', minsec( total_time), bytesize( total_size, config.bytesize), curdir or all[0])
    return total_time, total_size

if __name__ == '__main__':
    import sys
    import optparse
    oparser = optparse.OptionParser()
    def optany( name, *short, **k):
        return oparser.add_option( dest=name, *(list(short)+['--'+name.replace('_','-')] ), **k)
    def optbool( name, *short, **k):
        return optany( name, action='store_true', *short, **k)
    optany( 'verbose',  '-v', action='count', help= 'multiple to increase verbosity')
    optbool( 'mp3info', '-3', help= 'force use mp3info (instead of mad)')
    optbool( 'bytesize', '-s', help= 'show also bytesize')
    options,args = oparser.parse_args()

    total_time = total_size = 0
    for curdir in (args or [os.getcwd()]):
        time, size = dirsize( curdir, config= options)
        total_time += time
        total_size += size

    print( 'total:', minsec( total_time), bytesize( total_size, options.bytesize))

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
from __future__ import print_function
import os, os.path
import subprocess, wave

class config:
    verbose = False
    mp3info = False
    bytesize = False
    noffprobe = False

import sys#,locale
v3 = sys.version_info[0]>=3
#locale/stdout may fail on virtual terminals e.g. vim's output
#os.environ.get( 'LANG', '')
ENC = sys.stdout.encoding # locale.getpreferredencoding() or '',

def output( *args):
    try:
        r = subprocess.check_output( args, stderr=subprocess.STDOUT )
    except subprocess.CalledProcessError:
        return None
    if v3: r = r.decode( ENC)
    return r

DIGITS = 0
def minsec( s):
    m = int(s/60)
    ss = s-m*60
    return '{m:2d}:{ss:0{w}.{p}f}'.format( p=DIGITS, w=2+bool(DIGITS)+DIGITS, **locals())
    return '%(m)2d:%(ss)4.1f = %(s).1fs ' % locals()

def bytesize( size, show =True):
    if not show: return ''
    return '%5dM' % (size//1024//1024)

def fileduration( fp, ext =None):
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
    else:
        r = output( 'ffprobe', '-hide_banner', fp)
        duration = 0
        if r:
            for l in r.splitlines():
                l = l.strip()
                if 'Duration:' in l:
                    duration = l.split( 'Duration:')[-1].split(',')[0].strip()
                if l.startswith( 'Stream ') and ' Audio: ' in l: break
            else:
                duration = 0
            if duration and ':' in duration:
                h,m,s = duration.split(':')
                duration = float(s) + 60*int(m) + 60*60*int(h)
            else: duration=0
          #Duration: 00:22:23.41, start: 0.000000, bitrate: 773 kb/s
          #Duration: N/A, bitrate: 773 kb/s

    if 0: #ext in 'mpegaudio mpc wma'.split():
        out = output( 'filmid.sh', fp) #mplayer -vo null -ao null -frames 0 -msglevel identify=4 "$@" 2>/dev/null
        for l in out.split('\n'):
            if 'ID_LENGTH' in l:
                duration = float(l.split('=')[1].strip())
                break
        else:
            assert 0, 'cant find duration of '+fn

    return duration

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
    duration = fileduration( fp, config.noffprobe and ext or None)
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
    optbool( 'noffprobe', help= 'dont use ffprobe for all')
    optbool( 'mp3info', '-3', help= 'force use mp3info (instead of mad)')
    optbool( 'bytesize', '-s', help= 'show also bytesize')
    optany( 'rounddigits', type= int, default=0, help= 'digits after . in (sub)seconds')
    options,args = oparser.parse_args()
    DIGITS = options.rounddigits
    total_time = total_size = 0
    for curdir in (args or [os.getcwd()]):
        time, size = dirsize( curdir, config= options)
        total_time += time
        total_size += size

    print( 'total:', minsec( total_time), bytesize( total_size, options.bytesize))

# vim:ts=4:sw=4:expandtab

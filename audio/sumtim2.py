#!/usr/bin/env python
#$Id: sumtim2.py,v 1.6 2007-07-29 04:49:05 sdobrev Exp $
import os, os.path
import subprocess, wave
class config:
    verbose = False
    mp3info = False

def output( *args):
    return subprocess.Popen( args, stdout=subprocess.PIPE).communicate()[0]

def minsec( s):
    m = int(s/60)
    ss = s-m*60
    return '%(m)2d:%(ss)02.0f' % locals()
    return '%(m)2d:%(ss)4.1f = %(s).1fs ' % locals()

def filesize( fn, curdir =None, config =config):
    size = 0
    name,ext = os.path.splitext(fn)
    ext = ext[1:].lower()
    fp = curdir and os.path.join( curdir, fn) or fn
    #if config.verbose>1: print 'ext:', ext
    if not os.path.getsize( fp):
        print '? 0', fn
        return 0
    if ext == 'flac':
        samples = output( 'metaflac', '--show-total-samples', fp)
        rate = output( 'metaflac', '--show-sample-rate', fp)
        size = float( samples) / float( rate) #???
        #mplayer ID_LENGTH is 20% bigger!!
    elif ext == 'wav':
        i = wave.open( fp, 'r')
        params = (nchannels, sampwidth, framerate, nframes, comptype, compname) = i.getparams()
        size = float( nframes) / float( framerate)
        i.close()
    elif ext == 'ape':
        out = output( 'macinfo', fp)       #made by mac*/src/Examples/Sample1/
        for l in out.split('\n'):
            if 'Length of' in l:
                size = float(l.split(':')[1].strip())
                break
        else:
            assert 0, 'cant find size of '+fn
    elif ext == 'wv':
        out = output( 'wvunpack', '-s', fp)
        for l in out.split('\n'):
            if 'duration' in l:
                size = float(l.split(':')[1].strip())
                break
        else:
            assert 0, 'cant find size of '+fn
    elif ext == 'ogg':
        out = output( 'ogginfo', fp)
        r = out.split( 'Playback length:')[1].strip().split()[0]
        m,s = r.split(':')
        m = m.strip('m')
        s = s.strip('s')
        size = 60*int(m)+float(s)
    elif ext == 'mp3':
        size = None
        #won't work for files made from joining multiples into one, via mp3wrap, qmp3join, mpgtx
        if 'MP3WRAP' not in fp and not config.mp3info:
            try:
                import mad
                mf = mad.MadFile( fp)
                track_length_in_milliseconds = mf.total_time()
                size = track_length_in_milliseconds//1000
                mf = None
            except: pass
        if size is not None: pass
        elif 10:
            out = output( 'mp3info', '-p', "%m %s", fp )
            m,s = out.split()
            size = 60*int(m)+float(s)
        else:
            out = output( 'filmid.sh', fp)
            for l in out.split('\n'):
                if 'ID_LENGTH' in l:
                    size = float(l.split('=')[1].strip())
                    break
            else:
                assert 0, 'cant find size of '+fn

    elif ext in 'mpegaudio mpc wma'.split():
        out = output( 'filmid.sh', fp)
        for l in out.split('\n'):
            if 'ID_LENGTH' in l:
                size = float(l.split('=')[1].strip())
                break
        else:
            assert 0, 'cant find size of '+fn

    if size:
        if config.verbose: print '+',minsec(size), fn
    return size

def dirsize( curdir, config =config):
    total = 0
    if os.path.isdir( curdir):
        all = sorted( os.listdir( curdir))
    else:
        all = [ curdir ]
        curdir = None
    for fn in all:
        try:
            size = filesize( fn, curdir, config=config)
        except:
            print '??', fn
            raise
        total += size

    print '=',minsec(total), curdir or all[0]
    return total

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
    options,args = oparser.parse_args()

    total=0
    for curdir in (args or [os.getcwd()]):
        total += dirsize( curdir, config= options)

    print 'total:', minsec(total)

# vim:ts=4:sw=4:expandtab

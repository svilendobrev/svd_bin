# -*- coding: utf-8 -*-
##!/usr/bin/env python
from __future__ import print_function
from os.path import isdir, basename, exists, join, dirname, getmtime
from svd_util.osextra import execresult

class mp3times:

    @staticmethod
    def mp3info( fnames):
        ee = [ 'mp3info', '-r', 'a', '-p', '%S::%Q::%o::%r::%f\n' ] + fnames
        rr = execresult( ee )
        mtsec = {}
        for tf in rr.splitlines():
            t,sampling,mode,kbitrate,f = tf.split( '::', 4)
            mtsec[ f] = dict(
                time= int(t),
                mode= mode,
                sampling= int(sampling),
                kbitrate= kbitrate, #text!float
                )
        return mtsec

    @staticmethod
    def mad( fnames):
        try: import mad
        except:
            print( '!cant import mad for mp3-times')
            mp3times.mad = None
            return None
        mtsec = {}
        for fn in fnames:
            mf = mad.MadFile( fn)
            mtsec[ basename(fn)] = mf.total_time() //1000
            mf = None
        return mtsec

    @staticmethod
    def eyed3( fnames):
        try: import eyeD3       #python2 only
        except:
            print( '!cant import eyeD3 for mp3-times')
            mp3times.eyed3 = None
            return None
        mtsec = {}
        for fn in fnames:
            m = eyeD3.Mp3AudioFile( fn)
            mtsec[ basename(fn)] = m.play_time
        return mtsec

apps = 'mp3info mad eyed3'.split()
#apps = [ k for k in dir(mp3times) if not k.startswith('_')]    wrong order

def ftime(f): return getmtime(f) #os.path.getctime) stat( f).st_mtime

def sumer( durations_values):
    return sum(
        d['time'] if isinstance( d, dict) else d
        for d in durations_values
        )
def durations( dirpath, fnames, cache_file =None, durations =None, durations_time =0, force_app =None):
    if not fnames: return 0, {}
    tsec = None
    if not durations and cache_file and exists( cache_file):
        try:
            durations = eval( open( cache_file ).read().strip() )
        except: pass
        durations_time = ftime( cache_file)

    if durations and durations_time:
        if set( basename(f) for f in fnames) == set( durations.keys()):
            maxt = max( ftime( f ) for f in fnames)
            if durations_time >= maxt:
                tsec = sumer( durations.values())

    if force_app: assert force_app in apps

    mtsec = None
    for m in apps:
        if tsec is None or force_app==m:
            func = getattr( mp3times, m)
            if not func: continue
            durations = func( fnames)
            if durations is None: continue
            assert len(durations) == len(fnames)
            mtsec = sumer( durations.values())
            if tsec is None and cache_file:
                tsec = mtsec
                print( '>>', cache_file)
                with open( cache_file, 'w' ) as of:
                    of.write( '{' +
                        ', '.join( '%r:%s' % kv
                        for kv in sorted( durations.items()) )
                        +'}' )
            elif abs(mtsec-tsec) > 9*len(fnames):
                print( '! %(m)s.size %(mtsec)s != mp3.size %(tsec)s' % locals(), dirpath)

    return tsec, durations

# vim:ts=4:sw=4:expandtab

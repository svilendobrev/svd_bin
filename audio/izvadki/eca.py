# -*- coding: utf-8 -*-
from __future__ import print_function
import subprocess, os
import wave

def eca( ipath, opath, func, arg, resample= False, mono2stereo =True, typewav =False, fake =False, dbg =False ):
    def fixcomma(x):
        assert ',' not in x, x
        #if ',' in x: x = '`'+x+'`'     #in manpage... but no go
        return x
    if mono2stereo:
        w = wave.open( ipath)
        mono2stereo = w.getnchannels() == 1
        w.close()
    ipath = fixcomma( ipath )
    if resample:
        ipath = 'resample,auto,'+ipath
    if typewav:
        ipath = 'typeselect,.wav,'+ipath

    args = ['ecasound',
            '-i', ipath,
            '-o', fixcomma( opath ),
        ]
    if 'gain' in func:
        args += [ '-ea:'+str(int(100*arg)) ]
    if 'pitch' in func:
        args += [ '-ei:'+str(int(100*arg)) ]
    if mono2stereo:
        args += '-chcopy 1,2'.split()

    if dbg: print( ' '.join( '"'+a+'"' for a in args))
    if fake: return
    p = subprocess.Popen( args )
    return p and os.waitpid( p.pid, 0 )

# vim:ts=4:sw=4:expandtab

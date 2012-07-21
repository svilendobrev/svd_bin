# -*- coding: utf-8 -*-
import subprocess, os

def eca( ipath, opath, func, arg, resample= False, typewav =False, fake =False, dbg =False ):
    def fixcomma(x):
        assert ',' not in x, x
        return x
    ipath = fixcomma( ipath )
    if resample:
        ipath = 'resample,auto,'+ipath
    if typewav:
        ipath = 'typeselect,.wav,'+ipath

    args = ['ecasound',
            '-i', ipath,
            '-o', fixcomma( opath ),
        ]
    if func == 'gain':
        args += [ '-ea:'+str(int(100*arg)) ]
    elif func == 'pitch':
        args += [ '-ei:'+str(int(100*arg)) ]

    if dbg: print ' '.join( '"'+a+'"' for a in args)
    if fake: return
    p = subprocess.Popen( args )
    return p and os.waitpid( p.pid, 0 )

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
'''for each (directory gain-percent) tuple in input file,
   apply gain for files matching ipath into opath'''

import sys, subprocess, glob, re, os
def opt(x):
    try: sys.argv.remove( x ); return True
    except ValueError: return None
dbg = opt( '-debug')
fake= opt( '-fake')

from eca import eca
def ampl( name, koef, ipath, opath):
    return eca( ipath % locals(), opath % locals(), func= 'gain', arg= koef, resample= True, fake=fake, dbg=dbg)

if __name__ == '__main__':
    args = sys.argv[1:]

    ipath = 'wav/%(name)s.wav'
    if args: ipath = args[0]
    opath = 'wav/ampl.%(name)s.wav'
    if args[1:]: opath = args[1]

    for l in sys.stdin:
        l=l.strip()
        if not l or l.startswith('#'): continue
        x= l.split()
        name = x[0]
        koef0 = x[-1]
        koef = float(koef0)#/2
        print int(100*koef), name
        if '*' in ipath:
            ip = ipath % locals()
            ipr = re.compile( ip.replace( '*','(.*?)') )
            op = opath.replace( '*', '%(globname)s')
            for f in glob.glob( ip ):
                m = ipr.match( f)
                globname = m.group(1)
                ampl( name, koef, f, op % locals() )
        else:
            ampl( name, koef, ipath, opath)

# vim:ts=4:sw=4:expandtab

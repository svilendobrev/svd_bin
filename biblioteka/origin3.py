#$Id$
# -*- coding: utf-8 -*-
'''
P=`pwd`/.0
for a in *; do
    if [ -d $a/org/ ]; then
        echo $a
        cd $a/org
        for b in da.* ne.*; do
            md -p $P/$b
            ln -nsf ../../$a/org/$b $P/$b/$a
        done
        cd -
    fi
done
'''

import sys,os
from glob import glob
from os.path import join, split, isdir, realpath, exists, lexists, basename
from instr import meta_prevodi
from svd_util.lowercase import dict_lower
from svd_util import optz
optz.help( '%prog [опции] папка-изход  папки-входящи..')
optz.str( 'prevodi_meta',   help= 'файл-речник с преводи на понятия (lat=cyr) - хора..')
optz,args = optz.get()
out = args[0]
all = args[1:]

meta_prevodi = optz.prevodi_meta and meta_prevodi( optz.prevodi_meta, dict= dict_lower, nomer_stoinost=1) or {}

def ignored( f, org):
    if not isdir( f): return True
    if isdir( org): return False
    if glob( f+'/*.mp3'): return False
    return True

count = 0
for f in all:
    f = f.rstrip('/')
    rf = realpath( f)
    ro = realpath( out)
    common = os.path.commonprefix( [rf,ro])
    rf = rf[len(common):]
    ro = ro[len(common):]
    o2f = '../'*len(ro.split('/'))+rf

    org = join( f,'org')
    if ignored( f,org):
        print '?ignore', f
        continue
    empty = 1
    for i in glob( org+'/ne.*') + (glob( org+'/da.*') or [None] ):
        #print i
        if not i:
            oi = join( out, 'svd', 'da')
            dest = join( '..', o2f)
        else:
            if not isdir( i): continue
            ii = basename(i)
            dest = join( '..', o2f, 'org', ii)
            dane,aorg = ii.split('.',1)
            oi = join( out, meta_prevodi.get( aorg, aorg), dane)
        try: os.makedirs( oi)
        except: pass
        target = join( oi, basename(f) )
        #print target#, os.path.lexists(target)
        if lexists( target):
            #print exists, target
            os.remove( target)
        os.symlink( join( '..', dest), target)
        empty = 0
    if empty:
        print '????empty', f
    else:
       count += 1
print count

# vim:ts=4:sw=4:expandtab

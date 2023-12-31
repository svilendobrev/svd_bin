#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
обикаля ./ пропускайки папки 0/ , и търси папки в които има ./_tlf
 и копира *.mp3 в тях към целта, махайки междинни нива /mp3*/
'''

from os.path import join, exists, getsize
import sys, shutil, os
#import optz
def opt( *xx):
    for x in xx:
        if x in sys.argv: return sys.argv.remove( x ) or True
    return None

size_only = opt( '-s', '--size-only', '--size')
fake = opt( '-n', '--fake') or size_only
show_paths  = not opt( '-p', '--paths-hide', '--paths')
show_files  = not opt( '-f', '--files-hide', '--files')
show_exists = opt( '-e', '--exists-show', '--exists')
symlink     = opt( '-l', '--link', '--symlink')

start_path = '.'
if not size_only:
    target = sys.argv[1]
    assert target

invalids = '?*:\\'      #fat

# filedir/eventimestamp.py
#on FAT or FAT32 file systems, st_mtime has 2-second resolution, and st_atime has only 1-day resolution.
#so odd times will always appear newer than the FAT-copy
#hence: make them all even
def time( f):
    st = os.stat( f, follow_symlinks= True)
    time = st.st_mtime or st.st_ctime
    time = 2 * (time // 2)
    return time

cwd = os.getcwd()
sz_all = 0
for path,dirs,files in os.walk( start_path, followlinks= False):
    try: dirs.remove( '0' )
    except: pass
    if '_tlf' not in files: continue
    if not files: continue
    if not size_only:
        if show_paths: print( path)
        plevels = [ p for p in path.split('/')
                        if not p.startswith( 'mp3')
                        ]
        np = join( target, *plevels)
        for c in invalids:
            np = np.replace( c, '_')
        if not fake and not exists( np):
            os.makedirs( np, exist_ok= True)

    sz4path = 0
    for f in files:
        if not f.endswith( '.mp3'): continue
        fp = join( path, f)
        if size_only:
            sz = getsize( fp )
            if show_files: print( sz, fp)
            sz4path += sz
            continue
        nfp= join( np, f)
        for c in invalids:
            nfp = nfp.replace( c, '_')
        if exists( nfp):
            otime = time( fp)
            ntime = time( nfp)
            if show_exists: print( 'exist', nfp, otime, ntime)
            if otime <= ntime:
                continue
        if show_files:
            print( 'link:' if symlink else 'copy:', fp, '\n', nfp )    #yield
        if not fake:
            if symlink: os.symlink( join( cwd, fp), nfp)
            else: shutil.copy2( fp, nfp, follow_symlinks= True)
    if size_only and show_paths: print( sz4path, path)
    sz_all += sz4path

if size_only: print( sz_all)

# vim:ts=4:sw=4:expandtab

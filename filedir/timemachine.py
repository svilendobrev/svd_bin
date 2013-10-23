#!/usr/bin/env python
#sdobrev 2013
#copy fulltree of timemachine backups , symlinking the common (~hardlinked) dirs

#see http://hints.macworld.com/article.php?story=20080623213342356

from os.path import join
import os.path as ospath
import os, stat, shutil

from svd_util import optz, osextra
optz.list( 'exclude',    help= 'exclude filepattern (multiple)')
optz.list( 'include',    help= 'include filepattern (multiple)')
optz.list( 'direxclude', help= 'exclude dirpattern  (multiple)')
optz.list( 'dirinclude', help= 'include dirpattern  (multiple)')
optz.bool( 'dont',      '-n', help= 'dont actualy do anything')
optz.bool( 'verbose',   '-v', help= 'verbose')
optz.bool( 'linkusage', help= 'symlink used or unused links to archive/_used/ or _unused')
optz.text( 'orgarchive', help= 'path to the original hidden archive .HPF...')
optz.text( 'archive', help= 'archive-dir-name -instead of that hidden .HPF... [%DEFAULT]', default= '_archiv')
optz,argz = optz.get()

target  = argz.pop( -1)
archive = optz.archive

def match1( f, p):
    return fnmatch.fnmatch( f,p)
def match( f, patterns):
    for p in patterns:
        if match1( f, p): return True
def included( a, inc, exc):
    if inc and not match( a, inc): return
    if exc and match( a, exc): return
    return a
def levels( d): return d.strip('/').split('/')

used = set()
def walk( src):
    srcdepth = len( levels( src))
    for path,dirs,files in os.walk( src): #, followlinks= False):
        if not included( path, optz.dirinclude, optz.direxclude):
            dirs[:] = []
            continue
        path = path.replace( '//','/')
        path = path.replace( '//','/')
        nlevels = len( levels( path))
        #path2src = '../'*nlevels
        pathdeeper = levels( path)[ srcdepth:]
        mkdir = False
        for f in files:
            if not included( f, optz.include, optz.exclude ): continue
            if not mkdir:
                makedirs( join( target, path))
                #yield src, path
                mkdir = True
            pf = join( path, f)
            if ospath.islink( pf):
                l = os.readlink( pf)
                symlink( l, join( target, pf))
                continue
            s = os.lstat( pf)
            nlinks = s[ stat.ST_NLINK ]
            size   = s[ stat.ST_SIZE ]
            if nlinks >1000 and not size:
                dirlink = 'dir_%s' % nlinks
                symlink(
                    join( '../'*nlevels, archive, dirlink),
                    join( target, pf)
                    )
                used.add( dirlink)
            else:
                copy(
                    join( pf),
                    join( target, pf)
                    )

verbose = optz.verbose or optz.dont
def dbg(op,a):
    print '\n'+op, '\n > '.join( repr(x) for x in a)
def symlink( *a):
    if verbose: dbg( 'symlink', a)
    if optz.dont: return
    t = a[-1]
    if ospath.lexists(t) and ospath.islink(t) and os.readlink( t)==a[0]: return
    os.symlink( *a)
def makedirs( *a):
    if verbose or 1: dbg( 'makedirs', a)
    if not optz.dont: osextra.makedirs( *a)
def copy( *a):
    if verbose: dbg( 'copy', a)
    if optz.dont: return
    t = a[-1]
    if not(
        ospath.lexists(t)
        and ospath.isfile(t)
        and ospath.getsize( t) == ospath.getsize( a[0])
        ):
        shutil.copyfile( *a)
    shutil.copystat( *a)

print target
print archive
walk( argz[0])

if optz.linkusage:
    optz.dont = False   #HACK
    pused   = join( target, '_used')
    punused = join( target, '_unused')
    pmissing = join( target, '_missing')
    for p in pused, punused:
        makedirs( p)
    def symus( u, pu):
        symlink( join( '../../', archive, u), join( pu, u) )
    for u in used:
        symus( u, pused)
    if optz.orgarchive:
        orglinks = os.listdir( optz.orgarchive)
        for u in orglinks:
            if u not in used:
                symus( u, punused)
        missing = used - set( orglinks)
        if missing:
            makedirs( pmissing)
            for u in missing:
                symus( u, pmissing)

# vim:ts=4:sw=4:expandtab

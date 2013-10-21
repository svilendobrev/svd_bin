#!/usr/bin/env python

'''
301:
dir/file  = dir2/file2  -> dir2/file2
dir/file  = file2       -> dir/file2
dir/file  = dir2        -> dir2/the-only-mp3-file
dir/file  =             -> dir/the-only-mp3-file

410:
dir/file  = -

left/right column separator = can be just space if names has no spaces
dont-check !:
dir/file  = some/thing!
wont-check roots:
dir/file  = /d/i/r..

specials:
dir/        -> dir/(.*).mp3->dir/the-single.mp3
--singles   -> auto-apply above, for all ./dirs that have single mp3
'''
ext_equivs = 'mp3 wma ogg'.split()
import sys
from svd_util import optz
optz.text( 'base', help= 'base url')
optz.text( 'path', help= 'base filepath')
#optz.text( 'root', help=' root filepath, so root+ /base-url is valid filepath')
optz.bool( 'on',   help= 'RewriteEngine on')
optz.bool( 'singles',   help= 'for all ./dirs that have single mp3 inside, route dir/(.*).mp3->dir/the-single.mp3')
optz,args = optz.get()

#RewriteEngine on
if optz.on:   print 'RewriteEngine on'
if optz.base: print 'RewriteBase', optz.base

path = optz.path or ''

from os.path import splitext, exists, isdir, join, dirname, basename
from glob import glob

def ls( p, path =''):
    pp = join( path, p)
    if isdir( pp):
        mp3s = glob( pp+'/*.mp3')
        assert len( mp3s)==1, 'multiple mp3s: '+p
        #print >>sys.stderr, mp3s
        return mp3s[0][ path and len(path.rstrip('/'))+1 or 0:]

def singles( path =''):
    mp3s = glob( join( path, '*/*.mp3'))
    d = {}
    for m in mp3s:
        d.setdefault( dirname(m), []).append( m)
    for k,v in sorted( d.items()):
        if len(v)==1: yield v[0]

def esc( x):
    return x.replace( ' ', '\\ ')
def rule( l, r, code =301, flags ='', asfiles =True):
    l = esc(l)
    r = esc(r)
    if flags: flags = ','+flags
    if asfiles and '.*' in l or '.+' in l or '?' in l:
        print 'RewriteCond %{REQUEST_FILENAME} !-f'
    print 'RewriteRule ^%(l)s %(r)s [R=%(code)d%(flags)s]' % locals()

def manual( r):
    for a in 1,2,3,4,5:
        if '$'+str(a) in r: return True
    return False

def l_r( l,r, manual =False):
    #any -
    if r == '-':
        #print 'RewriteRule ^%(l)s(.*) $1 [R=410]' % locals()
        rule( l+'(.*)', '$1', code=410, flags='L', asfiles= False)
        return

    #dir dir
    if '/' not in l or l.endswith('/'):
        l = l.rstrip('/')
        r = r.rstrip('/')
        #print 'RewriteRule ^%(l)s($|/.*) %(r)s$1 [R=301]' % locals()
        rule( l+'(|/.*)$', r+'$1', asfiles= False)
        return r,isdir

    #dir/file  dir
    if '/' in l and r.endswith('/'):
        r += basename( l)
    else:
        rr = ls( r, path)
        if rr:
            r = rr
            #print >>sys.stderr, 444444
        else:
            #dir/file  file
            if '/' not in r: r = join( dirname( l), r)

    if not manual:
        lext = splitext( l)[1]
        rext = splitext( r)[1]
        if lext != rext: #dir/file.mp3  file
            #print >>sys.stderr, lext, rext
            if lext[1:] not in ext_equivs or rext[1:] not in ext_equivs:
                r = r + lext
    rule( l, r)
    return r,exists

for a in sys.stdin:
    a = a.strip()
    if not a or a[0]=='#': continue
    if '=' in a:
        lr = a.split( '=')
    else:
        lr = a.rsplit( None,1)
    if len(lr)==2:
        l,r = (x.strip() for x in lr)
    else:
        l = a
        r = ''

    if l and r:
        dontcheck = l.startswith('!')
        if dontcheck: l = l[1:].strip()
        else:
            dontcheck = manual(r)
        #print >>sys.stderr, 111111, l, r, dontcheck
        try:
            x = l_r( l,r, dontcheck)
        except:
            print >>sys.stderr, '!!!!!', l, r, dontcheck
            raise
        if x:
            r,checker = x
            if r.startswith('/') or dontcheck:
                if not dontcheck: print >>sys.stderr, 'cant check', r
            else:
                #r+='4'
                if path: r = join( path, r)
                assert checker( r), (checker.__name__, r,l)
        continue

    if not l.endswith('.mp3') and not l.endswith('/'):
        print >>sys.stderr, '? ignore', l
        continue

    if not optz.singles:
        #single wrong dir+filename, try guess
        p = dirname(l)
        #print >>sys.stderr, p
        r = ls( p, path)
        if r:
            if l.endswith('/'):     #dir: route anything into the guess one
                print 'RewriteCond %{REQUEST_FILENAME} !-f'
                l += '.+\.mp3'
            rule( l, r, flags='L')
            continue

    print >>sys.stderr, '? wrong path', l

if optz.singles:
    for m in singles( path):
        f = m[ len(path):].strip('/')
        p = dirname(f)
        #print 'RewriteCond %{REQUEST_FILENAME} !-f'
        l = join( p, '.+\.mp3')
        rule( l, f, flags='L')

# vim:ts=4:sw=4:expandtab

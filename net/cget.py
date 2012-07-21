#!/usr/bin/env python
#$Id: cget.py,v 1.1 2006-01-10 12:15:22 sdobrev Exp $

import re,sys,time
import os.path

re_href = re.compile( '(?P<type>a|base)\s*href\s*=\s*"(?P<url>[^"]+)"', re.IGNORECASE )
class cfg:
    base = ''
    filters = [ re.compile( '^javascript:' ) ]
    nop = False
    cargs = [ 'curl',
                '-C', '-',  #continue if needed
                '-O',       #autoname = file part of url
                '-f',       #fail on protocol/http-errors
            ]
    verbose = 0
    retryafter = 0

def findurls( html):
    for m in re_href.finditer( html):
        type = m.group('type').lower()
        url  = m.group('url')
        if not type or not url:
            print 'cant subparse', m.group(0)
            continue
        ignore = 1
        for f in cfg.filters:
            if f.search( url):
                if cfg.verbose: print ' ignore:', url
                break
        else: ignore=0
        if ignore: continue

        if type=='base':
            cfg.base = url
            continue

        if 'http:' not in url.lower():
            url = cfg.base + url
        yield url

def arg( a, patern):
    if isinstance( patern, str):
        patern = ( patern,)
    for patrn in patern:
        if a.startswith( patrn):
            if not patrn.endswith('='): return True
            return a[ len( patrn): ]
    raise IndexError

help = """
cget [-nop] [-filter=patrn] [-base=url] [-r[etryafter]=sec's] html-file [-all-others-passed-down]
download (curl) all not.ok-yet href's in html, stops at first (protocol or else) failure
"""

input = None

for a in sys.argv[1:]:
    if input:    #exe option
        cfg.cargs.append( a)
        continue

    if not a.startswith('-'):
        input = a
        continue

#my option
    try:
        if (arg( a, '-h')):
            raise SystemExit, help
    except IndexError: pass
    try:
        cfg.nop = arg( a, '-nop')
        continue
    except IndexError: pass
    try:
        cfg.filters.append( re.compile( arg( a, '-filter=') ) )
        continue
    except IndexError: pass
    try:
        cfg.base = arg( a, '-base=')
        continue
    except IndexError: pass
    try:
        cfg.retryafter = int( arg( a, ('-r=', '-retry=', '-retryafter=', ) ))
        continue
    except IndexError: pass

    raise SystemExit, 'unknown arg '+repr(a)+help
    #cfg.cargs.append( a)
    #continue

if not input:
    raise SystemExit, help


if cfg.verbose: print 'parse', a
html = file( input).read()

okdir = 'ok/'
for url in findurls( html):
    if cfg.verbose: print 'target:', url
    target = os.path.basename( url)
    okfile = target + '.ok'
    if os.path.exists( okfile): continue
    if os.path.exists( okdir+okfile): continue
    cargs = cfg.cargs + [ url ]
    if cfg.nop:
        cargs = [ 'echo'] + cargs

    while 1:
        print ' '.join( cargs)
        r = os.spawnvp( os.P_WAIT, cargs[0], cargs )
        if cfg.nop: break
        if r==0:
            out = file( target).read( 1000)
            r = 'access denied'
            if r not in out.lower():
                try:
                    os.mkdir(okdir)
                except OSError:
                    pass
                try:
                    file( okdir+okfile,'w').write(' ')
                except IOError:
                    file( okfile,'w').write(' ')
                break
            os.rename( target, target + '.err')
        print 'err =', r
        if not cfg.retryafter:
            print 'STOP'
            raise SystemExit, r
        print 'retryafter', cfg.retryafter, 's..'
        time.sleep( cfg.retryafter )
        print time.asctime()


# vim:ts=4:sw=4:expandtab

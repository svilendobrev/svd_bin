#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

import pyquery
from pyquery.openers import url_opener
FILE = 'file://'
def opener( url, ienc =None, **ka):
    if url.startswith( FILE):
        url = url[ len(FILE): ]
    else:
        return url_opener( url, ka)

    import io
    d = io.open( url, 'rb').read()
    if not ienc:
        import chardet  #chardet.feedparser.org, python3-chardet, python-chardet
        ienc = chardet.detect( d)[ 'encoding']   #.confidence
    d = d.decode( ienc)
    return d


from svd_util.struct import DictAttr
from svd_util import optz
optz.text( 'url', default ='http://pozvanete.bg/imoti-prodava-offline&maxAds=100?page={npage}')
optz.int(  'pages', default=11)
optz.list( 'includes_info', )
optz.list( 'excludes_name', )
optz.bool( 'load')
optz.bool( 'save')
optz.bool( 'io', help='load+save')
optz.text( 'fload', default ='danni.pozv', help= '[%default]')
optz.text( 'fsave', default ='danni.pozv', help= '[%default]')
optz.bool( 'allprn', '-a', help ='всички, а не само новите')
optz.text( 'merge',  help ='смеси тези данни')

def oprosti( t):
    return tuple( t.replace(',',' ').lower().split() )

neinfo = set(['гр.'])

def get( url, info_includes, text_excludes, ienc ='utf-8', ads =None):
    if ads is None: ads = {}
    n=0
    for i in range( optz.pages):
        #p = pyquery.PyQuery( url= url % i , ienc= enc)
        print( url.format( npage= i))
        try:
            p = pyquery.PyQuery( url= url.format( npage= i), opener= opener, ienc= ienc)
        except Exception as e:
            print( e)
            break
        #for a in p( 'ul.offline-list promo-products') + p( 'ul.offline-list promo-products') + :
        for ul in p.items( 'ul.offline-list'):
            for li in ul.items( 'li'):
                #print( li)
                n+=1
                ad = DictAttr( (a, (list(li.items( 'div.offline-list-' +a))[0].text() or '').replace('\xA0', ' ').strip() )
                        for a in 'name info phones'.split()
                        )
                ad.info   = set( oprosti( ad.info) )
                ad.phones = set( oprosti( ad.phones) )
                name = oprosti( ad.name)
                if ignored( ad, name, info_includes, text_excludes):
                    continue
                if merge1( ads, ad, name): continue

    print(n)
    return ads

def merge1( ads, ad, name):
    b = ads.get( name)
    if b:
        b.phones.update( ad.phones)
        b.info.update( ad.info)
        return True
    ads[ name ] = ad

def merge( ads, adsi):
    novi = []
    for name, ad in adsi.items():
        if merge1( ads, ad, name): continue
        novi.append( ad)
    return novi

def ignored( ad, name, info_includes, text_excludes):
    ad.info -= neinfo
    return ( info_includes and not any(
                        x in ad.info for x in info_includes)
            or
         text_excludes and any(
                        name[0].startswith( x[1:]) if x[0]=='^' else x in name
                        for x in text_excludes)
        )

def clean( ads, info_includes, text_excludes):
    for name,ad in list( ads.items() ):
        if ignored( ad, name, info_includes, text_excludes):
            #print( 'del', name)
            del ads[ name ]

def info2dati( info):
    return set( datetime.date( *time.strptime( x, '%d.%m.%Y')[:3])
                for x in info if x[0].isdigit() )


def prn( ads, novi, lastdate =None):
    if isinstance( ads, dict): ads = ads.values()
    if not ads: ads = novi
    novi = set( ad.name for ad in novi )

    if lastdate: lastdate = set( [ lastdate ])
    #multiples of same phone
    ad_by_ph = {}
    for ad in ads:
        ad.novo = (ad.name in novi) * '*'
        if info2dati( ad.info) == lastdate:
            ad.novo += '#'
        ad_by_ph.setdefault( tuple( sorted(ad.phones)), []).append( ad)
        ad.ixp = ''
    ixp = 1
    for adp in ad_by_ph.values():
        if len(adp) > 1:
            for ad in adp: ad.ixp = ixp
            ixp+=1

    def px( ad, pfx=''):
        pa = ad.novo.ljust(2), pfx+bool(pfx)*' ' + ad.name, '|', ' '.join( ad.phones), '/', ' '.join( ad.info)
        print( *pa)#((pfx and (pfx,) or ()) + pa))

    for ad in sorted( ads, key= lambda v: v.name ):
        if ad.ixp:
            pfx = '+'
            for a in sorted( ad_by_ph.pop( tuple( sorted(ad.phones)), ()), key= lambda v: v.name ):
                px( a, pfx)
                pfx = '-'
        else:
            px( ad)

import datetime, time
import pprint, sys, os
def save( ads, fname):
    if os.path.exists( optz.fsave):
        os.rename( optz.fsave, optz.fsave+'.1')
    print( '>', fname, file=sys.stderr)
    pprint.pprint( dict( v=list( ads.values()), t=datetime.datetime.now().isoformat() ), stream= open( fname, 'w') )

def load( fname):
    r = eval( open( fname).read() )['v']
    return dict( (oprosti( ad['name']), DictAttr( ad)) for ad in r )

def textlist( tlist, default = ()):
    tlist = tlist or default or ()
    if isinstance( tlist, str): tlist = tlist.lower().split()
    else: tlist = [ a.lower().strip() for a in tlist]
    return tlist

def main( info_includes =None, text_excludes =None):
    global optz
    optz,argz = optz.get()
    if optz.io: optz.load = optz.save = True
    url = argz and argz[0] or optz.url
    info_includes = textlist( optz.includes_info, info_includes)
    text_excludes = textlist( optz.excludes_name, text_excludes)
    if optz.merge:
        adsnovi = load( optz.merge)
    else:
        adsnovi = url and get( url = url,
                    info_includes = info_includes,
                    text_excludes = text_excludes,
                    ) or {}
    ads = optz.load and load( optz.fload) or {}
    ads0 = pprint.pformat( ads)
    for a in ads, adsnovi:
        clean( a,
                    info_includes = info_includes,
                    text_excludes = text_excludes,
        )
    novi = merge( ads, adsnovi)
    if ads0 != pprint.pformat( ads) and optz.save:
        save( ads, optz.fsave)

    infos = set()
    for a in ads.values(): infos.update( a.info )
    last = infos and max( info2dati( infos )) or None
    prn( optz.allprn and ads, novi, lastdate=last)

if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:expandtab

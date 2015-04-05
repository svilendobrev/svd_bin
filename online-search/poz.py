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
optz.text( 'includes_info', )
optz.text( 'excludes_name', )

def get( url, info_includes, text_excludes, ienc ='utf-8'):
    ienc = 'utf-8'
    ads = {}
    for i in range(15):
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
                ad = ( DictAttr( (a, (list(li.items( 'div.offline-list-' +a))[0].text() or '').replace('\xA0', ' ').strip() )
                    for a in 'name info phones'.split()
                    ))
                if not info_includes or any( x.lower() in ad.info.lower() for x in info_includes.lower().split()):
                    b = ads.get( ad.name.lower())
                    if b:
                        assert b.phones == ad.phones
                        continue
                    if text_excludes and any( x.lower() in ad.name.replace(',',' ').lower().split() for x in text_excludes.lower().split()):
                        continue
                    ads[ ad.name.lower() ] = ad
    #        break

    for k,ad in sorted( ads.items()):
        print( ad.name, ad.phones)

if __name__ == '__main__':
    optz,argz = optz.get()
    get( url = argz and argz[0] or optz.url,
         info_includes = optz.includes_info,
         text_excludes = optz.excludes_name,
         )
# vim:ts=4:sw=4:expandtab

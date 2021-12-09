#!/usr/bin/env python
from __future__ import print_function

import sys
try:
    from urllib.parse import unquote_plus, unquote, urlparse, parse_qs
except:
    from urllib import unquote_plus, unquote
    from urlparse import urlparse, parse_qs

class optz: pass
for o in 'cp1251 quoted keepplus dict'.split():
    v = True
    try: sys.argv.remove( o)
    except: v= False
    setattr( optz, o, v)

unquote = optz.keepplus and unquote or unquote_plus

def tx(a):
    a = unquote( a.rstrip())
    if 'q=%' in a: a = unquote( a.rstrip())#tx(a)
    if optz.cp1251: return a.decode('cp1251', 'ignore')
    return a #.decode('utf-8', 'ignore') #.encode('cp1251', 'ignore')

for a in sys.stdin:
    a = a.rstrip()
    if optz.quoted:
        qq = a.split('"')
        pp = []
        for i,x in enumerate(qq):
            if i % 2: x = tx(x)
            pp.append(x)
        a = '"'.join( pp)
    else:
        a = tx(a)
    #if 'q=%' in a: a = tx(a)
    if optz.dict:   #TODO maybe do this before unquote-ing, then unquote items ??
        import pprint
        a = urlparse( a)._asdict()
        a['query'] = parse_qs( a['query'])
        pprint.pprint( a, sort_dicts=False )
        continue
    print( a)

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
from __future__ import print_function

import sys
try:
    from urllib import unquote_plus, unquote
except:
    from urllib.parse import unquote_plus, unquote

class optz: pass
for o in 'cp1251 quoted keepplus'.split():
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
    print( a)

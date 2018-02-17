#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import sys
if not hasattr( __builtins__, 'unicode'):
    unicode = str

#booleans only:
def opt( *xx):
    for x in xx:
        if x in sys.argv: return sys.argv.remove( x ) or True
    return None

o_utf8 = opt('-8', '--utf', '--utf8')
i_utf8 = opt('-i8', '--iutf', '--iutf8')
nodecode = opt('-D', '--no-decode')     # in very rare cases, e.g. msoffice-created-mail

ENC = i_utf8 and 'utf8' or 'cp1251'
def enc( s,e):
    if not isinstance( s, unicode):
        if not e or e=='ascii': e=ENC
        s = s.decode( e, 'ignore')   #unicode( s,e,'ignore')
    if o_utf8: s = s.encode( 'utf8')
    return s

from email import message_from_file, header, utils
posti = []
for a in sys.argv[1:]:
    m = message_from_file( open(a) )
    posti.append( m)
posti.sort( key= lambda m: utils.parsedate( m['Date']) )

for m in posti:
    print( '\n'*2)
    print( '='*80)
    print( '\n'*2)
    for k in 'Date From To Subject CC'.split():
        v = m[k]
        if not v: continue
        d = header.decode_header(v)
        print( k,':', *( enc(s,e) for s,e in d))

    for m in m.walk():
        e = m.get_charset() or m.get_charsets()[0]
        txt = m.get_payload( decode= not nodecode)
        if txt: print( enc( txt, e))

# vim:ts=4:sw=4:expandtab

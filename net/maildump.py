#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import sys
import os
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
tree     = opt('--tree')

ENC = i_utf8 and 'utf8' or 'cp1251'
def enc( s,e):
    if not isinstance( s, unicode):
        if not e or e=='ascii': e=ENC
        s = s.decode( e, 'ignore')   #unicode( s,e,'ignore')
    if o_utf8: s = s.encode( 'utf8')
    return s

from email import message_from_file, header, utils
import mimetypes
posti = []
for a in sys.argv[1:]:
    m = message_from_file( open(a) )
    posti.append( (m,a))
posti.sort( key= lambda ma: utils.parsedate( ma[0]['Date']) )

for m,a in posti:
    print( '\n'*2)
    print( '='*80)
    print( '\n'*2)
    if tree: os.makedirs( a+'.dir', exist_ok=True)
    for k in 'Date From To Subject CC'.split():
        v = m[k]
        if not v: continue
        d = header.decode_header(v)
        ka = {}
        if tree:
            ka = dict( file= open( a+'.dir/headers', 'w'))
        print( k,':', *( enc(s,e) for s,e in d), **ka)

    n = 0
    for part in m.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        n+=1
        e = part.get_charset() or part.get_charsets()[0]
        txt = part.get_payload( decode= not nodecode)
        if not txt: continue
        filename = 'p'+str(n)+ (part.get_filename() or '')
        ext = mimetypes.guess_extension( part.get_content_type())
        if not tree:
            print( enc( txt, e), )
        else:
            with open( a+'.dir/'+filename, 'wb') as fo:
                fo.write( txt)

# vim:ts=4:sw=4:expandtab

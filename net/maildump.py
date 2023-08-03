#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os
if not hasattr( __builtins__, 'unicode'):
    unicode = str

import optparse
oparser = optparse.OptionParser()
def optany( name, *short, **k):
    return oparser.add_option( dest=name, *(list(short)+['--'+name.replace('_','-')] ), **k)
def optbool( name, *short, **k):
    return optany( name, action='store_true', *short, **k)

optbool( 'utf8', '-8', help= 'output as utf8')
optbool( 'iutf8', help= 'input as utf8')
optbool( 'no_decode', '-D', help= 'do not decode - in very rare cases, e.g. msoffice-created-mail')
optbool( 'tree', help= 'make subtree of attachments')
optbool( 'date', help= 'rename by date')
opts,args = oparser.parse_args()

ENC = opts.iutf8 and 'utf8' or 'cp1251'

def enc( s,e):
    if not isinstance( s, unicode):
        if not e or e=='ascii': e=ENC
        s = s.decode( e, 'ignore')   #unicode( s,e,'ignore')
    if opts.utf8: s = s.encode( 'utf8')
    return s

from email import message_from_file, header, utils
import mimetypes
posti = []
for a in args:
    m = message_from_file( open(a) )
    posti.append( (m,a))
posti.sort( key= lambda ma: utils.parsedate( ma[0]['Date']) )

for m,a in posti:
    print( '\n'*2)
    print( '='*80)
    print( '\n'*2)
    if opts.tree:
        dirname = a
        if opts.date:
            dt = utils.parsedate_to_datetime( m['Date'])
            dirname += '-'+dt.isoformat()
        dirname += '.dir'
        os.makedirs( dirname, exist_ok=True)
    hdrs = {}
    for k in 'Date From To Subject CC'.split():
        v = m[k]
        if not v: continue
        d = header.decode_header(v)
        hdrs[ k] = [ enc(s,e) for s,e in d ]
    if opts.tree:
        with open( dirname+'/headers', 'w') as fo:
            for k,vv in hdrs.items(): print( k,':', *vv, file=fo)
    else:
            for k,vv in hdrs.items(): print( k,':', *vv)

    n = 0
    for part in m.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        n+=1
        e = part.get_charset() or part.get_charsets()[0]
        txt = part.get_payload( decode= not opts.no_decode)
        if not txt: continue
        filename = part.get_filename() or ''
        if filename:
            fname, charset = header.decode_header( filename )[0]
            if charset:
                filename = fname.decode( charset)
        filename = 'p' + str(n) + filename
        ext = mimetypes.guess_extension( part.get_content_type())
        if not opts.tree:
            print( enc( txt, e), )
        else:
            with open( dirname+'/'+filename, 'wb') as fo:
                fo.write( txt)

# vim:ts=4:sw=4:expandtab

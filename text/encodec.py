#!/usr/bin/env python
#$Id: encodec.py,v 1.3 2007-03-28 07:19:29 sdobrev Exp $

import codecs
import sys
if len(sys.argv)<3:
    print 'use as filter: enc2enc [-]input-encoding [-]output-encoding <input >output'
    print '  the -enconding will reverse text'
    raise SystemExit
e_from = sys.argv[1]
e_to = sys.argv[2]
reverse = False
if e_from[0]=='-':
    e_from = e_from[1:]
    reverse = not reverse
if e_to[0]=='-':
    e_to= e_to[1:]
    reverse = not reverse
fi = codecs.getreader( e_from)( sys.stdin, errors='replace')
fo = codecs.getwriter( e_to)( sys.stdout, errors='replace')
for l in fi:
    if reverse:
        a = list(l)
        a.reverse()
        l = ''.join(a)
    fo.write( l)

# vim:ts=4:sw=4:expandtab

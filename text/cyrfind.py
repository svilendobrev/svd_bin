#!/usr/bin/env python
import re,sys
import eutf
enc = eutf.e_utf_stdout() and 'utf-8' or 'cp1251'
r = sys.argv.pop(1).decode( enc)
#print r, sys.argv
rx = re.compile( r)
for f in sys.argv[1:]:
    for a in eutf.readlines( file(f)):
        if rx.search( a): print f,':',a

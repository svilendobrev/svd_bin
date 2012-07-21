#!/usr/bin/env python
#$Id$

import sys
level=0
prev=None
url =0
exclude = 'ID VISITED CREATED EXPANDED ACTIVE ICONFILE DESCRIPTION UNIQUEID'.split()
dotree = '-notree' not in sys.argv
for l in sys.stdin:
    l = l.strip()
    if not l: continue
    if l.split('=')[0] in exclude: continue
    dl=0
    nurl=url
    if l=='-':
        dl-=1
        nurl=url=0
    elif l=='#FOLDER':
        dl+=1
        url=nurl=0
    elif l=='#URL':
        url=1
        nurl=0
    if dotree:
        l = (level+nurl)*4*' '+l
    print l
    level+=dl
    assert level>=0, prev+'\n'+l
    prev=l

# vim:ts=4:sw=4:expandtab

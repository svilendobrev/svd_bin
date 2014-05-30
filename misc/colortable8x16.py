#!/usr/bin/env python
#$Id: colortable8x16.py,v 1.3 2006-05-11 17:04:59 sdobrev Exp $
from __future__ import print_function
ESC = chr(27)
CLRSCR = ESC+'[J'
GOTOXY = ESC+'[%(y)d;%(x)dH'    #x,y 1-based
GOTO00 = ESC+'[H'

def CLR(fg,bg,hi=0):
    fg += 30
    bg += 40
    return ESC+'[%(hi)d;%(fg)d;%(bg)dm' % locals()

for bg in range(8):
    for fg in range(8):
        print( CLR(fg,bg),'Xabc',CLR(fg,bg,1),'Ydef', end='')
    print( CLR(fg,0))
print( CLR(8,0),'===')
# vim:ts=4:sw=4:expandtab

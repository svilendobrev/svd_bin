#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys,re
prg = sys.argv.pop(0)
try: dont = sys.argv.remove('-n') or True
except: dont = False
try: link = sys.argv.remove('-l') or True
except: link = False
try: dirfiles = sys.argv.remove('-r') or True
except: dirfiles = False

def renul( x, up):
    r = os.path.split(x)
    return os.path.join( r[0], up and r[1].upper() or r[1].lower())

if 'renu' in prg: func = lambda x: renul(x,True)
elif 'renl' in prg: func = lambda x: renul(x,False)
else:
    regexp = sys.argv.pop(0)
    subst  = sys.argv.pop(0)
    for a in range(1,6):
       subst = subst.replace( '$'+str(a), '\\'+str(a))
    def func( x):
        return re.sub( regexp, subst, x)
    print( '#', regexp, '=>', subst)

def doit(a):
    b = func(a)
    if b != a:
        print( a, '->', b)
        if not dont: (link and os.link or os.rename)( a,b)
    return b

import glob
for a in sys.argv:
    if a == '-':
        for f in sys.stdin:
            doit( f.strip() )
        continue
    b = doit(a)
    if dirfiles:
        for f in glob.glob( b+'/*'):
            doit( f)

# vim:ts=4:sw=4:expandtab

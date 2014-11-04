#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys,re
from svd_util import optz
optz.bool( 'fake', help= 'do nothing')
optz.bool( 'link', help= 'link instead of move/rename')
optz.bool( 'dirfiles', '-r', help= 'dir and then files inside') #?
optz.bool( 'upper', '-u', help= 'just upper-case, all args are filepaths')
optz.bool( 'lower', '-l', help= 'just lower-case, all args are filepaths')
optz.bool( 'insymlink', help= 'rename inside symlinks-text, ignore non-symlinks')
optz.help( '''
%prog [options] regexp subst filepaths
   subst can also use $1..$6 for groups
   if filepath is - , reads stdin, one filepath per line
   ! put -- before args if any filepath/regexp/subst starts with -
%prog -u/-l [options] filepaths
renu* [options] filepaths
renl* [options] filepaths
'''.strip() )
optz,argz = optz.get()

def renul( x, up):
    r = os.path.split(x)
    return os.path.join( r[0], r[1].upper() if up else r[1].lower())

prg = os.path.basename( sys.argv[0] )
if prg.startswith( 'renu'): optz.upper = True
if prg.startswith( 'renl'): optz.lower = True

if   optz.upper: func = lambda x: renul(x,True)
elif optz.lower: func = lambda x: renul(x,False)
else:
    regexp = argz.pop(0)
    subst  = argz.pop(0)
    for a in range(1,6):
       subst = subst.replace( '$'+str(a), '\\'+str(a))
    repl = re.compile( regexp)
    def func( x):
        return repl.sub( subst, x)
    print( '#', regexp, '=>', subst)

if optz.insymlink:
    print( '# inside symlinks')

def doit(a):
    org = a
    if optz.insymlink:
        if not os.path.islink( a):
            print( '!ignore non-symlink', a)
            return a
        a = os.readlink( a )
    b = func(a)
    if b != a:
        print( *[ x for x in [
                org!=a and org+'->',
                a, ':>', b
                ] if x])
        if not optz.fake:
            if optz.insymlink:
                os.remove( org)
                os.symlink( b, org)
            else:
                (optz.link and os.link or os.rename)( a,b)
    return b

import glob
for a in argz:
    if a == '-':
        for f in sys.stdin:
            doit( f.strip() )
        continue
    b = doit(a)
    if optz.dirfiles:
        for f in glob.glob( b+'/*'):
            doit( f)

# vim:ts=4:sw=4:expandtab

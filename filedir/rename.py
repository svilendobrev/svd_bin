#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys,re
from svd_util import optz
optz.bool( 'fake', '-n', help= 'do nothing')
optz.bool( 'link', help= 'link instead of move/rename')
optz.bool( 'dirfiles', '-r', help= 'dir and then files inside') #?
optz.bool( 'lower', '-l', help= 'just lower-case, all args are filepaths')
optz.bool( 'upper', '-u', help= 'just upper-case, all args are filepaths')
optz.int(  'levels',    default=0, help= 'levels above leaf to rename lower/upper, default [%default]')
optz.str(  'movepath',  help= 'rename and move into')
optz.str(  'command',   help= 'exec this with 2 args instead of os.rename/os.link')
optz.bool( 'insymlink', help= 'rename inside symlinks (text it points to), ignore non-symlinks')
optz.bool( 'outsymlink', help= 'if --insymlink, also rename/cmd actual symlinked-path')
optz.bool( 'thesymlink', help= 'if --insymlink, also rename/cmd the symlink itself')
#optz.bool( 'filter',    help= 'additional filter for inside symlinks; action applies if this matches inside symlink')  mmm use instead find -lname ?
optz.bool( 'noerror',   help= 'skip errors')
optz.bool( 'abssymlink', help= 'rename symlinks to point to abs-full-path, ignore non-symlinks')
optz.bool( 'quiet', )
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

def renul( x, up, levels =optz.levels):
    r = os.path.split(x)
    r0 = r[0]
    if levels>0: r0 = renul( r0, up, levels-1)
    return os.path.join( r0, r[1].upper() if up else r[1].lower())

prg = os.path.basename( sys.argv[0] )
if prg.startswith( 'renu'): optz.upper = True
if prg.startswith( 'renl'): optz.lower = True

if   optz.upper: func = lambda x: renul(x,True)
elif optz.lower: func = lambda x: renul(x,False)
elif optz.abssymlink: func = os.path.realpath
else:
    regexp = argz.pop(0)
    subst  = argz.pop(0)
    for a in range(1,6):
       subst = subst.replace( '$'+str(a), '\\'+str(a))
    repl = re.compile( regexp)
    def func( x):
        return repl.sub( subst, x)
    if not optz.quiet: print( '#', repr(regexp), '=>', repr(subst))

if optz.insymlink and not optz.quiet:
    print( '# inside symlinks')

_print = print
def print(*aa):
    _print( *(a.encode('utf8','ignore').decode('utf8') for a in aa))

def doit(a):
    if optz.movepath == a:
        print( '!ignore movepath target', a)
        return

    org = a
    orgb = org
    if optz.insymlink:
        if not os.path.islink( a):
            print( '!ignore non-symlink', a)
            return a
        a = os.readlink( a )
        if optz.thesymlink:
            orgb = func( org)
    b = func(a)
#    print( '?<', a)
#    print( '?>', b)
    if b == a: return b
    if optz.movepath:
        b = os.path.join( optz.movepath, b)


    if not optz.quiet or optz.fake:

        print( *( (org!=a) * [ org,'->', ] + [ a, ] ))
        print( ':>', *( (orgb!=a) * [ orgb,'->', ] + [ b ] ))
        if optz.insymlink and optz.outsymlink:
            print( a, )
            print( ':>', b )
    if optz.fake: return b

    if optz.insymlink:
        os.remove( org)
        os.symlink( b, orgb)
    if not optz.insymlink or optz.outsymlink:
        if optz.command:
            import subprocess
            print( optz.command, a, b)
            subprocess.call( optz.command.split() + [ a, b] )
        else:
            #print( a,':>',b)
            try:
                (optz.link and os.link or os.rename)( a,b)
            except Exception as e:
                if optz.noerror:
                    print( '??', e )
                else: raise
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

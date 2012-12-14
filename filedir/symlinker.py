#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os, fnmatch
from os.path import isdir, basename, exists, join, dirname, realpath
from svd_util import optz, osextra

optz.help( '''
walklink sourceitem[s] target  -  mv/cp/ln that sees through dir+file symlinks
    if targetnotexists
        TODO if one source, rename it
        else - make targetdir, move sources into it
    if target.exists
        if target.isdir, move sources into it
        TODO elif target.isfile and one source.isfile and --force, overwrite target
        else error: multiple or non-file sources into existing target.file
''')

optz.bool( 'force', '-f', help= 'force source file to overwrite target file if exists')
optz.list( 'exclude',    help= 'exclude filepattern (multiple)')
optz.list( 'include',    help= 'include filepattern (multiple)')
optz.list( 'direxclude', help= 'exclude dirpattern  (multiple)')
optz.list( 'dirinclude', help= 'include dirpattern  (multiple)')
optz.simvolni = True #',  '-L', help= 'обхожда и символни връзки')

ops = {
    os.rename : 'mv move',
    os.link   : 'ln link',
#   os.link   : 'cp copy',
    None:       'print'
}
op2op = {}
for op,names in ops.items():
    for n in names.split():
        op2op[n] = op

optz.text( 'op', type= 'choice', choices= ' '.join( sorted( ops.values())).split(),
    help= 'operation: ln/link mv/move cp/copy, default: print')

optz,argz = optz.get()

target = argz.pop( -1)

ops = []

def match1( f, p):
    return fnmatch.fnmatch( f,p)

def match( f, patterns):
    for p in patterns:
        if match1( f, p): return True

def included( a, inc, exc):
    if inc and not match( a, inc): return
    if exc and match( a, exc): return
    return a

def levels( d): return d.strip('/').split('/')

def walk( argz, target, followlinks =True):
    if not exists( target): yield None, target
    else: assert isdir( target)
    for src in argz:
        src = realpath( src)
        if not isdir( src):
            yield src, join( target, src)
        else:
            srcdepth = len( levels( src))
            for path,dirs,files in os.walk( src, followlinks= followlinks):
                if not included( path, optz.dirinclude, optz.direxclude):
                    dirs[:] = []
                    continue
                #dirs[:] = [ d for d in dirs if included( d, optz.dirinclude, optz.direxclude) ]

                pathdeeper = levels( path)[ srcdepth:]
                targdeeper = join( target, *pathdeeper )
                mkdir = False
                for f in files:
                    if not included( f, optz.include, optz.exclude ): continue
                    fsrc = realpath( join( path, f))
                    if not mkdir:
                        yield None, targdeeper
                        mkdir = True
                    yield fsrc, join( targdeeper, f )

op = op2op.get( optz.op)
for s,t in walk( argz, target):
    try:
        if not s:
            if op: osextra.makedirs( t)
            else: print( '>>', t+'/' )
        elif op:
            if exists( t) and optz.force: os.remove( t)
            op( s, t)
        else: print( '--', s, '\n->', t)
    except:
        print( '--', s, '\n->', t)
        raise

# vim:ts=4:sw=4:expandtab

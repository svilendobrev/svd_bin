#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

from shutil import copy2, copytree
import os,errno

copyargs = {}
try: #use dirs_exist_ok, py 3.8+
    copytree( '', None, dirs_exist_ok =True)
except TypeError:
    #XXX HACK shutil.copytree
    _makedirs = os.makedirs
    def makedirs( *a,**ka):
        if 1:
            ka['exist_ok'] = True
            return _makedirs( *a,**ka)
        else:
            #see svd_util.osextra.makedirs... py<=3.4
            try:
                _makedirs( *a,**ka)#, exist_ok =True)
            except OSError as e:
                if e.errno != errno.EEXIST: raise
    os.makedirs = makedirs
except FileNotFoundError:
    copyargs.update( dirs_exist_ok = True)

try: #use ignore_dangling_symlinks, py 3.2+
    copytree( '', None, ignore_dangling_symlinks=True)
except TypeError: pass
except FileNotFoundError:
    copyargs.update( ignore_dangling_symlinks = True)

#print( copyargs)

from svd_util import optz
optz.text( 'include', '-i', help= 'these-only, regexp.match, applied over whole path - use .*/[^/]*xyz[^/]* to match filename having xyz ; .*xyz.* to match anything having xyz in path' )
optz.text( 'exclude', '-x', help= 'these-skip, regexp.match, applied over whole path, before --include' )
optz.bool( 'symlinks_dereference', '-L', help= 'dereference symlinks into files')
optz.bool( 'verbose', '-v', help= 'print what is copied or not')
optz,argz = optz.get()

import re
exclude = None
if optz.exclude:
    print( 'excluding:', optz.exclude)
    exclude = re.compile( optz.exclude)
include = None
if optz.include:
    print( 'including:', optz.include)
    include = re.compile( optz.include)

src,dst = argz[:2]
if 1:
    def copy( src, dst, **ka):
        if exclude and exclude.match( src):
            if optz.verbose: print( 'excluded:', src)
            return
        if include and not include.match( src):
            if optz.verbose: print( 'not included:', src)
            return
        if optz.verbose: print( 'copy:', src, '>>', dst)
        return copy2( src, dst, **ka)
    copyargs.update( copy_function= copy)
else:
    def ignore( dir,listdir):
        skipped = filter( dir, listdir) if filter else ()
        return skipped
    copyargs.update( ignore= ignore)

copytree( src, dst, symlinks= not optz.symlinks_dereference, **copyargs)

# vim:ts=4:sw=4:expandtab

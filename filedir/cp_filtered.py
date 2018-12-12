#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

from shutil import copy2, copytree
import os,errno


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

from svd_util import optz
optz.text( 'include', '-i', help= 'these-only, regexp.match, applied over whole path' )
optz.text( 'exclude', '-x', help= 'these-skip, regexp.match, applied over whole path, has priority over --include' )
optz,argz = optz.get()

exclude = None
if optz.exclude:
    import re
    print( 'excluding:', optz.exclude)
    exclude = re.compile( optz.exclude)
include = None
if optz.include:
    import re
    print( 'including:', optz.include)
    include = re.compile( optz.include)

src,dst = argz[:2]
if 1:
    def copy( src, dst, **ka):
        if exclude and exclude.match( src): return
        if include and not include.match( src): return
        return copy2( src, dst, **ka)
    copyargs = dict( copy_function= copy)
else:
    def ignore( dir,listdir):
        skipped = filter( dir, listdir) if filter else ()
        return skipped
    copyargs = dict( ignore= ignore)

copytree( src, dst, symlinks=optz.symlinks, ignore_dangling_symlinks=True, **copyargs)

# vim:ts=4:sw=4:expandtab

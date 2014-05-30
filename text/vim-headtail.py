#!/usr/bin/env python
#$Id: cvs-vim-all.py,v 1.4 2007-12-07 20:46:52 sdobrev Exp $
from __future__ import print_function
from svd_util import gencxx, optz
optz.bool( 'head')
optz,argz = optz.get()

import os.path
#from textwrap import TextWrap
ext_c = '.changed .cpp .cxx .h .hpp .hxx .java'.split()
ext_make = '.mak'.split()

for a in argz:
    org = f = file(a).read()
    if not f.strip(): continue
    ext = os.path.splitext( a )[1].lower()
    is_c = ext in ext_c
    is_make = ext in ext_make or os.path.basename( a ).lower().startswith( 'makef' )

    if optz.head and gencxx._CVShead[:3] not in f:
        h = is_c and gencxx.CVShead or gencxx.CVShead_py
        f = h + f

    if gencxx._VIMtail.strip() not in f:
        h = is_c and gencxx.VIMtail or gencxx.VIMtail_py
        if is_make: h = h.replace( ':expandtab', ':noexpandtab' )
        f = f + h
    if not is_make:
        f = f.expandtabs(4)

    if f != org:
        try:
            w = file(a,'w')
        except IOError, e:
            print( 'cannot write', a, e)
        else:
            try:
                print( 'w', a)
                w.write( f)
            finally:
                w.close()

# vim:ts=4:sw=4:expandtab

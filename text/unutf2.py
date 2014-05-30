#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

def unutf2( x, decode =True):
    if decode: x = x.decode( 'utf8')
    return ''.join( [chr(ord(i)) for i in x] ).decode('utf8')

if __name__ == '__main__':

    import sys,os
    from svd_util import optz
    optz.bool( 'rename', help= 'input lines are file-names, rename them')
    optz, argz = optz.get()

    for l in sys.stdin:
        r = unutf2( l.rstrip())
        print( r)
        if optz.rename:
            os.rename( l, r)

# vim:ts=4:sw=4:expandtab

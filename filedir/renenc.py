#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from svd_util import optz
import os,sys

optz.bool( 'fake')
optz.text( 'input',  '-i', help= 'input encoding', default= 'utf8')
optz.text( 'output', '-o', help= 'output encoding')
optz,argz = optz.get()
#if opt('-icp1251', '-i=cp1251'): ienc = 'cp1251'
#if opt('-icp866', '-i=cp866'): ienc = 'cp866'
#if opt('-outf8', '-o=utf8'): oenc = 'utf8'

for x in argz:
    dir,x = os.path.split( x)
    fn = x.decode( optz.ienc)
    print( x, fn)
    if optz.fake: continue
    if optz.oenc: fn = fn.encode( optz.oenc)
    os.rename( *(os.path.join( dir,f) for f in (x, fn)))

# vim:ts=4:sw=4:expandtab

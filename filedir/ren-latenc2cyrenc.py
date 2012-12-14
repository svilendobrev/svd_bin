#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
def f(x): return ''.join( chr(ord( c)) for c in a.decode('utf8')).decode('cp1251')

for a in os.listdir('.'):
    print f(a)
    os.rename( a, f(a))

# vim:ts=4:sw=4:expandtab

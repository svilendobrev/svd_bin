#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys, os.path
all = {}
for a in sys.argv[1:]:
    if os.path.islink(a): continue
    all.setdefault( os.path.getsize( a), []).append(a)
for sz,items in sorted( all.items()):
    if len(items) ==1: continue
    print( '\n  '.join( [str(sz)] + sorted( items)))
# vim:ts=4:sw=4:expandtab

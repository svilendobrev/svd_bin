#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys
for a in sys.stdin:
    print( a.encode('latin-1').decode('cp1251') )
# vim:ts=4:sw=4:expandtab

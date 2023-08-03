#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys
print( *sorted(set(a.split('\t')[1] for a in sys.stdin if a[:1]!="!")),sep="\n")

#files which are tagged by ctags
#usage: text/tags_filenames-only.py < ./tags

# vim:ts=4:sw=4:expandtab

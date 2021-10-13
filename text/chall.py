#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

import sys, re
patrn,subst= sys.argv[1:3]
for a in sys.argv[3:]:
    t = open( a).read()
    t = re.sub( patrn,subst, t)
    with open( a, 'w') as o:
        o.write( t)

# vim:ts=4:sw=4:expandtab

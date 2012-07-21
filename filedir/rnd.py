#!/usr/bin/env python
#$Id: rnd.py,v 1.4 2008-01-07 09:05:34 sdobrev Exp $

import os.path,sys
import random
random.seed()

if len( sys.argv[1:])>1:
    r = sys.argv[1:]
else:
    r = os.listdir( sys.argv[1:] and sys.argv[1] or '.')
random.shuffle( r)
for a in r:
    if not os.path.basename( a).startswith('.'): print a

# vim:ts=4:sw=4:expandtab

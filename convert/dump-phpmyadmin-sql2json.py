#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

import json, pprint, sys
for x in sys.stdin: #open( sys.argv[1]): #'svilendobrev.json'
    x = x.strip()
    if not x: continue
    if x.startswith('//'):
        print(x)
        continue
    if not x.startswith('['):  continue
    rows = json.loads( x)
    print( len(rows))
    for r in rows: pprint.pprint( r)
    print('=='*6)
    print('\n'*3)


# vim:ts=4:sw=4:expandtab

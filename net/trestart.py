#!/usr/bin/env python
import os,subprocess,sys
r = []
for x in sys.stdin:
    r += x.split(None,1)[:1]
r = [ x.rstrip('*') for x in r if '*' in x ]
print ','.join(r)

#!/usr/bin/env python3
import sys,os
func = 'lower'
try: sys.argv.remove('-lo')
except: func = 'upper'
for a in sys.argv[1:]:
    b = getattr( a[0], func )() + a[1:]
    print( a, '->', b)
    os.rename( a,b)

# vim:ts=4:sw=4:expandtab

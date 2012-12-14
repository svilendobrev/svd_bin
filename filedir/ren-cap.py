#!/usr/bin/env python3
import sys,os
for a in sys.argv[1:]:
    b = a[0].upper()+a[1:]
    os.rename( a,b)

# vim:ts=4:sw=4:expandtab

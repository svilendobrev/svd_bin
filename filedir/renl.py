#!/usr/bin/env python3
import os,sys
func = 'renu' in sys.argv[0] and 'upper' or 'lower'
for a in sys.argv[1:]:
    b = getattr( a, func)()
    if b != a:
        print( a, '->', b)
        os.rename( a,b)

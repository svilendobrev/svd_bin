#!/usr/bin/env python
import sys, urllib
try: cp1251= not sys.argv.remove('cp1251')
except:cp1251=0
try: quoted= not sys.argv.remove('quoted')
except:quoted=0

def tx(a):
    a = urllib.unquote_plus( a.rstrip())
    if 'q=%' in a: a = urllib.unquote_plus( a.rstrip())#tx(a)
    if cp1251: return a.decode('cp1251', 'ignore')
    return a #.decode('utf-8', 'ignore') #.encode('cp1251', 'ignore')

for a in sys.stdin:
    a = a.rstrip()
    if quoted:
        qq = a.split('"')
        pp = []
        for i,x in enumerate(qq):
            if i % 2: x = tx(x)
            pp.append(x)
        a = '"'.join( pp)
    else:
        a = tx(a)
    #if 'q=%' in a: a = tx(a)
    print a

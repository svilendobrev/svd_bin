#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys
def r( d, lam): return d/lam

koef = '''
λD: W/mK
0.14    дърво - бор, ела
0.14    газобетон
0.39    тухли с много отвори
0.5     тухла
0.76    плътни тухли
2.3     стоманобетон
0.8     варова мазилка ; шпакловка
0.7     силикатна мазилка
0.02    Пенополиуретан ..0.023
0.032   EPS + графит? неопор
0.035   XPS
0.037   каменна вата .033-.039
0.04    EPS стиропор
'''


sloeve = sys.argv[1:]
if not sloeve:
    print( sys.argv[0], 'd1=k1 d2=k2 ...')
    print( koef)
    primer = '''
0.04=0.8    #вътрешна мазилка
0.25=0.5    #тухла
0.05=1.5    #външна мазилка
0.10=0.038  #изолация
0.01=2      #замазка
'''.strip()
    print( primer)
    sloeve = [ a.split('#',1)[0].strip() for a in primer.split('\n')]

sloeve = [ tuple(float(x)
            for x in a.split('=')) for a in sloeve ]
print( sloeve)
rsum = sum( r( d,lam) for d,lam in sloeve )
rsi = 0.04 #m2K/W съпротивление на топлопредаване на вътрешната повърхност
rse = 0.13 #m2K/W съпротивление на топлопредаване на външната повърхност
rsum += rsi + rse
print( 1/rsum, 'W/m2K')

# vim:ts=4:sw=4:expandtab

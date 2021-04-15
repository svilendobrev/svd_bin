#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
args = [eval(x) for x in sys.argv[1:]]
suma, godini, god_procent= args[:3]
#godini2, god_procent2 = args[3:] and args[3:5] or (0,0)

def calc( suma, godini, god_procent, G2M =12):
#http://krediten-kalkulator.bghot.com/
    meseci = godini*G2M
    mes_lihva = god_procent /100.0/G2M
    x= (1 + mes_lihva) ** meseci
    mes_suma = (suma * x * mes_lihva)/(x-1)
    vse_suma = mes_suma * meseci
    return mes_suma, vse_suma

if god_procent<0:
    merka,G2M,god_procent = 'den',365,-god_procent
else:
    merka,G2M,god_procent = 'mesec',12,god_procent
mes_suma, vse_suma = calc( suma, godini, god_procent, G2M)
print( #int(mes_suma), '/'+merka,
        int(vse_suma/godini/12), '/m',
        '==', int(vse_suma), int(vse_suma*100/suma),'%', )

# vim:ts=4:sw=4:expandtab

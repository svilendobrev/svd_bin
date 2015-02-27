#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
suma   = float(sys.argv[1])
godini = float(sys.argv[2])
god_procent= float(sys.argv[3])


#http://krediten-kalkulator.bghot.com/
meseci = godini*12
mes_lihva = god_procent /100.0/12
x= (1 + mes_lihva) ** meseci
mes_suma = (suma * x * mes_lihva)/(x-1)
vse_suma = mes_suma * meseci
print( mes_suma, '/m', vse_suma, int(vse_suma*100/suma),'%')

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
suma, godini, god_procent= [float(x) for x in sys.argv[1:4]]

#http://krediten-kalkulator.bghot.com/
meseci = godini*12
mes_lihva = god_procent /100.0/12
x= (1 + mes_lihva) ** meseci
mes_suma = (suma * x * mes_lihva)/(x-1)
vse_suma = mes_suma * meseci
print( int(mes_suma), '/m', int(vse_suma), int(vse_suma*100/suma),'%')

# vim:ts=4:sw=4:expandtab

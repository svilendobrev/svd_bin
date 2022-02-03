#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys
x = eval( sys.argv[1])

dod = 0.10
osig_rabotnik_perc = (8.38+2.2+3.2)/100.0
MAX_OSIG_BRUTO = 3000
def osig_rabotnik( bruto): # = 413.4 if >=3000
    return min( MAX_OSIG_BRUTO, bruto ) * osig_rabotnik_perc
def osig_rabotodatel( bruto):   #=567.6 if >= 3000
    return min( MAX_OSIG_BRUTO, bruto ) * (10.92+0.4+2.8+4.8) / 100.0

def neto( bruto):
    return ( bruto - osig_rabotnik( bruto) ) * (1-dod)
    #n = (b-o(b)) * (1-dod)

MAX_OSIG_NETO = neto( MAX_OSIG_BRUTO)

def bruto( neto):
    #b>=3000: n=(b-413.4)*(1-dod) -> b= n/(1-dod)+413.4
    #b<3000:  n=(b-b*o_perc)*(1-dod) -> b= n/(1-dod)/(1-o_perc)
    b = neto / (1-dod)
    if neto >= MAX_OSIG_NETO: return b + osig_rabotnik( MAX_OSIG_BRUTO)
    return b / (1-osig_rabotnik_perc)

def razhod( bruto):
    return bruto + osig_rabotodatel( bruto)

bx = bruto(x)
rbx = razhod(bx)
nx = neto(x)
rnx = razhod(x)
print( f'neto : {x} -> bruto= {bx:.2f}, razhod: {rbx:.2f}')
print( f'bruto: {x} -> neto = {nx:.2f}, razhod: {rnx:.2f}')

''' 2021
брутно възнаграждение = БрВ >=3000
Осиг работник в/у 3000 = 3000*(8,38+2,2+3,2)/100 = 413,4
ДОД = (БрВ-413,4)*10%
Запл. за получаване = БрВ - 413,4 - ДОД = 0,9*(БрВ - 413,4)

За работодателя = БрВ+567,6
Осиг работодател = 3000*(10.92+0.4+2.8+4.8)/100 = 567.6
'''

# vim:ts=4:sw=4:expandtab

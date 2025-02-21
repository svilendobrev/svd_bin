#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys

# https://nra.bg/wps/portal/nra/osiguryavane/darzhavno-obshtestveno-osiguryavane-doo/osiguritelen-dohod
# https://nra.bg/wps/portal/nra/osiguryavane/osiguryavam-se-sam
# https://nra.bg/wps/wcm/connect/nra.bg25863/bf946fec-c77d-469a-bf77-9b4a035c90c4/Приложение_1_20-28-1_08.01.2024.pdf
# родени след 1.1.1960 вкл.

samoosig = False
godina = 2025
_max_osig_bruto = {
    2023: 3400,
    2024: 3750,
    2025: 4130,
    }
MAX_OSIG_BRUTO = _max_osig_bruto[ godina ]
razhodi_priznati_samoosig_koef = 0.25

for x0 in sys.argv[1:]:
    if x0 in ('samo', 'само', 'self'):
        samoosig = True
        continue
    x = eval( x0)
    print( x, '='+x0 if str(x) != x0 else '' )
    if -x in _max_osig_bruto:
        godina = -x
        MAX_OSIG_BRUTO = _max_osig_bruto[ godina ]
        continue

    dod = 0.10
    if samoosig:
        osig_rabotnik_procent      = 14.8+3.5 +5 +8    # 2024
        osig_rabotodatel_procent   = 0
    else:
        osig_rabotnik_procent      =  8.38 +2.2 +3.2   # 8.38= 6.58+1.4+0.4
        osig_rabotodatel_procent   = 10.92 +2.8 +4.8   #+0.4???  #10.92= 8.22+2.1+0.6
    def osig_rabotnik( bruto):
        return min( MAX_OSIG_BRUTO, bruto ) * osig_rabotnik_procent / 100.0
    def osig_rabotodatel( bruto):
        return min( MAX_OSIG_BRUTO, bruto ) * osig_rabotodatel_procent / 100.0


    def neto( bruto):
        razhodi_koef = samoosig * razhodi_priznati_samoosig_koef
        b = bruto - osig_rabotnik( bruto)
        return b * (1- dod*(1-razhodi_koef))
        #n = (b-o(b)) * (1-dod)

    MAX_OSIG_NETO = neto( MAX_OSIG_BRUTO)

    def bruto( neto):
        #b>=3000: n=(b-413.4)*(1-dod) -> b= n/(1-dod)+413.4
        #b<3000:  n=(b-b*osig_koef)*(1-dod) -> b= n/(1-dod)/(1-osig_koef)
        razhodi_koef = samoosig * razhodi_priznati_samoosig_koef
        b = neto / (1- dod*(1-razhodi_koef))
        if neto >= MAX_OSIG_NETO: return b + osig_rabotnik( MAX_OSIG_BRUTO)
        return b / (1-osig_rabotnik_procent)

    def razhod( bruto):
        return bruto + osig_rabotodatel( bruto)

    bx = bruto(x)
    rbx = razhod(bx)
    nx = neto(x)
    rnx = razhod(x)
    print( f' neto : {x} -> bruto= {bx:.2f}, razhod: {rbx:.2f}')
    print( f' bruto: {x} -> neto = {nx:.2f}, razhod: {rnx:.2f}')

''' 2021
брутно възнаграждение = БрВ >=3000
Осиг работник в/у 3000 = 3000*(8,38+2,2+3,2)/100 = 413,4
ДОД = (БрВ-413,4)*10%
Запл. за получаване = БрВ - 413,4 - ДОД = 0,9*(БрВ - 413,4)

За работодателя = БрВ+567,6
Осиг работодател = 3000*(10.92+0.4+2.8+4.8)/100 = 567.6
'''

# vim:ts=4:sw=4:expandtab

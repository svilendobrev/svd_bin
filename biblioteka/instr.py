# -*- coding: utf-8 -*-
from util import eutf

def meta_prevodi( fname, dict= dict, nomer_stoinost =0, prn =None, zaglavie ='meta_prevodi' ):
    if prn: prn( zaglavie +':', fname)
    meta_prevodi = dict()
    for l in eutf.readlines( fname):
        l = l.strip()
        if not l or l[0]=='#': continue
        kvv = l.split()
        k = kvv[ nomer_stoinost]
        for v in kvv:
            meta_prevodi[ v ] = k       #XXX ignorecase .lower
        if prn: prn( k, '=', *kvv )
    return meta_prevodi

def zaglavie( x):
    x = x and str(x).strip()
    return x and x[0].upper() + x[1:]
def nezaglavie( x):
    x = x and str(x).strip()
    return x and (x[0].lower() + x[1:])

# vim:ts=4:sw=4:expandtab

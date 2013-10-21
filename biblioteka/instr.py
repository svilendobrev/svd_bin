# -*- coding: utf-8 -*-
from svd_util import eutf

def meta_prevodi( fname, dict= dict, nomer_stoinost =0, prn =None, zaglavie ='meta_prevodi', razdelitel_v_nachaloto =False):
    if prn: prn( zaglavie +':', fname)
    meta_prevodi = dict()
    for l in eutf.readlines( fname):
        if not l or l[0]=='#': continue
        if razdelitel_v_nachaloto:
            razdelitel = l[0]
            l = l[1:]
            if not razdelitel.strip(): razdelitel = None
        else: razdelitel = None
        l = l.strip()
        kvv = l.split( razdelitel)
        k = kvv[ nomer_stoinost].strip()
        for v in kvv:
            meta_prevodi[ v.strip() ] = k       #XXX ignorecase .lower
        if prn: prn( razdelitel, k, '=', *kvv )
    return meta_prevodi

def zaglavie( x):
    x = x and str(x).strip()
    return x and x[0].upper() + x[1:]
def nezaglavie( x):
    x = x and str(x).strip()
    return x and (x[0].lower() + x[1:])

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, re
import pprint
from svd_util import optz
optz.bool( 'ednakvo_ime_razlika_razmer')
optz.bool( 'samoime')
optz.append( 'sravni')
optz.append( 'prevod')
optz,args = optz.get()

def walk( a):
    ff = []
    for path,dirs,files in os.walk( a, followlinks= False):
        for f in files:
            if not f.endswith('jpg'): continue
            ff.append( ( f, path, os.stat( os.path.join( path,f)).st_size ))
    ff.sort()
    return ff

ff = walk( args and args[0] or '.')

if optz.ednakvo_ime_razlika_razmer:
    u=''
    for f,p,s in ff:
        prn = 0
        if not u: u=f,p,s
        else:
            uf,up,us=u
            if uf==f and us==s: continue
            if uf==f:
                print( '?', *u)
                prn=1
        u=f,p,s
        if prn: print( ' ', *u)

elif optz.sravni:

    def l2d( ff):
        ff_po_ime = {}
        for f,p,s in ff:
            if f not in ff_po_ime:
                ff_po_ime[f] = { s: [p] }
            else:
                sp = ff_po_ime[f]
                if s not in sp:
                    print( 'sz', f, sp, s, p)
                    sp[s] = [p]
                else:
                    sp[s].append(p)
        return ff_po_ime

    ff_poime = l2d(ff)

    prevodi= []
    if optz.prevod:
        for p in optz.prevod:
            l,r = p.split('=')
            prevodi.append( (re.compile( l), r))
    #print( optz.prevod, prevodi)
    #optz.sravni = ()
    for d in optz.sravni:
        dd = walk( d)
        dd_poime = l2d( dd)
        lipsi = {}
        for f0,sp in dd_poime.items():
            f = f0
            for l,r in prevodi:
                f = l.sub( r, f)

            g = ff_poime.get( f)
            if not g: lipsi[f0] = (f,sp)
            else:
                for s,p in g.items():
                    if s in sp: break
                else:
                    print( f0,'?')
                    pprint.pprint( g)
                    pprint.pprint( sp, indent=2)
        for k,(f,sp) in sorted( lipsi.items()):
            xsp = pprint.pformat( sp, indent=2)
            if len(sp) >1:
                xsp = '\n'+xsp
            print( '-', k, f, xsp)



else:
    for f,p,s in ff:
        if optz.samoime: print( f)
        else: print( ' ', f, p, s)

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import opisvane #import save_if_diff
from prikazki import href #save_if_diff

from itertools import groupby

def ix( uuchastnici, po_dejnost =False ):
    fkey = po_dejnost and (lambda a: (a[1], a[0], a[2], a[3:])) or (lambda a: (a[0], a[1], a[2], a[3:]))
    uu = sorted( (fkey(u) for u in uuchastnici), key= lambda t: (t[:2], t[2][1], t[3] and t[3][0][1]) )

    gg = groupby( uu, key= lambda u: u[0] )
    tt = [ (k, groupby( list(g), key= lambda u: u[1])) for k,g in gg ]

    txt = [ '<ul>' ]
    for k,g in tt:
        txt += [ '<li> '+str(k) + ' <ul>' ]
        for k2,u in g:
            txt += [ ' <li>'+str(k2) + ' <ul>' ]
            for t in u:
                x,y = t[2:4]
                papkafname,ime = x #.ime_sglobeno2
                if y: # is not None and y is not x:
                    fname,iime = y[0] #sglobi( y.ime, avtor= (y.avtor != x.etiketi.avtor) and y.avtor)
                    ime = iime + ' : ' + ime
                txt += [ '  <li>' + href( papkafname, ime ) ]
            #txt += [ '  <li>' + str( t[2])
            txt += [ '  </ul>' ]
        txt += [ ' </ul>' ]
    txt += [ '</ul>' ]
    txt = '\n'.join( txt)

    save_if_diff( 'options.html_hora' + (po_dejnost and 'd2h' or 'h2d'), txt, )#enc= options.html_enc )

def save_if_diff( *a,**k):
    return opisvane.save_if_diff(
        naistina= optz.davai,
        podrobno= not optz.davai,
        #prezapis= info.options.prezapis,
        *a,**k)

from svd_util import optz
optz.bool( 'davai')
optz.bool( 'prikazki_otdelno')  #TODO
optz,argz = optz.get()
u = []
for a in argz:
    u += eval( open(a).read() )
for po_dejnost in False, True:
    ix( u, po_dejnost)

# vim:ts=4:sw=4:expandtab

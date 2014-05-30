#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ezodf
from ezodf.text import Paragraph, Heading, Span, ListItem, List, CN

from svd_util import optz
optz.text( 'template')
optz,args = optz.get()

inp = args[0]

d = ezodf.opendoc( inp)

odt = ezodf.newdoc( doctype='odt',
        filename= inp.replace('.odt','.flat.odt'),
        template= optz.template or inp)
body = odt.body
#pic = body.find( CN("draw:frame"))

body.clear()
#if pic: body.append( pic)

if 0:
    img = CN('draw:image')
    fra = CN('draw:frame')
    tbx = CN("draw:text-box")

    once = 0
    def delimg( a):
        global once
        for i in a:
            if i.xmlnode.tag == img:
                if once:
                    print( 66666, i.xmlnode)
                    a.remove( i)
                once +=1
            else:
                delimg( i)

def walk( a, lvl =0):
    #print(11111111111111,  a, a.xmlnode, a.plaintext())
    if lvl<2 and a.__class__ is ezodf.base.GenericWrapper:
        for i in a:
            walk( i, lvl= lvl+1)
    else:
        body.append( a)

for a in d.body:
    #delimg(a)
    walk(a)
odt.save()

# vim:ts=4:sw=4:expandtab

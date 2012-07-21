#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ezodf
from ezodf.text import Paragraph, Heading, Span, ListItem, List, CN


def o(x): return '<'+x+'>'
def c(x): return '</'+x+'>'
def oc(a,x): return o(a)+x+c(a)
def ital(x): return oc('i',x)
def bold(x): return oc('b',x)

def style(x): return getattr( x, 'style_name', None)

def span( i):
    s = style(i)
    t = i.plaintext() or ''
    if s and t:
        if 'Emphasis' in s: t = ital(t)
        if 'Strong' in s: t = bold(t)
    return t + (i.tail or '')

from util import optz
optz,args = optz.get()
d = ezodf.opendoc( args[0] )

if 0:
 LIST = 'dl'
 LISTITEM = 'dd'
else:
 LIST = 'ul'
 LISTITEM = 'li'

def walk( a,  lvl =''):
    if a.__class__ is Span:
        print( lvl, span(a))
        #print( lvl, a.tail)
        return
    tag = ''
    if isinstance( a, Paragraph):
        tag = 'p'
        s = style(a) #.xmlnode, a.text, a.tail)
        if s == 'Signature':
            tag = ''
            print( lvl, o('hr width=60% size=3 noshade'))
        elif s =='Caption':
            return
        #else: print(11111111111111,  a,s, a.plaintext())

    elif isinstance( a, Heading): tag = 'h'+str( a.outline_level)
    elif isinstance( a, List): tag = LIST
    elif isinstance( a, ListItem):
        print( lvl, o( LISTITEM))
    elif 0: print( 3333333333, lvl, a )#, a.plaintext())

    if tag: print( lvl, o( tag))

    if a.text:
        print( lvl, a.text)
    for i in a:
        walk( i, lvl= lvl+'  ')
    if a.tail:
        print( lvl, a.tail)

    if tag: print( lvl, c( tag))

#print( d.body)
for a in d.body:
    walk(a)

# vim:ts=4:sw=4:expandtab

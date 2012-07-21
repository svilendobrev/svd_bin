#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ezodf
from ezodf.text import Paragraph, Heading, Span, ListItem, List, CN
from sla import sla, DictAttr, State
import lxml.etree
import sys

from util import optz
optz.text( 'template')
optz,args = optz.get()

odt = ezodf.newdoc( doctype='odt', filename= args[0], template= optz.template )
body = odt.body
pic = body.find( CN("draw:frame"))
body.clear()
if pic: body.append( pic)

def Heading2(): return Heading( outline_level=2)
def Heading3(): return Heading( outline_level=3)

styles = {
   'h1': Heading,
   'h3': Heading2,
   'p' : Paragraph,
   'dd list-entry': ListItem,
   'dt list-hdr':   Heading3,
   'dt list-hdr0':  Heading3,
   'dl':  List,
   'ul':  List,
   'mail':  None,
}

wraps = dict(
#    underline= 'Internet_20_Link',
    bold     = 'Strong_20_Emphasis',
    italic   = 'Emphasis',
)


class State( State):
    dl = 'dd'.split()

stack = [ body]
last = None
def add( x):
    global last
    if not x: return
    last = x()
    stack[-1].append( last)
    if x is ListItem:
        last.append( Paragraph() )
        last = last[-1]
def push( x):
    if not x: return
    x = x()
    stack[-1].append( x)
    stack.append( x)
def pop():
    stack.pop()
    assert stack

for tt,s,i,sprev,sdif in sla( sys.stdin, State=State ):

    #if 'style' in sdif:
    #    pr( s.ostyle())

    #if 'style' in sdif:
    #    if sprev:
    #        pr( sprev.cstyle())

    x = styles.get( s.style, None)
    if 'style' in sdif:
        if sprev and s.parent != sprev.parent:
            if sprev.parent:
                pop()
        if not sprev or s.parent != sprev.parent:
            push( styles.get( s.parent))
        add( x)
    elif sprev.closed:
        add( x)

#    print( 7777, s, x, tt, stack)
#   print( stack)

    if s.style in ('mail', None): continue

    def atext( t):
        if x is ListItem and t[0] in '-*+': t = t[1:].strip()
        t = t.replace( '&quot;', '"')
        t = t.replace( '&amp;', '&')
        t = Span(t)
        for k,v in wraps.items():
            if getattr( s, k, False):
                assert not t.style_name
                t.style_name = v
        last.append( t)

    for t in tt[:-1]:
        atext( t)
        add( x)
    atext( tt[-1])

#print( lxml.etree.tostring( body.xmlnode, pretty_print=1).decode('utf-8'))

odt.save()

# vim:ts=4:sw=4:expandtab

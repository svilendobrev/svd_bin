#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function

import re
import sys

class DictAttr( dict):
    def __init__( me, *a, **k):
        dict.__init__( me, *a, **k)
        me.__dict__ = me

styles = {
    "HTML_h1" : 'h1',
    "HTML_h3" : 'h3',
    "HTML_p"  : 'p',
    "HTML_default" : 'dd list-entry',
    "HTML_list"   : 'dt list-hdr',
    "HTML_list_0" : 'dt list-hdr0',
}

newp = '&#x5;'
newl = '&#x1c;'

class State( DictAttr):
    dl = 'dt dd'.split()
    ul = 'li'.split()
    @property
    def parent( me):
        if not me.style: return None
        y = me.style.split()[0]
        if y in me.dl: return 'dl'
        if y in me.ul: return 'ul'
        return None


def slaZ( inp, State =State, newline ='\n'):
    import xml.etree as et
    e = et.parse( inp)
    q = e.getroot()


re_text = re.compile( ' CH="(?P<text>.*?)"')
def sla( inp, State =State, newline ='\n'):
    res = []
    sprev = None
    sstyle = []
    for a in inp:
        a = a.strip()
        if a.startswith( '<para ') or a.startswith( '<trail '):   #new
            astyle = a.split('PARENT=')
            if len(astyle)>1:
                astyle = a.split('PARENT=')[-1].split('"')[1]
                #print >>sys.stderr, style
                st = styles.get( astyle)
                sprev.style.append( st)     # [None] -> default para-style
                sprev.closed = True
            sstyle = []     # no para-style
            continue
        if not a.startswith( '<ITEXT '): continue
        item = DictAttr()
        attr = value = None
        for i in a.split( '="'):
            lr = i.split('"')
            if len(lr)<2:
                attr = i.split()[-1]
                continue
            l,r = lr
            item[attr] = l
            attr = r.split()[-1]

        i = item #DictAttr( item)
        txt = i.pop('CH')

        font = i.get('FONT','').lower()
        s = State(
            underline = 'underline' in i.get('FEATURES',''),
            italic    = 'italic' in font or 'oblique' in font,
            bold      = 'bold' in font,
            style     = sstyle,
            closed    = False
        )
        txt = txt.replace( newl, newline )
        tt = txt.split( newp)
        res.append( ( tt, s, i))
        sprev = s

    sprev = None
    for tt,s,i in res:
        if s.style: s.style = s.style[0] or 'default'
        else: s.style = None
        sdif = diff( sprev, s)
        yield ( tt, s, i, sprev, sdif )
        sprev = s

def diff( prev,i):
    dif = set( i.items() )
    if prev is not None:
        dif -= set( prev.items() )
    return DictAttr( dif)

if __name__ == '__main__':
    for x in sla( sys.stdin):
        print( x)

# vim:ts=4:sw=4:expandtab

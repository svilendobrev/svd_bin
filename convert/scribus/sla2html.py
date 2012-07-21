#!/usr/bin/env python
#scribus .sla to .html
#from __future__ import print_function
from sla import sla, DictAttr, State

if __name__ == '__main__':
    def o(p): return p and '<'+p+'>'
    def c(p): return p and '</'+p+'>'

    class State( State):
        wraps = list( dict(
            underline= 'u',
            bold     = 'b',
            italic   = 'i',
            ).items())
        def open( me):
            x = [ ' '+o(v)
                for k,v in me.wraps
                if getattr( me, k, False) ]
            return ''.join( x)
        def close( me):
            x = [ ' '+c(v)
                for k,v in reversed( me.wraps )
                if getattr( me, k, False) ]
            return ''.join( x)

        def ostyle( me):
            return o( me.style) #'\n',
        def cstyle( me, force =False):
            if not force:
                if me.style and me.style.split()[0] in 'p dd dt li'.split():
                    return
            return c( me.style)

        def postyle( me, prev):
            r = []
            if prev:
                if me.parent == prev.parent: return
                r.append( prev.pcstyle())
            r.append( o( me.parent))
            return [a for a in r if a]
        def pcstyle( me):
            return c( me.parent)

    def pr( p):
        if p:
            if isinstance( p, (tuple,list)):
                for a in p:
                    if a: print a.rstrip()
            else: print p.rstrip()

    import sys
    for tt,s,i,sprev,sdif in sla( sys.stdin, State= State, newline= '\n<br>\n' ):

        print
        if 'style' in sdif:
            if sprev:
                pr( sprev.cstyle())
        if 'style' in sdif:
            print
            pr( s.postyle( sprev))
            pr( s.ostyle())
        elif sprev.closed:
            pr( s.ostyle())

        pr( s.open())

        for t in tt[:-1]:
            print t
            pr( s.cstyle())
            print
            pr( s.ostyle())

        print tt[-1]

        pr( s.close())

        #if 'style' in sdif: print s.cstyle(),

    pr( s.cstyle())

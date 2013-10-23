#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,re,sys
def err(*a):
    return
    print( *a, file= sys.stderr)

e = os.environ
comps = 'CWORD KEY WORDS WORDBREAKS TYPE POINT LINE'.split()
c = dict( (k,e.get('COMP_'+k,'')) for k in comps)
err( '\n'.join( a+'='+repr(c[a]) for a in comps))

#XXX WORDBREAKS are ' \t\n"\'><=;|&(:'
#but not mutualy equivalent...
#e.g  a b and a:b are quite different.. seems ><=;...: are treated as whitespace+that
#so WORDS & CWORD cannot be trusted - the rules aren't clear nor convenient
#hense: use .line upto .point then manual
line = c['LINE']
point= int( c['POINT'])
breaks= re.compile( '['+c['WORDBREAKS']+']+' )
words = breaks.split( line)
#    .replace( '(', r'\(')
err( words)
l = line[:point]
rest = line[point:]
lwords = breaks.split( l)
err( lwords[:-1], lwords[-1] )
print( '\n'.join('wa sb tc'.split()))

# vim:ts=4:sw=4:expandtab

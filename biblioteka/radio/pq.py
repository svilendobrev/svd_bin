#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import pyquery
import urllib
d = pyquery.PyQuery( filename= '/home/tmp/i.d.hb.20140314.15.41..html')
#d = pyquery.PyQuery( url= '.../i.d.hb.20140314.15.41..html')

q = d( '.'.join( 'div  row-fluid module_container'.split() ))
p = q( '.'.join( 'div  title'.split() ))
for t in p('a'):
    print( t.text, t.attrib['href'] )

#TODO........ refactor scheduler into this

# vim:ts=4:sw=4:expandtab

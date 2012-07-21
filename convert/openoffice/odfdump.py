#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, ezodf
import lxml.etree
name = sys.argv[1]
odt = ezodf.opendoc( name)
print( lxml.etree.tostring( odt.body.xmlnode, pretty_print=1).decode('utf-8'))

# vim:ts=4:sw=4:expandtab

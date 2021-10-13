#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
if 0:
    import lxml.etree, sys
    #parser = lxml.etree.XMLParser(remove_blank_text=True)
    #a = lxml.etree.parse( sys.stdin, parser)
    a = lxml.etree.parse( sys.stdin)
    print( lxml.etree.tostring( a, pretty_print=1, encoding= 'unicode'))

else:
    import xml.etree.ElementTree as ET, sys
    a = ET.parse( sys.stdin)
    ET.indent( a)
    print( ET.tostring( a.getroot(), encoding= 'unicode'))
    #a.write( sys.stdout, encoding= 'unicode')

# vim:ts=4:sw=4:expandtab

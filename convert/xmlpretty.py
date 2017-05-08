#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import lxml.etree, sys
#parser = lxml.etree.XMLParser(remove_blank_text=True)
#a = lxml.etree.parse( sys.stdin, parser)
a = lxml.etree.parse( sys.stdin)
print( lxml.etree.tostring( a, pretty_print=1))
# vim:ts=4:sw=4:expandtab

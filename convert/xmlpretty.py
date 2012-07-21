#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lxml.etree, sys
a = lxml.etree.parse( sys.stdin)
print lxml.etree.tostring( a, pretty_print=1)
# vim:ts=4:sw=4:expandtab

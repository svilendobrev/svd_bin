#!/usr/bin/env python
#$Id: uni2win.py,v 1.2 2006-07-10 14:41:22 sdobrev Exp $
from __future__ import print_function
encoding = 'cp1251'
import sys
i=6
while i:
	a = sys.stdin.readline()
	if not a: break
	#a = a.replace('%0D%0A','\n')
	z = a.replace('%u0','\\u0')
	if z != a:
		a=z
		a = a.replace('%u','uu')
		a = a.replace('%20',' ')
		a = a.replace('%','\\x')
		print( a)
		b = eval('u'+a)
		z = b.encode( encoding)#, 'replace' )
	print( z)
#	i-=1
# vim:ts=4:sw=4:expandtab

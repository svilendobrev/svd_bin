#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys, subprocess
cmd = (sys.argv[1:] or [ 'ls -ogF' ] )[0]

from pathlib import Path
from sumtim2 import filesize, minsec

p = Path( './radio')
for b in p.glob( '*/*.wav'):
	a = b.with_suffix( '.flac')
	if not a.exists(): continue
	atime,afsz = filesize( str(a))
	btime,bfsz = filesize( str(b))
	if abs(atime-btime)<0.4:
		print( '=', minsec( atime), a)
		subprocess.call( cmd.split() + [ str(b) ] )
	else:
		print( '? ', atime, minsec( atime), afsz, a)
		print( ' ?', btime, minsec( btime), bfsz, b)

# vim:ts=4:sw=4:expandtab

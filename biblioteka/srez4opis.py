#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

from izvadki2opis import dai_opis, dai_srezove
from os.path import dirname, join, splitext, exists
import sys

args = sys.argv[1:]
try: args.remove('flac')
except: flac=False
else: flac=True

fzvuk = args[0]
fpath = dirname( fzvuk)
fopis = (args[1:] or [join( fpath, 'opis')])[0]
opis = dai_opis( fopis )
assert opis, fopis
s = dai_srezove( opis)
#print(11111,s)
ss = s.split()
while '-' in ss: ss.remove('-')
if len(ss)==1:
    assert '-' in s,s
    ss = s.split('-')

#100-4+7.1 +200+4   -> start=103.1 size=204
#1:2.5 +100+2       -> start=62.5  size=102
#55  -100+1         -> start=55    end=-99

from svd_util.minsec import minsec2sec
start,end = ss[0],ss[-1]
start = minsec2sec( start) if ':' in start else eval( start)

#start,end = eval(ss[0]),ss[-1]
e0 = end[0] if end[0] in '=-+' else '='
end = end.strip('=-+')
end = minsec2sec( end) if ':' in end else eval(end)
end = e0+str(end)

ozvuk = fzvuk + '.cut.' + (flac and 'flac' or 'wav')
ozvuk = join( fpath, ozvuk)
import subprocess
if 'cache':
    wzvuk = splitext( fzvuk)[0] + '.wav'
    if wzvuk != fzvuk and not exists( wzvuk):
        print( '>', wzvuk, start, end)
        subprocess.call( ['sox', fzvuk, wzvuk, ] )
    fzvuk = wzvuk
print( '< ', fzvuk)#, start, end)
print( ' >', ozvuk, start, end)
subprocess.call( [str(s) for s in ['sox', fzvuk, ozvuk, 'trim', start, end]] )

# vim:ts=4:sw=4:expandtab

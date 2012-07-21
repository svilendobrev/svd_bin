#!/usr/bin/env python
#$Id: sumtime.py,v 1.1 2007-03-03 00:42:23 sdobrev Exp $

#usage: filmid.sh *avi *mp3 | sumtime4mplayer.py

import sys
k = 'ID_LENGTH'
s=0
for l in sys.stdin:
    kv = l.split('=')
    if len(kv)>1 and kv[0]==k:
        s += float(kv[1])
m = int(s/60)
print m, 'min', s-m*60, 'sec  === ', s, 'seconds'

# vim:ts=4:sw=4:expandtab

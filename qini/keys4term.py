#!/usr/bin/env python
#$Id: keys4term.py,v 1.1 2006-09-26 09:00:09 sdobrev Exp $
' use: infocmp -L | keys4term.py '

dirs = dict(    #cu-keys
    down =1,
    home =1,
    left =1,
    right =1,
    up =1,

    end =1,     #no cu-key
)



#dirs = cursors.copy()
#dir.update( dict(
#))

pfxs = dict(
    cursor_ =1,
    key_ =1,
)

keys = {}
for pfx in pfxs:
    for dir in dirs:
        keys[ pfx+dir] = 1

for i in range(12):
    keys['key_f'+str(1+i)]=1
print keys.keys()

import sys
f = sys.stdin
all = f.read().split(',')
for p in all:
    p = p.strip()
    try:
        k,v = p.split('=',2)
    except ValueError:
        #print '?',p
        continue
    k = k.strip()
    v = v.strip()
    if k in keys:
        print '%(k)s=%(v)r' % locals()

# vim:ts=4:sw=4:expandtab

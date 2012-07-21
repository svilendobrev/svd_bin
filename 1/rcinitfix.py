#!/usr/bin/env python
#$Id: rcinitfix.py,v 1.1 2006-01-17 03:54:28 sdobrev Exp $
##use as find /etc/rc.d/ -name [KS]\* | rc.py
##use -f to do renaming
import sys,re,os
re_f = re.compile( 'rc(?P<level>\d)\.d/(?P<fullname>(?P<typ>[KS])(?P<num>\d\d)(?P<service>\w+))' )
services = {}

MAXLEVEL=5
MINLEVEL=1

class Service:
    def __init__(me, name):
        me.levels = ['']*(MAXLEVEL-MINLEVEL+1)
        me.types = {}
        me.name = name

for f in sys.stdin:
    m = re_f.search(f)
    if not m: continue
    level = int( m.group('level'))
    if MINLEVEL <= level <= MAXLEVEL:
        s = Service( m.group('service') )
        s = services.setdefault( s.name, s)
        typ = m.group('typ')
        s.levels[ level -MINLEVEL ] = typ
        s.types[ typ ] = m.group('fullname')


do = '-f' in sys.argv
wrongs = 0
typeweight = { None:3, 'K':1, 'S':2 }
for s in services.itervalues():
    print s.name, s.types, '-'.join(s.levels)
    d = None
    i = MAXLEVEL+1
    s.levels.reverse()
    for l in s.levels:
        i-=1
        if not l:
            print ' ??', i
            continue
        if typeweight[d] > typeweight[l]:
            d = l
        elif typeweight[d] < typeweight[l]:
            path = '/etc/rc.d/rc%d.d/' % (i,)
            old = path+s.types[l]
            new = path+s.types[d]
            print '   rename %s %s' % (old,new)
            if do:
                os.rename( old,new)
            wrongs +=1
if wrongs:
    print ':::wrongs:', wrongs
    print ':::use -f to actualy do renaming'
# vim:ts=4:sw=4:expandtab

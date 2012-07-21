#!/usr/bin/env python
#$Id$
import bzrlib.merge3 as mr3

def main(argv):
    # as for diff3 and meld the syntax is "MINE BASE OTHER"
    a = file(argv[1], 'rt').readlines()
    base = file(argv[2], 'rt').readlines()
    b = file(argv[3], 'rt').readlines()

    m3 = Merge3(base, a, b)

    #for sr in m3.find_sync_regions():
    #    print sr

    # sys.stdout.writelines(m3.merge_lines(name_a=argv[1], name_b=argv[3]))
    sys.stdout.writelines(m3.merge_annotated())

import sys
def opt( *xx):
    for x in xx:
        if x in sys.argv: return sys.argv.remove( x ) or True
    return None
argv = sys.argv
lines_cvs = opt( '--cvs', '--lines')    #default
annotated = opt( '--annotate', '--annotated')
groups    = opt( '--group', '--groups', '--grouped')
if not argv[3:] or opt('-h', '--help'):
    print 'as for diff3 and meld the syntax is "MINE BASE OTHER"'
    raise SystemExit


def merge_groups( m):
    'Yield sequence of line groups. see Merge3.merge_groups'
    for t in m.merge_groups():
        if len(t)>2:
            t = t[0],t[1:]
        yield t


a    = file(argv[1], 'rt').readlines()
base = file(argv[2], 'rt').readlines()
b    = file(argv[3], 'rt').readlines()

m3 = mr3.Merge3( base, a, b)

if annotated:
    sys.stdout.writelines( m3.merge_annotated())
elif groups:
    last = None
    for t,g in merge_groups( m3):
        t = dict(a='mine', b='other').get( t,t)
        if t == 'conflict':
            #base,a,b = g
            for x,nm in zip( g, 'base mine other'.split()):
                for l in x:
                    print '%-4s:' % nm, l
            if last: print last
            last = None #r.append( t, '')
            continue
        if not g: continue
        if last:
            if last[0] == t:
                last[1] += len(g)
                continue
            print last
        last = [t, len( g)]
    if last: print last

else: #lines_cvs
    sys.stdout.writelines( m3.merge_lines())
# vim:ts=4:sw=4:expandtab

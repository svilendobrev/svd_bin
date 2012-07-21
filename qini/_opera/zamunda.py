#!/usr/env/bin python
import sys
n,m = sys.argv[1:]
for a in range(int(n)):
    for b in range(int(m)):
        if b: print ', ',
        print '*[title~="S%02dE%02d"]' % (a+1,b+1),
    print ' { display : none }'
# vim:ts=4:sw=4:expandtab

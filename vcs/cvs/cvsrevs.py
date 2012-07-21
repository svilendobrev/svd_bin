#!/usr/bin/env python
#$Id: cvsrevs.py,v 1.2 2006-06-23 15:15:36 sdobrev Exp $
import os,re
_r_rev = '([\d\.]+)'
def cvsrevisions( target):
    cmd = 'cvs log %(target)s' % locals()
    print cmd
    r_rev  = re.compile( '^revision '+_r_rev )
    r_date = re.compile( '^date: ([\d\.\/]+ [\d:]+)')
    all_revs = {}
    revision = None
    for l in os.popen( cmd):
        m = r_rev.search( l)
        if m:
            revision = m.group(1)
            continue
        m = r_date.search( l)
        if m:
            date = m.group(1)
            all_revs[ revision] = date
            continue
    return all_revs

if __name__=='__main__':
    import sys
    target = sys.argv[1]
    print cvsrevisions( target)

# vim:ts=4:sw=4:expandtab

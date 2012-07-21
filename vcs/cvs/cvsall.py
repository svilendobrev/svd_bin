#!/usr/bin/env python
#$Id: cvsall.py,v 1.2 2006-06-23 15:19:10 sdobrev Exp $

import os,re
#ROOT = os.popen( 'cat CVS/Repository' )

import sys
target = sys.argv[1]

print target
if not os.access( target, os.R_OK):
    print ' ! file %(target)r does not exist' % locals()
    raise SystemExit, -1
ls = 'ls -lF '+target
os.system( ls)

class stat:
    r_ = '''\
File: (?P<file>\S+) Status: .*
\s*
Working revision: (?P<workrev>[\d\.]+)
Repository revision: (?P<reprev>[\d\.]+)
'''.replace('\n','\s*').replace(' ', '\s*')
#Sticky Tag:          (none)
#Sticky Date:         (none)
#Sticky Options:      (none)
    r_stat = re.compile( r_)
    def __init__( me, target):
        cmd = me._cmd = 'cvs stat '+target
        f = os.popen( cmd )
        out = me._result = f.read()
        err = f.close()
        m = me.r_stat.search( out)
        if not m:
            print ' ! cannot understand:', cmd, ':'
            print out
            print '-- retCode', err
            print '-- regexp:', me.r_
            raise SystemExit, -1
        me.__dict__.update( m.groupdict() )

s = stat( target)
#print s.__dict__

print 'original-version:', s.workrev
revs = s.reprev.split('.')
revBASE = '.'.join( revs[:-1])
revTO = int( revs[-1])
def revBASEx(x): return revBASE + '.%d' % (x,)
print 'loop versions: ', revBASEx(1), 'to', revBASEx( revTO)

print 'continue?'
sys.stdin.readline()

def cvsget( target, ver):
    cmd = 'cvs up -r %(ver)s %(target)s' % locals()
    os.system( cmd)

os.rename( target, target+'.org' )

while revTO>0:
    ver = revBASEx( revTO)
    print target, '.', ver
    cvsget( target, ver)
    os.rename( target, target+'.'+ver )
    revTO -= 1

print '---'
print 'restoring', target, 'to', s.workrev
if s.workrev == s.reprev:
    print ' i.e. HEAD'
    cmd = 'cvs up -A %(target)s' % locals()
    os.system( cmd)
else:
    cvsget( target, s.workrev)
os.rename( target+'.org', target)
os.system( s._cmd)
os.system( ls)

# vim:ts=4:sw=4:expandtab

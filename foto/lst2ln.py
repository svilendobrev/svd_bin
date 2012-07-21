import sys
import os
from os.path import join, islink, isfile, isdir, basename, normpath
if len(sys.argv)<2:
    raise SystemExit, 'use: '+sys.argv[0]+' prefix-path [-n(one) -q(uiet) -a(ll) -r(ooted-dir-filter)] < file-list'

que = {}
path = sys.argv[1]
assert isdir( path)

none   = '-n' in sys.argv[2:]
quiet  = '-q' in sys.argv[2:]
all    = '-a' in sys.argv[2:]
rooted = '-r' not in sys.argv[2:]
target_pfx = ''

for l in sys.stdin:
    l = l.strip()
    l = l.replace( ' ', '')
    if not l: continue
    l = l.replace( '+?', '?+')
    if (l[-1] in '+=') or all:
        nm = all and l or l.rstrip('+=')
        nm = nm.rstrip(':')
        print nm
        if isdir( nm):
            target_pfx = normpath( nm)
            print 'dir', target_pfx
            if target_pfx=='.': target_pfx=''
            continue
        dst = basename( nm)
        dst = dst.rstrip('?')
        l = que.setdefault( dst, [])
        l.append( ( target_pfx, nm ) )

found = {}
#rooted=0
for root, dirs, files in os.walk( path ):
    if not rooted:
        dd = [ d for d in dirs if d[0] in '123456789' or d=='jpg']
        print 'rooted filtering:', dirs, '->', dd
        dirs[:] = dd
        rooted = 1
    for name in files:
        full = join(root, name)
        #print '?',full
        try:
            dup = found[ name]
        except KeyError: pass
        else:
            print full, 'duplicates', dup
            continue

        try:
            org = que[ name]
        except KeyError: continue
        else:
            found[ name] = full
            del que[ name]
            for target_pfx,org in org:
                dst = name
                if org[-1]=='?':
                    pp = dst.split('.')
                    pp[-1:-1] = '?'
                    dst = '.'.join( pp)
                dst = dst.replace( 'CRW', 'img')
                src = full
                if not isfile( src):
                    print 'inexistent', src
                else:
                    if target_pfx:
                        lvl = 1+target_pfx.count('/')
                        dst = join( target_pfx, dst)
                        src = '../' * lvl + src
                    if not quiet:
                        print dst, '->', src
                    if not none:
                        if islink( dst): os.remove( dst)
                        os.symlink( src,dst)


v = que.values()
v.sort()
for name in v:
    print 'inexistent', name

#!/usr/bin/env python

#$Id$
#rename $dst/trackXXX* as of src/XXXname*

import sys, os, re

try: sys.argv.remove( '-autocyr2lat'); autocyr2lat=True
except: autocyr2lat= False

verbose = None

src = sys.argv[1]
dst = sys.argv[2]
print '#renamimg', dst, 'as', src

re_fname = re.compile( '^(\d+)')
fnames = {}
fn_iter = os.path.isdir(src) and os.listdir( src) or open(src)
for a in fn_iter:
    a = a.strip()
    if not a or a[0]=='#': continue
    if verbose: print '#', a
    m = re_fname.search( a)
    if not m:
        print '#unknown filenaming: '+a
        continue
    if autocyr2lat:
        a = a.replace(',','-')
        a = a.replace(' ','-')
        a = a.replace('_','-')
        a = a.replace('---','-')
        a = a.replace('--','-')
        import lat2cyr

        a = lat2cyr.zvuchene.cyr2lat( a)
        a = a.lower()
        if verbose: print '# ->', a

    fnames[ int(m.group(1))] = a

print '#src:', len(fnames), 'files'

re_trk = re.compile( '(track.*?)?(\d+)(\..*?)')
for f in os.listdir( dst):
    m = re_trk.match( f)
    if m:
        n = m.group(2)
        fn = fnames.get( int(n) )
        if fn is not None:
            ext = os.path.splitext( f)[-1]
            if not fn.endswith( ext):
                fn += ext
            print 'mv', f, fn
        else:
            print '# !not found', f, `n`
    else:
        print '# unknown filenaming: '+f

# vim:ts=4:sw=4:expandtab

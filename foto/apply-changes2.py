import os, sys
join = os.path.join

none = '-n' in sys.argv
tree = {}
paths = set()
try:
    os.mkdir( 'del')
except Exception, e: print e

for path, dirs, files in os.walk( '2/' ):
    for name in files:
        assert name not in tree, name
        pp = path.split( '/')
        tree[ name] = p = join( *pp[1:] )
        paths.add( p)
        #print pp,name

if not none:
    for p in paths:
        try:
            os.makedirs( p)
        except : pass

for path, dirs, files in os.walk( '.' ):
    if path == '.':
        try:
            dirs.remove( '2' )
        except: pass
    for name in files:
        if name not in tree:
            print 'deleted', name
        target = tree.get( name, 'del' )
        if not target:
            if '.' == path: continue
        else:
            if join( '.', target) == join( path):
                continue
        a = join( path, name )
        b = join( target, name)
        print a, '>', b
        if not none: os.rename( a,b)


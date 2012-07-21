import os,sys
if 0:
    if len(sys.argv)<3:
        print 'renenc -iencoding [oencoding]use as filter: enc2enc [-]input-encoding [-]output-encoding <input >output'
        print '  the -enconding will reverse text'
        raise SystemExit
    e_from = sys.argv[1]
    e_to = sys.argv[2]
    reverse = False
    if e_from[0]=='-':
        e_from = e_from[1:]
        reverse = not reverse
    if e_to[0]=='-':
        e_to= e_to[1:]
        reverse = not reverse

def opt( *xx):
    for x in xx:
        if x in sys.argv: return sys.argv.remove( x ) or True
    return False

fake     = opt('-n', '--fake')

ienc = 'utf8'
if opt('-icp1251', '-i=cp1251'): ienc = 'cp1251'
if opt('-icp866', '-i=cp866'): ienc = 'cp866'
oenc=None
if opt('-ocp1251', '-o=cp1251'): oenc = 'cp1251'
if opt('-outf8', '-o=utf8'): oenc = 'utf8'

for dir in sys.argv[1:]:
    for x in os.listdir( dir ):
        fn = x.decode( ienc)
        print x, fn
        if fake: continue
        if oenc: fn = fn.encode( oenc)
        os.rename( *(os.path.join( dir,f) for f in (x, fn)))

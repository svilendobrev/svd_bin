#!/usr/bin/env python
import sys,socket,anydbm, os.path
from util import optz
import multiprocessing as mp

#TODO: timed cache
optz.any( 'cache', help= 'filename to store cache [%default]', default= 'ip2hs.cache')
optz.any( 'prefix', help= 'extra prefix on each line')
optz.bool( 'ipprefix', help= 'put i.p.= as prefix on each line')
optz.int( 'timeout', help= 'timeout in seconds [%default]', default=5)
optz.bool( 'merge_caches', help= 'merge all given arguments as caches', )
optz.int( 'parallel', default=3, help= 'how many DNS queries at same time', )
optz,args = optz.get()

db= anydbm.open( optz.cache, 'c')
if optz.merge_caches:
    for a in args:
        if os.path.exists( a):
            db.update( anydbm.open( a).iteritems())
    raise SystemExit

timeout = optz.timeout
if hasattr(socket, 'setdefaulttimeout'):
    socket.setdefaulttimeout( timeout)

cache = {}  # loaded at start, saved at end
cmiss = {}
cache.update( db.iteritems() )
db.close()
totals=0

def ip2host( ip):
    #print >>sys.stderr, os.getpid(), ip
    try: host,alias,ips = socket.gethostbyaddr( ip)
    except : host = ip
    return host

pool = mp.Pool( processes= optz.parallel)
func = optz.parallel>1 and pool.apply_async or apply

rr = []
for a in sys.stdin:
    try:
        ip,r = a.rstrip().split(' ',1)
    except:
        continue
    host = cache.get( ip)
    if host is None:
        #print >>sys.stderr, 'mis:', ip
        host = func( ip2host, [ip])
        cache[ ip] = cmiss[ip] = host
    totals+=1
    rr.append( (ip,host,r) )

    if not totals % 1024:
        db= anydbm.open( optz.cache, 'r')
        cache.update( db.iteritems() )
        db.close()

print >>sys.stderr, 'misses:', len(cmiss), ' totals:', totals

for ip,host,r in rr:
    if not isinstance( host, str):
        host = host.get()
        cmiss[ip] = host
    r = host + ' ' + r
    if optz.ipprefix: r = ip + '= ' + r
    if optz.prefix: r = optz.prefix + r
    print r

if cmiss:
#    import random,time
#    random.seed( optz.prefix+str(len(cmiss)))
#    time.sleep( random.randint(0,9)/10.0)
    try:
        db= anydbm.open( optz.cache, 'c')
        db.update( cmiss.items() )
    except Exception,e:
        print >>sys.stderr, 'errrr:', e
        db= anydbm.open( optz.prefix +'.'+ optz.cache, 'c')
        db.update( cmiss.items() )

# vim:ts=4:sw=4:expandtab

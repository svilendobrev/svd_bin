#!/usr/bin/env python3
import sys,socket, os.path
from svd_util import optz
#import multiprocessing as mp
#import threading as mp
import concurrent.futures

def lprint( *a):
    print( *a, file= sys.stderr)

#TODO: timed cache
optz.any( 'cache', help= 'filename to store cache [%default] or url like tt://host:port', default= 'ip2hs.cache')
optz.any( 'prefix', help= 'extra prefix on each line')
optz.bool( 'ipprefix', help= 'put i.p.= as prefix on each line')
optz.int( 'timeout', help= 'timeout in seconds [%default]', default=9)
optz.bool( 'merge_caches', help= 'merge all given arguments as caches', )
optz.int( 'parallel', default=3, help= 'how many DNS queries at same time', )
optz.bool( 'verbose', help= 'debug', )
optz,args = optz.get()

timeout = optz.timeout
if hasattr( socket, 'setdefaulttimeout'):
    socket.setdefaulttimeout( timeout)

def items( db): return db.items()
def update( db, i): return db.update(i)

hp = optz.cache.split('://')
if hp[0]=='tt':
    from svd_util.ext import pytyrant3 as pytyrant
    hp = hp[-1].split(':') #'127.0.0.1', 1978)
    if len(hp)>1:
        h,p = hp
    else:
        h,p = hp,None
    ka = {}
    if h: ka['host'] = h
    if p: ka['port'] = int(p)
    tt = pytyrant.PyTyrant.open( **ka)
    cache = db = tt
if hp[0]=='redis':
    import redis
    #   redis://[:password]@localhost:6379/0
    #   unix://[:password]@/path/to/socket.sock?db=0
    rd = redis.Redis.from_url( optz.cache) #Redis(host='localhost', port=6379, db=0)
    cache = db = rd
    _dbname = 'ip2host'
    if not rd.dbsize():
        rd[ '_dbname'] = _dbname
    else:
        dbname = rd.get( '_dbname')
        if dbname is not None: dbname = dbname.decode( 'utf8')
        assert dbname == _dbname, dbname
else:
    try:
        import dbhash as adb
    except:
        import dbm as adb
        def items( db):
            for k in db.keys(): yield k,db[k]
        def update( db, i):
            for k,v in i: db[k] = v
    #import anydbm as adb
    db= adb.open( optz.cache, 'c')
    if optz.merge_caches:
        for a in args:
            if os.path.exists( a):
                update( db, items( adb.open( a)))
        raise SystemExit
    cache = {}  # loaded at start, saved at end

cmiss = {}
if cache is not db:
    cache.update( items(db) )
    db.close()
totals=0

def ip2host( ip):
    #print >>sys.stderr, os.getpid(), ip
    try: host,alias,ips = socket.gethostbyaddr( ip)
    except : host = ip
    return host

if 0:
    pool = mp.Pool( processes= optz.parallel)
    func = optz.parallel>1 and pool.apply_async or apply
    def result( f): return f.get()
else:
    pool = concurrent.futures.ThreadPoolExecutor( max_workers= optz.parallel)
    def func( f, args): return pool.submit( f, *args)
    def result( f):
        if optz.verbose: lprint( 'res', f)
        return f.result()


rr = []
for a in sys.stdin:
    try:
        ip,r = a.rstrip().split(' ',1)
    except:
        continue

    if ip in cmiss:
        host = None
    else:
        host = cache.get( ip)
        if host is None:
            if optz.verbose: lprint( 'mis:', ip)
            host = func( ip2host, [ip])
            if optz.verbose: lprint( 'fin:', ip, repr(host) )
            cmiss[ip] = host
            if cache is not db:
                cache[ ip] = host
    totals+=1
    rr.append( (ip,host,r) )

    if cache is not db:
        if not totals % 1024:
            db= adb.open( optz.cache, 'r')
            cache.update( items(db) )
            db.close()


lprint( 'misses:', len(cmiss), ' totals:', totals, optz.prefix)

n=0
pp=0
for ip,host,r in rr:
    if not isinstance( host, (str,bytes)):
        h = cmiss[ip]
        if isinstance( h, (str,bytes)): host = h
        else:
            c = cache.get(ip)
            if c is not None and c is not h:
                host = c    #someone already did it
            else:
                assert host, ip
                if optz.verbose: lprint( 'q:', ip)
                host = result( host)
                if optz.verbose: lprint( 'r:', ip, host)
                if cache is db: cache[ip] = host
            cmiss[ip] = host
            n+=1
            p = ((10*n)//len(cmiss))
            if p != pp:
                lprint( p, optz.prefix)
                pp = p
            #if not (((100*n)//len(cmiss)) % 10): lprint( n, optz.prefix)
    if isinstance( host, bytes):    #WTF with redis
        #print( 'by', repr(host))
        host = host.decode( 'utf8')
    r = host + ' ' + r
    if optz.ipprefix: r = ip + '= ' + r
    if optz.prefix: r = optz.prefix + r
    print( r)

if cmiss and cache is not db:
#    import random,time
#    random.seed( optz.prefix+str(len(cmiss)))
#    time.sleep( random.randint(0,9)/10.0)
    try:
        db= adb.open( optz.cache, 'c')
    except Exception as e:
        lprint( 'errrr:', e)
        db= adb.open( optz.prefix +'.'+ optz.cache, 'c')
    update( db, cmiss.items() )

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python

def get_crc32( s):
    s= s.lower()
    bytes = bytearray(s)
    crc = 0xffffffff;
    for b in bytes:
        crc = crc ^ (b << 24)
        for i in range(8):
            if (crc & 0x80000000 ):
                crc = (crc << 1) ^ 0x04C11DB7
            else:
                crc = crc << 1;
        crc = crc & 0xFFFFFFFF

    return '%08x' % crc

def get_hash( a):
    st = os.stat( a)
    time = st.st_mtime or st.st_ctime
    #PRId64 = 'I64d'
    #return hash.Format("d%"+PRId64+"s%"+PRId64, time, st.st_size);
    return 'd%ds%d' % (time, st.st_size)



import sys, os
from os.path import *
target = expanduser( '~/.xbmc/userdata/Thumbnails/')

from svd_util import optz
caches='0 ln sym'.split()
optz.str( 'cache', type='choice', choices= caches,
            help='fake the cache, and how - 0=empty file, ln=hardlink, sym=symlink')
optz.str(   'sqltextures',  help= 'path to the Textures13.db, to fill the texture table with fake rows' )
optz.bool(  'sqlsizes',     help= 'fill relations to sizes table')

optz,argz = optz.get()

def walker( a):
    for path,dirs,files in os.walk( a):
        for f in files:
            fp = join( path, f)
            c = get_crc32( fp)
            cf = join( c[0], c + splitext(f)[-1].lower() )
            cfp = join( target, cf)
            yield fp, c, cf, cfp

if optz.sqltextures:
    from sqlalchemy import create_engine, MetaData, bindparam, sql
    eng = create_engine( 'sqlite:///' + expanduser( optz.sqltextures))
    meta = MetaData( eng, reflect= True)
    #for t in meta.sorted_tables: print t

    texture = meta.tables['texture']
    # texture (id integer primary key, url text, cachedurl text, imagehash text, lasthashcheck text);
    # sizes (idtexture integer, size integer, width integer, height integer, usecount integer, lastusetime text)
    sizes   = meta.tables['sizes']

    item0   = dict( lasthashcheck= '2013-03-03 12:54:29')   #imagehash= len('d1348783086s2093477')*'a',
    szitem0 = dict( size=1, width= 100, height=100, usecount=1, lastusetime = '2013-03-03 12:54:29')

    def item( fp, cf):
        return dict( _url= fp, _cachedurl= cf, _imagehash= get_hash( fp) )

    def hascount( table, clause):
        s = table.count( clause)
        r = meta.bind.execute( s)
        row = r.fetchone()
        c = row[0]
        r.close()
        return c


    MAXL = 500
    buff = []
    def save( fp, cf, flush =False):
        if not flush:
            fp = fp.decode('utf8')
            c = hascount( texture, texture.c.url == fp)
            if c:
                print 'has', fp
                return
            buff.append( item( fp, cf))
            if len(buff)<MAXL: return
        if not buff: return

        print 'saving texture', fp
        r = texture.bind.execute(
            texture.insert().values(
                url= bindparam('_url'),
                cachedurl= bindparam('_cachedurl'),
                imagehash= bindparam('_imagehash'),
                **item0),
            buff[ :MAXL] )

        del buff[ :MAXL]


for a in argz:
    if isdir( a):
        for fp, crc, cf, fcache in walker( a):
            if optz.cache:
                ex = exists( fcache)
                print fcache, ex
                if not ex:
                    if optz.cache == '0':
                        open( fcache, 'w').close()
                    elif optz.cache == 'ln':
                        os.link( fp, fcache)
                    elif optz.cache == 'sym':
                        os.symlink( fp, fcache)
                    else:
                        assert 0, optz.cache
            if optz.sqltextures: save( fp, cf)
            #f len(buff)>7: break
    else: #a = a.decode('utf8')
        print get_crc32( a)
        print get_hash( a)


if optz.sqltextures:
    save( 0,0,flush=True)

    if optz.sqlsizes:
        hasno = []
        for row in meta.bind.execute( texture.select()):# [ texture.c.id ])):
            c = hascount( sizes, sizes.c.idtexture == row['id'])
            if c:
                print row['id'], 'has'
            else: hasno.append( row['id'] )

        while hasno:
            print 'saving sizes'
            sizes.bind.execute(
                sizes.insert().values( idtexture= bindparam('_idtexture'), **szitem0),
                [ dict( _idtexture= id) for id in hasno[:MAXL] ] )
            del hasno[ :MAXL]


''' src functions:
bool CTextureDatabase::GetCachedTexture(const CStdString &url, CTextureDetails &details)
.. sql

bool CTextureCacheJob::CacheTexture(CBaseTexture **out_texture)

CStdString CTextureCacheJob::GetImageHash(const CStdString &url) {
'''
# vim:ts=4:sw=4:expandtab

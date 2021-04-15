import sys
igla = bytes( [0xFF,0xD8,0xFF,0xE1,0x6B,0xFE, ]+ [ord(x) for x in 'Exif'] ) #.fromhex
#igla = bytes( 'Canon'.encode('ascii'))
print( igla)
szigla = len(igla)

out = None
a = open( sys.argv[1], 'rb')
n = 0
d = bytes()
found = 0

def save( ofs):
    global out
    print( '>>', n, (szigla if not out else 0)+ofs, d[:20])
    if not out:
        out = open( f'ig{n:05d}', 'wb')
        if found: out.write( igla )
    out.write( d[:ofs])
    out.close()
    out= None

l=0
while a:
    r = a.read( 1024*1024*100)
    if not r: break
    l+=len(r)
    d += r
    r = None
    while 2:
        ofs = d.find( igla)
        print( ofs, len(d), l)
        if ofs <0:
            print( '>>>', n, szigla+ofs, d[:20])
            if 10:
                if not out:
                    out = open( f'ig{n:05d}', 'wb')
                    if found: out.write( igla )
                out.write( d[:-szigla])
                d = d[-szigla:]
            break   #read more
        save( ofs)
        found = 1
        n+=1
        d = d[ ofs+szigla:]

save( len(d))
#    print( '>>', n, szigla+len(d))
#    if 10:
#     with open( f'ig{n}', 'wb') as out:
#        out.write( igla + d)

# vim:ts=4:sw=4:expandtab

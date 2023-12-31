import vobject

#HACKed
#vcard.py#156
# VCardTextBehavior.encode()
#..
#            if encoding and encoding.upper() in (cls.base64string, 'BASE64'):
#..

import sys
vcf = open( sys.argv[1]).read()

vcf = vcf.replace( '=\n=', '=')
tt = []
ooall = []
for o in vobject.readComponents( vcf,
                    #ignoreUnreadable=False,
                    allowQP=True
                    ):
    #o.prettyPrint()
    ooall.append( o)
    #print( o.contents)
    fn = o.fn.value
    #n = o.n.value  and then .additional .family .given .prefix .suffix
    #tt.append( (fn, ':', o.tel.value))
    #print( fn, o.tel ) #o.contents) #type(o))#.tel.params)# , type(o.tel))#.TYPE , dir(o.tel), )
    tt.append( fn + ': '+ '  '.join(a.value for a in o.contents.get('tel',()) ))
    #print( fn, o.tel.params)# , type(o.tel))#.TYPE , dir(o.tel), )

print( '\n'.join( sorted( tt, key= lambda x: x.lower())))
print( '-------------')
print( ''.join( o.serialize().replace( '\r\n', '\n') for o in ooall))

if 0:
 vcardstart = 'BEGIN:VCARD'
 for v in vcf.split( vcardstart):
    if not v.strip(): continue
    #print(v)
    v = v.replace( '=\n=', '=')
    o = vobject.readOne( vcardstart+v)
    o.prettyPrint()
    print( o.contents)#dict(o))

# vim:ts=4:sw=4:expandtab

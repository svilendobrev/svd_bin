#!/bin/env python
# -*- coding: utf-8 -*-

import sys, codecs, encodings, os
if 0:
    a = ' '.join( sys.argv[1:])
    for e in sorted(set(encodings.aliases.aliases.values())):
        print e, ':',
        try:
            #print a.decode( e).encode( 'cp1251')
            print a.decode( e, 'replace').encode( 'cp1251', 'replace')
        except Exception,ex: pass#print ex
        for dt in +64,+32,-32,-64:
            try:
                for c in a:
                    oc = ord(c)
                    if oc>=128:
                        c = chr(oc+dt)
                    print c.decode( e, 'replace').encode( 'cp1251', 'replace'),
            except Exception,ex: pass#Eprint ex
            print

xx = {}
ax = {
'ЕСЯЎїю¬б єб': 'Песничка за',
'ЕїФЫУ': 'Питър',
'обФЇ ьбУї': 'Матю Бари',
'д«¬Ф«У мї¬б¬ ЎС н«Ѕї': 'Доктор Никак не боли',
'Єїу':'жив',
'сТжј»йтвщЮµЖъ®З':'дуСмпВхГЧшцТгйА',
'ыбУ¬їЎґ Єбнб':'Царкиня жаба',
'иЪ':'Кщ',
}
for k,v in ax.items():
    for c,t in zip( k,v):
        oc = xx.get(c)
        if oc is None:
            xx[c] = t
        elif oc != t:
            print 'dupl-wrong', c,t,oc

def tx( a):
    return ''.join( xx.get(c,c) for c in a)

argv = sys.argv[1:]
if argv:
    for a in argv:
        print a, '->', tx(a)
        os.rename( a, tx(a))
else:
    for a in sys.stdin:
        print tx(a),

if 0:
    s = ''.join(sorted(xx.keys()))
    print ' '.join(xx[a] for a in s)
    print s.encode('hex')
    print ''.join(xx[a] for a in s).encode('hex')

# vim:ts=4:sw=4:expandtab

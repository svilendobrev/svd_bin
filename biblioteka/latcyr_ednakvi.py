#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
'еднакво-изглеждащи букви - латиница, кирилица, други'

lc1= tuple( a+b for a,b in zip(
    'ABEKMHOPCTYXaekopcyx',     #некирилица
    'АВЕКМНОРСТУХаекорсух',     #цел-кирилица
    ))
lc2= lc1 + tuple( a+b for a,b in zip(
    'nug',
    'пид',
    ))
assert all( ord(x)<127 for x,y in lc1+lc2 )
assert all( ord(y)>1000 for x,y in lc1+lc2 )

i_drugi = tuple( a+b for a,b in {
        '\u2013': '-' ,   #-  ndash?...
        '\u0406': 'I' ,   #І  римско 1
        '\xA0'  : ' ',
        }.items())


def lc_ok4ignorecase( lc):    #връща които са еднакви при големи и малки букви
    return tuple( x+y for x,y in lc
                    if (x+y).lower() in lc and (x+y).upper() in lc
                    )
lc10 = lc_ok4ignorecase( lc1 )
lc20 = lc_ok4ignorecase( lc2 )


def lc_regex_r( x, tablica =lc1, ot_kirilica =True):
    ot_kirilica = bool( ot_kirilica)
    for a in tablica:
        x = x.replace( a[ ot_kirilica], '['+a[0]+a[1]+']' )
    return x

def lc_subst_r( x, tablica =lc1, kym_kirilica =True):
    kym_kirilica = bool( kym_kirilica)
    for a in tablica:
        x = x.replace( a[ not kym_kirilica], a[ kym_kirilica] )
    return x

#тези са 10-пъти по бързи..
_dicts = {},{}
def _tablica( tablica, ot_kirilica =True):
    ot_kirilica = bool( ot_kirilica)
    rtablica = _dicts[ ot_kirilica].get( tablica)
    if not rtablica:
        rtablica = _dicts[ ot_kirilica ][ tablica ] = dict( tablica) if ot_kirilica else dict( (y,x) for x,y in tablica)
    return rtablica

def lc_regex_d( x, tablica =lc1, ot_kirilica =True):
    tablica = _tablica( tablica, not ot_kirilica)
    return ''.join( a if a not in tablica else '['+tablica[a]+a+']'
                for a in x)

def lc_subst_d( x, tablica =lc1, kym_kirilica=True):
    tablica = _tablica( tablica, kym_kirilica)
    return ''.join( tablica.get( a, a) for a in x)

lc_subst = lc_subst_d
lc_regex = lc_regex_d

if __name__ == '__main__':
    for txt,exp, tablica in [
        ['абвгде-IJ К', '[aа]бвгд[eе][–-][ІI]J[\xa0 ][KК]', lc1+i_drugi],
        ['аАбвгийклмНнопР', '[aа][AА]бвгий[kк]лмНн[oо]п[PР]', lc10],
        ['аАбвгийклмНнопР', '[aа][AА]бвгий[kк]лмНн[oо]п[PР]', lc20],
        ['аАбвгийклмНнопР', '[aа][AА]бвг[uи]й[kк]лм[HН]н[oо][nп][PР]', lc2],
        ]:
        r = lc_regex_r( txt, tablica)
        assert r == exp, (txt,r,exp)
        r = lc_regex_d( txt, tablica)
        assert r == exp, (txt,r,exp)

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#$Id$
# Сричкопренасяне за български език.
# Bulgarian hyphenation rules. (c) 2009 svd.
# cp1251/utf8 text, HTML:softhyphen
# original: wh2.c/hyrules.c (c) svd ~1991 reversed from izdatel 1.0

__all__ = [ 'hyphtext', 'HTML_HYPHEN' ]

class config:
    hyphen = '-'
    minsize = 4

VOCALS = u'АЕИОУЪЮЯ'.upper()
VOCALS += VOCALS.lower() #''.join( chr(ord(v)+32) for v in VOCALS)
VOCALS = dict( (v,v) for v in VOCALS)

#def vocal(x): return x in VOCALS

def hyphword( src, hyphen =config.hyphen, minsize =config.minsize):
    'this only knows about VOCALS, all else assumed a letter'
    #print 111100000, src
    n = len(src)
    if n< minsize: return src

    for firstH in range(n):
        if src[ firstH] in VOCALS: break #FIRST vocal
    for lastH in range( n-1, 0, -1):
        if src[ lastH] in VOCALS: break   #LAST vocal
    if firstH<2: firstH=2       #LONELY letters are not hyphenated
    if lastH==n-1: lastH-=1     #LONELY letters are not hyphenated
    if firstH>lastH: return src

    res = src[:firstH]
    for i in range( firstH, lastH+1):
        if hyphrules( src, i):
            res+= hyphen   #? Hyphenable BEFORE i-th position
        res+= src[i]
    res += src[ lastH+1:]

    #print 111111111, src,res
    return res


def hyphrules( word, x): #ret bool ; x=offset-in-word
    '''
   #cpp, cp, cx, cn;   // pre-previous, previous, current (x), next char
   I. vocal CX : 1. vocal CP - ДА - между гласни                    @vV
                 иначе  НЕ - след съгласна и преди гласна           @nV
   II. !vocal CX
    1. vocal CP
      1. vocal CN    1. vocal CPP & vocal CPPP - НЕ -
                       -  след тройна гласна преди една! съгласна   @vvvNv
                      иначе ДА - след гласна преди една! съгласна   @vNv
      2. !vocal CN   1. CX,CN = "ДЖ" - ДА - след гласна преди ДЖ    @vДЖ
                      иначе НЕ - след гласна преди две! съгласни    @vNn
    2. !vocal CP :
      1. CX="Ь" | CP=CPP | CX=CN   - НЕ  -    между съгласна и Ь    @nЬ
                                             след  двойна! съгласна @zzN
                                             преди двойна! съгласна @nZZ
      2. CP,CX = "ДЖ" - НЕ - между ДЖ                               @дЖ
      3. CP="Й" 3.1 !vocal CN - НЕ  - след Й преди две съгласни     @йNn
      иначе ДА  между две съгласни                                  @nN

     заб.: горните правила не пренасят примерно пре-крати, а прек-рати
'''
    cpp,cp,cx,cn= word[x-2:x+1+1]

    if (cx in VOCALS):
        return (cp in VOCALS)
    if (cp in VOCALS):
        if (cn in VOCALS):
            return not (x>2 and (word[x-3] in VOCALS) and (cpp in VOCALS))
        return cx in u'Дд' and cn in u'Жж'
    return not (cx in u'Ьь' or cpp==cp or cx==cn or
              cp in u'Дд' and cx in u'Жж' or
              cp in u'Йй' and not (cn in VOCALS) )

LETTERS = ''.join( chr(v) for v in range(ord(u'А'.encode('cp1251')),ord(u'Я'.encode('cp1251'))+1) ).decode( 'cp1251') #А..Я
LETTERS += LETTERS.lower()
LETTERS = dict( (v,v) for v in LETTERS)

_on = True
def hyphtext( src, htmlpre =False, **kargs):
    'use this one as general hyphenator'
    r=''    # using yield is 2x slower
    word = ''
    global _on
    #_on = True
    for c in src:
        if _on and c in LETTERS:
            word+=c
        else:
            if word: r+= hyphword( word, **kargs)
            word = ''
            r+=c
            if htmlpre:
                if r.endswith('<pre>'):     _on = False
                elif r.endswith('</pre>'):  _on = True

    if word: r+= hyphword( word, **kargs)
    return r

HTML_HYPHEN = '&shy;'

txt  = u'алабаланица турска паница джинджифил прекрати пантера, и кога колко не е тъй-като'
tsz4 = u'ала~ба~ла~ни~ца тур~с~ка па~ни~ца джин~джи~фил прек~ра~ти пан~те~ра, и ко~га кол~ко не е тъй-ка~то'

def test():
    t0,t1 = txt, tsz4
    cfg = dict( hyphen= '~', minsize= 4)
    print cfg
    def tst( res, exp):
        if res != exp:
            print '\n %(res)s ?=\n %(exp)s' % locals()
            assert res == exp
    for w,w1 in zip( t0.split(), t1.split() ):
        tst( hyphtext( w, **cfg), w1 )
    tst( hyphtext( t0, **cfg), t1 )
    print t1


if __name__ =='__main__':
    import optparse
    oparser = optparse.OptionParser( u'''
    %prog [options] <infile  >outfile
    %prog [options] думи за пренасяне ...
    '''.rstrip())
    def optany( name, *short, **k):
        return oparser.add_option( dest=name, *(list(short)+['--'+name.replace('_','-')] ), **k)
    def optbool( name, *short, **k):
        return optany( name, action='store_true', *short, **k)
    optany( 'hyphen', help= u'"тире" за отбелязване на пренасянето (меко/скрито-тире); подразбира се "%default"', default= config.hyphen )
    optbool( 'html',  help= u'ползва HTML-меко-тире %(HTML_HYPHEN)r (вместо горното)' % locals() )
    optbool( 'htmlpre',  help= u'пропуска съдържанието на <pre>..</pre> групи' )
    optany( 'minsize', type=int, help= u'думи под тази дължина не се пренасят; подразбира се %default', default =config.minsize )
    optbool( 'utf',   help= u'вх/изх utf8' )
    optbool( 'iutf',  help= u'вх  utf8' )
    optbool( 'iguess',  help= u'вх  познай кодировката' )
    optbool( 'outf',  help= u'изх utf8' )
    optbool( 'i1251', help= u'вх  cp1251' )
    optbool( 'o1251', help= u'изх cp1251' )
    optbool( 'cp1251',help= u'вх/изх cp1251' )
    optbool( 'test',  help= u'самопроверка' )
    optbool( 'demo',  help= u'демо' )
    options,args = oparser.parse_args()

    if options.test:
        test()
        raise SystemExit,0

    cfg = dict(
        hyphen= options.html and HTML_HYPHEN or options.hyphen,
        htmlpre=options.html and options.htmlpre,
        minsize= options.minsize, )

    def ienc(a):
        if options.iutf or options.utf: a = a.decode('utf8')
        elif options.i1251 or options.cp1251: a = a.decode('cp1251')
        return a
    def oenc(a):
        if options.outf or options.utf: a = a.encode('utf')
        elif options.o1251 or options.cp1251: a = a.encode('cp1251')
        return a

    if options.demo:
        print oenc( hyphtext( txt, **cfg))
        raise SystemExit,0

    if args:
        for a in args:
            print oenc( hyphtext( ienc(a), **cfg)),
    else:
        import sys
        tt = sys.stdin
        if options.iguess:
            import eutf
            tt = eutf.readlines(tt)
            def ienc(a): return a

        if 0: tt = tt.readlines() * 10  #profile
        for l in tt:
            print oenc( hyphtext( ienc(l.rstrip()), **cfg))

# vim:ts=4:sw=4:expandtab

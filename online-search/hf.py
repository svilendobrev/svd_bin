#!/usr/bin/env python
# -*- coding: utf-8 -*-
import html5lib
from xml.etree import ElementTree as eltree
from urllib.request import urlopen
import sys, glob
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from svd_util import optz
from svd_util.eutf import fix_std_encoding, filew


def prn( *a,**ka): return print( file= sys.stderr, *a,**ka)

def re_filter(x):
    x = x.strip()
    varianti = x.split('==')
    if len(varianti) >1:
        x = '(' + '|'.join( v.strip() for v in varianti) + ')'
    x = re.sub( '\.\*сери[яий]', '.*сери[яий]', x )
    x = x.replace('  ', ' ' )
    x = x.replace('  ', ' ' )
    x = x.replace(' *', '\s*' )
    x = x.replace(' ', '\s+' )
    return x

def re_skriti( s):
    r = []
    for x in s.strip().split('\n'):
        if x.strip() and x.strip()[0] != '#':
            xx = re_filter( x)
            try:
                r.append( re.compile( xx, re.IGNORECASE ) )
            except:
                prn( '??', x , '-->', xx )
                raise
    return r

def finddel( tr, match):
    u = tr.find( match)
    tr.remove( u)

def text( i): return ' '.join( ''.join( i.itertext()).split())


class Iztochnik:
    ienc = None
    def __init__( me, skriti):
        me.skriti = skriti
        #for u in me.url_po_stranici(): prn( u)

    @property
    def baseurl( me):
        p = urlparse( me.url)
        return urlunparse( [ p.scheme, p.netloc ] + 4*[''] )

    itree= None
    def dai( me, argz =None, *urls):
        if not urls:
            a = argz
            #if not a: a = glob.glob( me.__class__.__name__+'*htm*')
            if not a:
                urls = list( me.url_po_stranici() )
            else:
                urls = a

        for u in urls:
            if u.startswith( 'http://'):
                with urlopen( u) as f:
                    itree = html5lib.parse( f, transport_encoding= f.info().get_content_charset(), namespaceHTMLElements=False)
                with open( me.__class__.__name__+'.cache.html', 'w') as f:
                    r = eltree.tostring( itree, encoding='unicode', method='html', short_empty_elements=False)      #cache2file
                    f.write( r)
            else:
                ienc = me.ienc
                with open( u, 'rb') as f:  #utf8 assumed
                    t = f.read()
                    if not ienc:
                        import chardet  #chardet.feedparser.org, python3-chardet, python-chardet
                        ienc = chardet.detect( t)[ 'encoding']   #.confidence
                    t = t.decode( ienc)
                itree = html5lib.parse( t, namespaceHTMLElements=False)

            me.parent_map = dict((c, p) for p in itree.iter() for c in p)

            if 'joinall':
                if me.itree:
                    me.do( itree2insert=itree )
                else:
                    me.itree = itree
                    me.do()
            else:
                me.itree = itree
                me.do()
                me.htmlout()

        me.htmlout()

    def htmlout( me):
        r = eltree.tostring( me.itree, encoding='unicode', method='html', short_empty_elements=False)      #cache2file
        r = r.replace( '</head>', f'''
<base href="{me.baseurl}">
<style type="text/css">
.skrijse {{ display: none !important; }}
.svijse  {{ font-size: 1pt; }}
body {{ background-color:#ddd0d0; }}
</style></head>
''')

        #<meta content="text/html; charset=utf8" http-equiv="Content-Type">
        r = r.replace( 'charset=windows-1251', 'charset=utf8')
        print( r)
        me.itree = None

    def remove( me, *items):
        for i in items:
            me.parent_map[i].remove(i)

    podrobno = False
    def grupa( me, r, txt):
        txt = ' '.join( txt.replace( '&nbsp','').split())
        pfx = '  '
        if me.tyrsi( txt):
            me.mahni( r)
            pfx = '* '
        if me.podrobno: prn( pfx, txt)

    def tyrsi( me, t):
        t = t.lower()
        for s in me.skriti:
            #if s in t.lower(): return True
            if s.search( t): return True

    iztrij = False
    def mahni( me, r):
        if me.iztrij: me.remove(r)
        elif 0*'skrijse': r.set('class', 'skrijse')
        else: me.svij( r)

    stranica_arg = None
    stranici = 2
    def url_po_stranici( me):
        u = me.url
        yield u
        if not (me.stranica_arg and me.stranici>1): return
        p = urlparse( u)
        q = parse_qs( p.query)
        for i in range( me.stranici-1):
            q[ me.stranica_arg] = [ str( 1+int( q[ me.stranica_arg][0] )) ]
            pq = urlencode( q, doseq=True)
            pp = p._replace( query= pq)
            u = urlunparse( pp)
            yield u





class zamunda( Iztochnik):
    url  = 'http://zamunda.net/browse.php?field=name&c35=1&c33=1&c20=1&c5=1&c19=1&c24=1&c28=1&page=0'
    stranica_arg = 'page'
    ienc = 'cp1251'

    headers = None
    def do( me, itree2insert =None):
        i = me.itree
        me.remove( *i.findall('.//script'))
        me.remove( *i.findall('.//iframe'))
        me.remove(
            i.find('.//table[@class="bottom navmain"]' ),
         #  i.find('.//div[@class="lefthb"]' ),
            #i.find('.//div[@class="iframeunique-unders "]' ), #XXX
         #  i.find('.//div[@class="unique-unders "]' ), #XXX
            #i.find('.//div[@class="unique-branding "]' ), #XXX
         #  i.find('.//div[@class="foot_links"]' ),
         #  i.find('.//form[@id="browse_ids"]' ),
            i.find('.//table[@class="test"]' ),
            )
        for x in [
            i.find('.//div[@id="toptorrents"]' ),
            i.find('.//table[@class="bottom responsivetable"]' ),
            ]:
            if x is not None: me.remove(x)

        table = i.find( './/table//tr/td[@class="td_clear td_newborder"]/../../..') #extra tbody
        for tr in table.findall('.//tr'):
            if not me.headers:
                me.headers = [ text(x).lower().strip() for x in tr ]#( './tr/td[@class="colhead"]') ]
                for td,kol in list(zip( tr, me.headers))[-3:]: tr.remove(td)
                continue
            ime = me.headers.index( 'име')  #=1

            td = list( tr.findall('td') )[ ime ]
            a = td.find('a')
            t = text(a)
            me.remove( *a)
            a.text = t
            me.grupa( tr, t )

            me.remove(
                td.find( './/div[@class="sharebox sharebox_details"]'),
                td.find( './/i'),
                )
            for td,kol in list(zip( tr, me.headers))[-3:]: tr.remove(td)

        table.set( 'border','0')
        body = i.find('.//body')
        me.remove( *body)
        body.append( table)

    def svij( me, tr):
        tr.set('class', 'svijse')
        for td,kol in zip( tr, me.headers):
            if kol=='име':
                a = td.find('./a')
                #me.remove( *a)
                a.text = '----'
                continue
            me.remove( *td)
            td.text = None

    ex = '''
<div id="result">
<table class=bottom width='90%' border=0 cellspacing=0 cellpadding=0>
 <tr><td class=embedded>
  <div id="div1">
   <table align=center width=700>
    <tr height=23>
    <td class=colheadd align=center width=35>&nbsp;Тип&nbsp;</td>
    <td ...
    </tr>

    <tr>
     <td align=center bgcolor=#FFFFFF width=35>
        <img src=http://img.zamunda.net/pic/cat_movies_xvid.gif width=45></td>
     <td align=left bgcolor=#FFFFFF>&nbsp;
        <a href=details.php?id=373108&hit=1 alt="Now You See Me / Зрителна измама (2013)" title="Now You See Me / Зрителна измама (2013)">
         <b>Now You See Me / Зрителна измама (2013)</b>
        </a> &nbsp;
        <img src=http://img.zamunda.net/pic/flag_bgsub.gif border=0 alt='с български субтитри'>&nbsp
        <a href="video.php?view=youtube&torrent=...&video=..." onclick="window.open('video.php?view=youtube&torrent=...&video=...', 'Video', 'HEIGHT=650,resizable=yes,scrollbars=yes,WIDTH=600');return false;">
         <img src=http://img.zamunda.net/pic/youtube.gif style='border: 1px #282828 solid;'>
        </a>
       &nbsp</td>
     <td align=center bgcolor=#FFFFFF>
        <img src="http://img.zamunda.net/pic/5.gif" border="0" alt='Рейтинг: 5 / 5' title='Рейтинг: 5 / 5' />
     </td>
     <td align=right bgcolor=#FFFFFF>1.65 GB&nbsp;</td>
     <td align=center bgcolor=#FFFFFF>5939&nbsp;</td>
     <td align=center bgcolor=#FFFFFF>36</td>
     <td align=center bgcolor=#FFFFFF><a href=details.php?id=373108&hit=1&tocomm=1>33</a></td>

    <tr>
     ...

    '''

class kinozal( Iztochnik):
    url= 'http://kinozal.tv/browse.php?c=1003&page=0'
    stranica_arg = 'page'
    ienc = 'cp1251'

    def do( me, itree2insert =None):
        if itree2insert: i = itree2insert
        else:
            i = me.itree
            me.remove( *i.findall('.//script'))
            mainmenu = i.find( './/div[@id="main"]/div[@class="menu"]')
            me.remove( *[ x for n,x in enumerate( mainmenu) if n])
            me.remove(
                i.find( './/div[@class="pad0x0x5x0 center"]'),
                i.find( './/div[@id="footer"]'),
                i.find( './/div[@id="header"]' ),
                i.find( './/div[@class="paginator"]' ),
            )
            #me.remove( i.find( './/div[@id="header"]//table' ))
            for match in [ './/ul[@class="men"]',]: # './/div[@id="header"]/div[@class="menu"]//ul' ]:
                ul = i.find( match)
                ul.set( 'style', '''
                    list-style: none ;
                    list-style-type: none ;
                    margin: 0;
                    padding: 0;
                    ''')
                for li in ul.findall('./li'): li.set( 'style', 'display: inline')
            i.find( './/input[@class="w98p"]' ).set('style', 'width: 100%')

        #table = i.find( './/table/..[@class="bx2_0"]/table')
        table = i.find( './/div[@class="content"]//div[@class="bx2_0"]/table')
        #table.set( 'cellspacing', '5')
        table.set( 'cellpadding', '3')

        headers = table.find( './/tr[@class="mn"]')
        def delkoloni( tr ):
            dels = [ td for n,td in enumerate( tr.findall( './td')) if n in [2,4,5,7]]
            me.remove( *dels)
        delkoloni( headers)

        table2insert = itree2insert and me.itree.find( './/div[@class="content"]//div[@class="bx2_0"]/table')
        for tr in table.findall('.//tr/td[@class="nam"]/..'):
            td = tr.find('./td[@class="nam"]')
            text = ''.join( td.itertext())
            me.grupa( tr, text)
            delkoloni( tr)
            td = tr.find('./td[@class="bt"]')
            img = td.find( './img')
            if img is not None:
                td.remove( img )
                src = img.get( 'src')
                src = src.split('/')[-1].split('.')[0]
                td.text = me.cats.get( src, src)[0] #+' -'*2
            for td in tr.findall('./td[@class="s"]'):
                td.text = re.sub( '\.20\d\d ', '.. ', td.text or '')

            if table2insert:
                table2insert.append( tr)

    cats = { 20: 'аниме', 22: 'руско', 21: 'друго' }
    cats.update( (str(k),v) for k,v in list( cats.items()))

    def svij( me, tr):
        #tr.set('height', '5')
        tr.set('class', 'svijse')
        for td in tr:
            if td.get('class')=='nam':
                td.find('./a').text = '----'
                continue
            me.remove( *td)
            td.text = None

    ex = '''
    <div class="bx2_0"><table class="t_peer w100p" cellspacing=0 cellpadding=0><tr>....</tr>

    <tr class=first>
     <td class="bt">
        <img src="/pic/cat/21.gif" class="p90x32 pointer" onclick="cat(21);" alt=""></td>
     <td class="nam">
      <a href="/details.php?id=1121620" class="r0">руско-заглавие / англ-заглавие / година...</a>
     <td class='s'>
     ...
     <td class='sl'><a href='/userdetails.php?id=17150030' class=u5>pogranets</a><i class="i1 s4"></i></td></tr>

    '''
    #cols': ['', '', 'Комм.', 'Размер', 'Сидов', 'Пиров', 'Залит', 'Раздает', _??],



skriti = re_skriti( '''
Haikyuu
Лунтик
Терраформирование == Terra Formars

Хвост Феи == Gekijouban Fairy Tail

S\d{1,2}E\d+
''')


if __name__ == '__main__':

    srcs = dict( (d.__name__, d) for d in Iztochnik.__subclasses__())

    from svd_util import optz
    optz.text( 'ienc',          help= 'входно кодиране; подразбиране - автоматично' )
    optz.text( 'oenc',          help= 'изходно кодиране', )
    optz.int(  'stranici',      help= 'колко страници; подразбиране - според източника', default=0 )
    optz.list( 'iztochnik',
        type= 'choice', choices= sorted( srcs),
        help= 'източник (%s), може няколко пъти; подразбиране - всички' % ' '.join( sorted( srcs)) )
    optz.text( 'skriti',    help= 'файл с филтрите')
    optz.bool( 'podrobno',  help= 'показва извлечените имена')
    optz.bool( 'trij',      help= 'изтрива филтрираните елементи вместо само да ги скрива/свива')
    optz,argz = optz.get()

    if optz.ienc=='auto': optz.ienc=None

    if optz.oenc:
        from svd_util.eutf import fix_std_encoding, filew
        fix_std_encoding( ENC= optz.oenc)
    def fopen( fn):
        if optz.oenc: f = filew( optz.oenc, fn)
        else: f = open( fn, 'w')
        return f

    Iztochnik.iztrij = optz.trij
    if optz.skriti: skriti = re_skriti( open( optz.skriti).read())
    if optz.stranici: Iztochnik.stranici = optz.stranici
    if optz.podrobno: Iztochnik.podrobno = optz.podrobno
    for i in optz.iztochnik:# or srcs.keys():
        prn( i)
        izt = srcs[i]( skriti)
        #if argz: url = argz[0]

        #try:
        izt.dai( argz=argz)# url, optz)
        #print( wdta)
        #except: traceback.print_exc( file= sys.stderr)

'''
 - чете (първа) страница от източника - или вх.файл
 - за всеки елемент                         !! трябва описание кое е елемент и какво съдържа, по източник
    - ако влиза в черния списък, едно от:   !! трябва черен списък
        - изтрива го
        - слага му клас=скрийсе
 - извежда страницата (като файл)

 -- четене няколко страници (?? файлове)
    - за всяка страница
        - горното
        - извеждане, едно от:
            - по отделно
            - като една обща    !! трябва описание как се сливат няколко страници в една, по източник

 -- помнене докъде е четено, и извеждане само на по-новите елементи

 -- хттп-посредник
    - сеща се откъде/как да чете по адреса, или по параметър, като
        - чете по една страница     !!трябва описание къде да се подменят връзките към следващи/предходни
        - или чете няколко (и после ги слива)
    - за всеки елемент
        - горното
        - добавя превключвател, който поисква пъхане на елемента в черния списък
    - трябва слушател за превключвателя
    - извеждане:
        - според четенето: по една или няколкото слети

'''
# vim:ts=4:sw=4:expandtab

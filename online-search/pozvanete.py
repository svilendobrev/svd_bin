#!/usr/bin/env python
# -*- coding: utf-8 -*-
#$Id: pozvanete.py,v 1.7 2008-01-24 14:41:58 sdobrev Exp $

import sys
ff = sys.argv[1:]

naemexcl = ''
kyshtaexcl = ''

naem = 'ofis' in ff or 'naem' in ff or 'naemi' in ff
if 'ofis' in ff: ff.remove('ofis')
if naem:
    naemexcl = '''
ПРОДАВАМ
ПАРЦЕЛ
.БЯЛА
'''

if 'kyshta' in ff:
    ff.remove('kyshta')
    kyshtaexcl = '''
СТАЕН
АПАРТАМЕНТ
'''

excludes = ('''
НОЩУВК
МАГАЗИН
СУТЕРЕН
СКЛАД
ПАВИЛИОН
РЕСТОРАНТ
ПОЛОВИН
БИЛБОРД
ФРИЗЬОРСК
ЗЪБОЛЕКАРС
ЗАВЕДЕНИЕ
АПТЕКА
КАФЕ
БИСТРО
БУНГАЛ
ТЪРС
ХОТЕЛ
ПОМЕЩЕНИЕ
ЗЕМЕДЕЛСК
ГАРСОНИЕР
БОКСОНИЕР
САМОСТОЯТЕЛНИ
БЕНЗИНОСТАН
ПРЕХОДНИ
'''
+ kyshtaexcl + naemexcl
).split()
#СТАЯ

lowerc = ''.join( chr(a) for a in range(128) )
lowerc+= 2*''.join( chr(a) for a in range(160,192) )
lowerc+= 2*''.join( chr(a) for a in range(224,256) )
excludes += [ a.translate( lowerc) for a in excludes]

excludecols = [ 1, 2, 5]

datagrad_col = 1


class date:
    today = None

def parse( f, initial =False):
    ncol = -1
    on = offr = offitem = 0
    for line in (isinstance( f, str) and file(f) or f):
        if 'results --' in line: on=1
        if '-- Pager' in line: on=0
        if not on or not line.strip():
            continue

        if '<!--  Start -->' in line: offr=1
        if '<!--  End -->' in line:
            offr=0
            continue
        if offr: continue

        if '<tr' in line: ncol = 0
        if '<th' in line: continue
        if '<col ' in line: continue

        if '</tr>' in line:
            offitem=0
        else:
            for k in excludes:
                if k in line:
                    offitem = 1
                    break
            if offitem: continue

            if '<td' in line: ncol+= 1

            if not date.today and ncol == datagrad_col:
                l = line.split(',')[0]
                #l = l.split('</td>')[0]
                l = l.split('<td>')[1].strip()
                l = l.replace(' ','-')
                date.today = l + '.html'
                print >>sys.stderr, date.today

        if not initial:
            if ncol in excludecols:
                if '<tr' in line: line = '<tr><td>'
                else:
                    #print 'ignore', line
                    continue

        if 'изгод' in line or 'спеш' in line: line = '<b> '+line


        for c in [ '<br>', '</td>', '</tr>', '<strong>', '</strong>', 'Снимка',
                    ' class="odd"', ' class="even"', ' class="bookmark"',
                '\t']:
            line = line.replace( c,'')
        line = line.strip()
        if not line: continue
        if not line.startswith( '<td>'): line='\n'+line
        else: line=' '+line
        yield line

if 'http' in ff:
    if 'naem' in ff or 'naemi' in ff:
        http = 'http://pozvanete.bg/ads_results.php?town=5&day=2&rubrics=2200&sub_rubrics=0&property_location=0&property_type=0&perpage=1000'
        fn = 'naem'
    else:
        http = 'http://pozvanete.bg/ads_results.php?town=5&day=2&rubrics=1800&sub_rubrics=0&property_location=0&property_type=0&perpage=1000'
        fn = 'kyshta'
    import urllib2
    f = urllib2.urlopen( http)
    s = ''.join( parse( f, initial=True) )
    fn += '-' + (date.today or 'tmpp')
    w = file( fn, 'w')
    w.write( s)
    w.close()
    ff = [ fn ]

for f in ff:
    for l in parse(f):
        print l,#.rstrip()

# vim:ts=4:sw=4:expandtab

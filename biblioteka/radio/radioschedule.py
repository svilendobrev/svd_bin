#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
1. cron.daily : radiorec-scheduler: прочита разписанието (http://programs..)
   и за всяко предаване прави ред в /etc/cron.d/radiorec
2. /etc/cron.d/radiorec: съдържа редове пускащи radiorec в съответното време
'''
import pprint
from time import sleep
from svd_util.struct import DictAttr, attr2item
from svd_util.osextra import makedirs#, save_if_diff
da = DictAttr

bnr_kanali = da(
    hristobotev = da(
        weekly  = None ,#'http://bnr.bg/hristobotev/page/sedmichna-programa', #XXX TODO
        #weekly  = 'http://bnr.bg/sites/hristobotev/Pages/ProgramScheme.aspx',
        #daily0  = 'http://bnr.bg/sites/hristobotev/Daily/Pages/{yymmdd}.aspx',
        #daily1  = 'http://bnr.bg/sites/hristobotev/Daily/Pages/{yymmdd}_1.aspx',
        #daily2  = 'http://bnr.bg/sites/hristobotev/Daily/Pages/{yymmdd}_izbrano.aspx',
        daily   = 'http://bnr.bg/hristobotev/', #sites/hristobotev
        stream  = 'http://stream.bnr.bg:8003/botev.mp3',
            #'http://streaming.bnr.bg/HristoBotev',
        abbr = 'hb',
    ),
    horizont = da(
        weekly  = None,
        #weekly  = 'http://bnr.bg/sites/horizont/Pages/ProgramScheme.aspx',
        #daily   = 'http://bnr.bg/sites/horizont/Daily/Pages/{yymmdd}.aspx',
        daily   = 'http://bnr.bg/sites/horizont/',
        stream  = 'http://streaming.bnr.bg/Horizont',
        abbr = 'hz',
    ),
    varna = da(
        weekly  = 'http://radiovarna.bnr.bg/Pages/ProgramScheme.aspx',
        stream  = 'http://212.56.1.60:8000/live',
        abbr = 'vn',
        #http://radiovarna.bnr.bg/Shows/Cultural/rtheatre/Pages/radiotheatre_2011_10_05.aspx
    ),
    sofia = da(
        weekly  = 'http://radiosofia.bnr.bg/Pages/ProgramScheme.aspx',
            #http://www.radiosofia.bnr.bg/RadioSofia/scheme.htm',
        stream  = 'http://streaming.bnr.bg/RadioSofia',
        abbr = 'sf',
        #http://radiovarna.bnr.bg/Shows/Cultural/rtheatre/Pages/radiotheatre_2011_10_05.aspx
    ),


)

for k in bnr_kanali:
    bnr_kanali[ k].name = k
for k in list( bnr_kanali.values()):
    bnr_kanali[ k.abbr] = k

kanal_default = bnr_kanali.hristobotev

from svd_util.txt import strip, slim

#Радиотеатър
#Златния фонд
#Златните гласове
#хлапета
#документално студио
INTITLES = strip('''
Радиотеат
Радотеат
театър
театр
за деца
Романи за деца
Златни
колекция
приказк
документа
Хумор и сатира
комика
смешните
''').lower().split('\n')

NOTINTITLES = strip( '''
История на изкуството
Музикални пътешествия
''').lower().split('\n')


def title_match( title):
    if not title: return False
    title = title.lower().replace('  ',' ')
    for f in INTITLES:
        if f in title:
            for n in NOTINTITLES:
                if n in title: break
            else: return True

def time4str( t): #hh:mm or hh.mm ...
    x = re.split( '(\d+)', t)
    hm = x[1],(len(x)>3 and x[3] or 0)
    return tuple( int(a) for a in hm)


import sys
from svd_util.html_visitor import visit
from svd_util.py3 import dictOrder
import re
import datetime

class bnr_weekly:
    syntax = ''' ..
  <div id="scroller-stripe">
    <div id=IGNORE class="week-day">
      <h2> Петък
        <span> (05 Август 2011)
        </span>
      </h2>
      <dl>
        <dt id=IGNORE">0:00 </dt>
        <dd id=IGNORE">Новини  </dd>
        ...
      </dl>
    </div>
    ... '''

    days = []
    aday = da()
    def newday():               bnr_weekly.days.append( da( bnr_weekly.aday, list= []) )
    def save_lastday_name( t):  bnr_weekly.days[-1].dayname = t
    def save_lastday_date( t):  bnr_weekly.days[-1].daydate = t
    def newitem():              bnr_weekly.days[-1].list.append( da() )
    def save_lastitem_time( t): bnr_weekly.days[-1].list[-1].time = t
    def save_lastitem_title(t): bnr_weekly.days[-1].list[-1].title = t

    grammar_stack= [
        da( tag= 'div', _id= 'scroller-stripe', subitems=[
            da( tag= 'div', _class= 'week-day', run= newday, subitems= [
                da( tag= 'h2', data= save_lastday_name, subitems= [
                    da( tag= 'span', data= save_lastday_date ),
                ]),
                da( tag= 'dl', subitems= [
                    da( tag= 'dt', run= newitem, data= save_lastitem_time ),
                    da( tag= 'dd', data= save_lastitem_title ),
                ]),
            ]),
        ])
    ]
    syntax = '''
    <div class="news_title">
        <h3>Седмична програма</h3>
    </div>
    <div class="news_content">
      <p><br /></p>
      <module id="m243">
        <div class="module span12 module_schedule ">
          <h2>02 октомври 2016, неделя</h2>
          <div>
            <div class="time_box">00:15</div>
                        Концерт
          </div>
          <div>
            <div class="time_box">03:00</div>
                        <a href="/hristobotev/evroklasik/broadcast">Еврокласик ноктюрно</a>
          </div>
          ...
          <h2>03 октомври 2016, понеделник</h2>
          ...
    '''
    grammar_stack= [
        da( tag= 'div', _class= 'module', subitems=[
            da( tag= 'h2', run= newday, data= save_lastday_date, ),
            da( tag= 'div', run= newitem, data= save_lastitem_time, subitems=[
                da( tag= 'div', _class='time_box', data= save_lastitem_time ),
            ]),
        ]),
    ]
    @classmethod
    def get( me, kanal, o):
        url = kanal.weekly
        if not url: return
        print( '#...', url, kanal.stream, file= sys.stderr)
        me.aday.update( stream= kanal.stream, channel= kanal.name)
        m = len( me.days)
        indata = visit( url, me.grammar_stack,
                    data2text = slim,
                    ienc= o.ienc, html_notfixed =o.html_notfixed, html_strict =o.html_strict )
        print( '#... days:', len( me.days) - m, file= sys.stderr)
        return indata

    re_daydate = re.compile( '\( *(?P<day>\d+) (?P<month>\w+) (?P<year>\d+)')
    months = 'Януари Февруари Март Април Май Юни Юли Август Септември Октомври Ноември Декември'.lower().split()
    weekdays = 'Понеделник Вторник Сряда Четвъртък Петък Събота Неделя'.lower().split()

    @classmethod
    def filter( me, today, ndays =1, nofilter =False):
        todays = [ today + datetime.timedelta( days= dayofs )
                    for dayofs in range( ndays) ]

        items = dictOrder()
        for d in me.days:
            if 'daydate' not in d:  #weekday samo
                wd = me.weekdays.index( d.dayname.lower() )
                twd = today.weekday()
                date = today + datetime.timedelta( days=wd-twd)
            else:
                mdate = me.re_daydate.search( d.daydate)
                date = datetime.date(
                    day   = int( mdate.group('day')),
                    month = 1+ me.months.index( mdate.group('month').lower() ),
                    year  = int( mdate.group('year')),
                    )

            dayon = True
            if not nofilter:
                dayon = date in todays

            for i in d.list:
                #{'title': 'Новини', 'time': '8:00'}
                i.time = time4str( i.time)
                if items:
                    last = list( items.values()) [-1]
                    if not last.get('endtime'): last.endtime = i.time
                if not dayon: continue
                if not nofilter:
                    if not title_match( i.title): continue
                key = d.channel, date, i.time
                items[ key] = da( i, today= date, stream= d.stream, channel= d.channel )

        return items

from svd_util import html_visitor
#html_visitor.dbg=1
import urllib
import traceback

class bnr_weekly_sofia( bnr_weekly):
    '''
        <tr valign="top">
            <td width="5"><img src="/bnr/img/spacer.gif" width="5" height="1"></td>
            <td width="60" class="programTXT">21:00</td>
            <td class="programTXT">Радиотеатър</td>
            <td width="5"><img src="/bnr/img/spacer.gif" width="5" height="1"></td>
        </tr>
    '''
    def newday( me, tag, attrs):
        #if 'alt' not in attrs: return
        #print( 333333, tag,attrs)
        bnr_weekly.days.append( da( bnr_weekly.aday, list= []) )
        bnr_weekly.days[-1].dayname = attrs['alt']

    def newitem_time( t):
        if bnr_weekly.days[-1].list:
            bnr_weekly.days[-1].list[-1].time += '-'+t
        bnr_weekly.newitem()
        bnr_weekly.save_lastitem_time( t)

    grammar_stack= [
        da( tag= 'table', _class= 'colorWhite', subitems=[
            da( tag= 'img', _alt=True, run3= newday),
            da( tag='td', _class= 'programTXT', _width=True,
                data= newitem_time),
            da( tag='td', _class= 'programTXT', _width=False,
                data= bnr_weekly.save_lastitem_title),
        ])
    ]
    bnr_weekly.grammar_stack += grammar_stack

class zbnr_daily:
    syntax = ''' ..
  <div class="accent">
    <div class="accent-info">
        <div id="ctl00_PlaceHolderMain_EditModePanel2">
        Понеделник, 08 август 2011  00:00
        </div>
    </div>
    ..
    <div>
      <div id="ctl00_PlaceHolderMain_RichHtmlField1__ControlWrapper_RichHtmlField" style="display:inline">
        от 0.15 до 2.00 часа
        <br><strong>title..
        </strong><br>description..
        <br><br>

        от 2.00 до 3.00 часа
        <br><strong>title..
        <br></strong>description..
        <br><br>
      ...
    </div>
    ... '''

    today_items = []
    today_whole = []
    anitem = da()
    def save_day_description( t):   bnr_daily.today_whole.append( t)
    def newitem():                  bnr_daily.today_items.append( da( bnr_daily.anitem))
    def save_lastitem_title( t):    bnr_daily.today_items[-1].title = t

    grammar_stack= [
        da( tag= 'div', _class= 'accent', subitems=[
            da( tag= 'div', _id= 'ctl00_PlaceHolderMain_RichHtmlField1__ControlWrapper_RichHtmlField',
                    data= save_day_description, zzsubitems=[
                da( tag='br', run= newitem,
                    data= save_lastitem_title,
                ),
                da( tag='p', run= newitem,
                    data= save_lastitem_title,
                ),
            ]),
        ]),
    ]
    re_titles = re.compile( '''
        \s*
        <br>
        \s*
        (?P<title>.*?)
        \s*
        <br>
        \s*
        (?P<text>.*)
        ''', re.X|re.DOTALL) #(<br>)?
    @classmethod
    def get( me, kanal, o, today):
        for url in [ kanal.get('daily0'), kanal.get('daily1'), kanal.get('daily2'), ]:
            if not url: continue
            yymmdd = today.strftime( '%y%m%d' )
            url = url.format( **locals() )
            print( '#...', url, file= sys.stderr)
            me.anitem.update( today= today, stream= kanal.stream, channel= kanal.name)
            m = len( me.today_items)
            try:
                indata = visit( url, me.grammar_stack,
                        data2text = slim,
                        ienc= o.ienc, html_notfixed =o.html_notfixed, html_strict =o.html_strict,
                        BR_as_data= '<br>' )
            except urllib.error.HTTPError as e:
                print( '  ?daily', kanal.abbr, url, e, file= sys.stderr)
                continue

            whole = me.today_whole.pop()
            whole = whole .replace( '\u2013','-'     #-
                    )

            tds = re.split( '([оo][тt] *\d+([.:]\d+)? *-? *([дd][оo]|-) *\d+([.:]\d+)? *часа)', whole, flags= re.IGNORECASE )
            #print( '#...', len(tds), len(me.today_items) -m, file= sys.stderr)
            #print( '##...', tds, file= sys.stderr)
            allitems = [ (tds[ i], tds[i+3+1])
                        for i in range( 1,len( tds),4+1) ]

            for times,data in allitems:
                times = re.split( '(\d+(.\d+)?)', times)
                m = me.re_titles.search( data)
                #print( 3333333, times, data, m.groups())
                title= m and m.group( 'title') or ''
                text = m and m.group( 'text') or ''
                me.today_items.append( da( bnr_daily.anitem,
                    time    = time4str( times[1] ),
                    endtime = time4str( times[4] ),
                    title   = slim( title),
                    text    = slim( text.replace('<br>','') ),
                ))
            return indata

    @classmethod
    def filter( me, nofilter =False):
        items = dictOrder()
        for i in me.today_items:
            if not nofilter:
                if not title_match( i.title): continue
            key = i.channel, i.today, i.time
            items[ key ] = da( i, stream= i.stream, channel= i.channel )    #today= today,
        return items

class bnr_daily:
    syntax1 = '''
    <div class="row-fluid module span12 module_category module_category_titles" id="module_11_1">
        <div class="row-fluid module_main_header">
            <div class="title"> byrabyra
        <div class="row-fluid module_container">
            <div class="title">
                <a href="/hristobotev/post/100284716">Избрано от програмата на 14 януари</a>
    '''
    syntax2 = '''
    <div class="news_title">
        <div class="news_content clearfix">
            <span itemprop="articleBody">
                от 0.15 до 3.00 часа<br /><b>title...</b><br />• description1...;<br />• description2....<br /><br />от 5.00 до 5.30 часа<br /><b>title..</b><br />description..<br /><br />
    '''
    today_items = []
    today_whole = []
    anitem = da()
    def newitem3( walker, tag, attrs):
        a = da( bnr_daily.anitem)
        a.url = attrs.get('href')
        bnr_daily.today_whole.append( a)
    def newitem():                  bnr_daily.today_whole.append( da( bnr_daily.anitem))
    def save_lastitem_title( t):    bnr_daily.today_whole[-1].title = t

    grammar_stack1= [
        #da( tag= 'div', _id= 'module_12_1', subitems=[
            da( tag= 'div', _class= 'row-fluid module_container', subitems=[
                da( tag= 'div', _class= 'title', subitems=[
                    da( tag='a', run3= newitem3,
                        data= save_lastitem_title,
                    ),
                ]),
            ]),
        #]),
    ]
    grammar_stack2= [
        #da( tag= 'div', _class='news_content', subitems=[
            da( tag= 'span', _itemprop= 'articleBody',
                    run= newitem,
                        data= save_lastitem_title,
            ),
        #]),
    ]
    re_titles = re.compile( '''
        \s*
        <br>
        \s*
        (?P<title>.*?)
        \s*
        <br>
        \s*
        (?P<text>.*)
        ''', re.X|re.DOTALL) #(<br>)?
    @classmethod
    def get( me, kanal, o, today):
        #me.today_whole = []
        indata = dictOrder()
        for url in [ kanal.get('daily') ]:
            if not url: continue
            print( '#...', url, file= sys.stderr)
            me.anitem.update( today= today, stream= kanal.stream, channel= kanal.name)
            try:
                indata[''] = visit( url, me.grammar_stack1,
                        #return_also_headers=True,
                        data2text = slim,
                        ienc= o.ienc, html_notfixed =o.html_notfixed, html_strict =o.html_strict,
                        BR_as_data= '<br>'
                        )
            except urllib.error.HTTPError as e:
                print( '  ?daily1', kanal.abbr, url, e, file= sys.stderr)
                continue
            #print( 4444444444444444444, me.today_whole)

            #ден след
            #днес
            #ден преди
            ndays=2
            for dnes in [ today + datetime.timedelta( days= dayofs )
                    for dayofs in range( ndays)
                    ]:
                url2 = None
                for u in me.today_whole:
                    if (u.channel == me.anitem.channel
                        and
                        bnr_weekly.months[ dnes.month-1 ] in u.title.lower()
                        and
                        str( dnes.day) in u.title.split()
                        and
                        u.get('url')
                        ):
                            url2 = u.url
                            break
                if not url2: continue
                me.anitem.update( today= dnes)

                if '://' in url:    #http
                    url2 = urllib.parse.urljoin( url, url2)

                print( '#....', url2, file= sys.stderr)
                try:
                    indata[ url2] = visit( url2, me.grammar_stack2,
                            data2text = slim,
                            ienc= o.ienc, html_notfixed =o.html_notfixed, html_strict =o.html_strict,
                            BR_as_data= '<br>'
                            )
                except urllib.error.HTTPError as e:
                    print( '  ?daily2', kanal.abbr, url2, e, file= sys.stderr)
                    continue
                #print( 5555555554444444444, me.today_items)

                whole = me.today_whole[-1].title
                whole = whole .replace( '\u2013','-'     #-
                        )

                tds = re.split( '([оo][тt] *\d+([.:]\d+)? *-? *([дd][оo]|-) *\d+([.:]\d+)? *часа)', whole, flags= re.IGNORECASE )
                #print( '#...', len(tds), len(me.today_items) -m, file= sys.stderr)
                #print( '##...', tds, file= sys.stderr)
                allitems = [ (tds[ i], tds[i+3+1])
                            for i in range( 1,len( tds),4+1) ]

                #print( 22222222, allitems)
                for times,data in allitems:
                    times = re.split( '(\d+(.\d+)?)', times)
                    m = me.re_titles.search( data)
                    #print( 3333333, times, data, m.groups())
                    title= m and m.group( 'title') or ''
                    text = m and m.group( 'text') or ''
                    me.today_items.append( da( bnr_daily.anitem,
                        time    = time4str( times[1] ),
                        endtime = time4str( times[4] ),
                        title   = slim( title),
                        text    = slim( text.replace('<br>','') ),
                    ))
                #print( 3333333, times, data, m.groups())
        return indata

    @classmethod
    def filter( me, today, ndays =1, nofilter =False):
        todays = [ today + datetime.timedelta( days= dayofs )
                    for dayofs in range( ndays) ]

        items = dictOrder()
        for i in me.today_items:
            if not nofilter:
                if not title_match( i.title): continue
                if i.today not in todays: continue
            key = i.channel, i.today, i.time
            items[ key ] = da( i, stream= i.stream, channel= i.channel )    #today= today,
        return items


import os, glob
import rec2dir
from svd_util.yamls import usability
l2c = rec2dir.lat2cyr.zvuchene.lat2cyr
import difflib

def junk( x): return not x.isalpha()
def tyrsi_podobni( ime, nalichni, min_ratio =0.7):
    podobni = [ (not s.set_seq1( ime.lower()) and 1-s._ratio(), s._item )
        for s in nalichni
        ]
    podobni.sort()
    min_ratio1 = 1-min_ratio
    return [ (r,i) for r,i in podobni if r <= min_ratio1 ]

def nalichni_imena( o, quick =0):
    if not o.nalichni_opisi: return
    nalichni_imena = [] #s(ime).(ime,dir,file)
    def dobavi( x):
        s = difflib.SequenceMatcher( junk )
        if not quick:  ratio = s.ratio
        elif quick==2: ratio = s.real_quick_ratio
        else:          ratio = s.quick_ratio
        s._ratio = ratio
        s._item = x
        s.set_seq2( x[0].lower() )
        nalichni_imena.append( s)

    def kym_imeto( opis):
        avtor = opis.get( 'автор')
        if avtor:
            if isinstance( avtor, (list,tuple)): avtor = ' '.join( avtor)
            avtor = avtor.strip()
        return avtor and ' : '+avtor or ''
    for fn in glob.glob( o.nalichni_opisi):
        try:
            with open( fn) as f:
                opis = dict( usability.load( f ) )
                ime = opis.get( 'име')
                ime = ime and str(ime).strip()
                if not ime or not ime.strip('?'):
                    ime = l2c( os.path.basename( fn))
                avtor = kym_imeto( opis)
                ime += avtor
                dobavi( (ime, fn))
                parcheta = opis.get( 'парчета')
                if not parcheta: continue
                for fnp,p in parcheta.items():
                    if isinstance( p, str):
                        ime = p
                        avtor1 = avtor
                    else:
                        ime = p.get( 'име')
                        avtor1 = kym_imeto( p) or avtor
                    ime = ime and str(ime).strip()
                    ime = ime or l2c( fnp)
                    ime += avtor1
                    dobavi( (ime, fn, fnp) )
        except IOError: pass
        except Exception as e:
            print( fn, ':', str(e), file= sys.stderr)
            raise
    print( '#налични описи:', len( nalichni_imena), file= sys.stderr)
    def tyrsach( ime):
        return tyrsi_podobni( ime, nalichni_imena,
                min_ratio= 0.7 )
    o.tyrsach = tyrsach
    return tyrsach

def cron( items, o ):
    '''
cron/crontab plain:  # m h dom mon dow  command
cron.d/crontab direct: # m h dom mon dow (user) command
'''
    tyrsach = nalichni_imena( o)

    for x in sorted( items, key= lambda a: (a.today,a.time) ):
        h,m = x.time

        #print( '#', x.time, x.title)
        endtime = x.get( 'endtime')
        if endtime:
            eh,em = endtime
            eoffs = eh*60+ em
            soffs = h*60+ m
            if eoffs < soffs: eoffs += 24*60
            sizemins = eoffs - soffs
        else: sizemins = ''
        t = datetime.datetime( x.today.year, x.today.month, x.today.day, h,m)

        dni = x.get('dni')
        if dni: #a,b,c-f
            r = set()
            for d in dni.split(','):
                dd = d.split('-')
                if len(dd)==2:
                    r.update( range( int(dd[0]), int(dd[1])+1) )
                else: r.add( int(d))
            if t.weekday()+1 not in r:
                continue    #skip

        channel = x.channel
        if not channel:
            if x.stream:
                channel = x.stream.split('://')[-1].replace('/','_')
        if channel in bnr_kanali:
            channel = bnr_kanali[ channel ].abbr


        fname = str( channel)
        fname_kanal = fname
        dati = '{t.year:04d}-{t.month:02d}{t.day:02d}-{t.hour:02d}{t.minute:02d}'.format( **locals())
        if not o.cron_fname_notime: fname += dati
        fname_kanal_vreme = fname + dati

        if x.get('title'): fname += '+'+x.title
        if x.get('text'):
            DOT = '\u2022' #'•'
            tx = x.text.replace('Предаването', 'Пр.'
                      ).replace('посветено', 'посв.'
                      ).replace('годишнина', 'год.'
                      ).replace('години', 'г.'
                      ).replace( DOT,'-'
                      )
            fname += '+'+tx
            x.text = x.text.replace( DOT, '\n--')

        def sykr( x):
            x = re.sub( rec2dir.requo, '', x.strip()
                    ).replace( '\u2013','-'     #-
                    ).replace( '\u0406','I'     #І
                    #).replace( '\u0425','X' cyrХ latX ?
                    ).replace( 'x','х'
                    ).replace('  ',' '
                    ).replace(' -','-'
                    ).replace('- ','-'
                    ##).replace('  ',' '
                    ).replace(' ','_'
                    ).replace('__','_'
                    #).replace('„',''
                    #).replace('”',''
                    ).replace('Документално_студио','Док.ст.'
                    ).replace('Радиоколекция',      'Ркц'
                    ).replace('Радиотеатър',        'Рт'
                    ).replace('радиотеатър',        'Рт'
                    ).replace('Радотеатър',         'Рт'
                    ).replace('Време_за_приказка',  'ВзаП'
                    ).replace('Ваканционна_програма',   'Вкц'
                    ).replace('Избрано_от_', ''
                    ).replace('фонда_на_редакция',''
                    ).replace('фонда_на_',   ''
                    ).replace('_на_БНР',''
                    ).replace('Запазена_марка',''
                    ).replace('Запазна_марка',''
                    ).replace('Семейно_радио', '' #Сем
                    ).replace('Голямата_къща_на_смешните_хора', 'ГКСХ'
                    ).replace('Салон_за_класифицирана_словесност', 'Салон_словесност'
                    ).replace('Съвременна',     'Съвр.'
                    ).replace('Драматургични',  'драм.'
                    ).replace('драматургия',    'драм.'
                    ).replace('Незабравими_български_спектакли_във_фонда', 'бълг.др.'
                    ).replace('българска',  'бълг.'
                    ).replace('български',  'бълг.'
                    )
            x = re.sub( rec2dir.rlatcyr( '([Дд])окументал(ен|н(а|о|и))'), r'\1ок.', x)
            x = re.sub( rec2dir.rezlf, rec2dir.zlf, x)
            x = re.sub( rec2dir.reakm, rec2dir.akomika, x)
            x = re.sub( rec2dir.rehs, rec2dir.hs, x)
            x = x.strip( rec2dir.rend+':')
            return x

        dosave = 10#True
        danni = DictAttr(
            rubrika = x.get('title') or '',
            data = '{t.year:04d}{t.month:02d}{t.day:02d}'.format( **locals()),
            opisanie = x.get('text') or '',
        )
        danni.opisanie = '\n'.join( d.strip() for d in danni.opisanie.split('\n') if d.strip())
        danni.rubrika_kysa = sykr( danni.rubrika)
        z = danni.razglobeno = rec2dir.razglobi_imena(
            imena= danni.opisanie.replace(' ','_'),
            rubrika= danni.rubrika or x.get('ime') or '',
            #rubrika_kysa = danni.rubrika_kysa,
            data = danni.data,
            dirname = None
        )
        z = attr2item( z, default='')

        op = danni.opisanie.lower()

        opis = dictOrder()
        s = attr2item( opis)
        s.име = z.ime or '??'
        s.автор     = z.avtori_plus
        s.откъде    = [ danni.rubrika_kysa, danni.data ]
        s.издание   = 'радио'
        s.етикети   = [ z.zagolemi, z.dok,
                            'радиоколекция' in z.rubrika.lower() and 'стихове' not in op and 'прочит',
                            'стихове' in op and 'стихове',
                            ]
        s.година    = z.godina
        s['#част']  = z.nomer
        s['#продължителност'] = sizemins and sizemins*60
        s.вид       = [ k for k in 'разказ стихове'.split() if k in op]
        s.описание  = (z.opisanie or '').replace('_', ' ')
        s['#автори_отделни'] = z.avtori
        if danni.opisanie != s.описание:
            s.ориг_описание = danni.opisanie
        s.ориг_рубрика  = danni.rubrika
        #s.dirname = z.dirname

        if tyrsach and not z.bez_ime and z.ime:
            ime = z.ime
            if z.avtori_plus: ime += ' : '+z.avtori_plus
            s['#подобни'] = '\n# '.join( ['']+[str(t) for t in tyrsach( ime )])

        for k,v in list( opis.items()):
            if isinstance( v, (tuple,list)):
                v = ' '.join( str(x) for x in v if x )
            if not v: del opis[k]
            else:
                if isinstance( v,str) and v.isdigit(): v = int(v)
                opis[ k ] = v

        def filtr( fname ):
            return ''.join((fname
                    ).replace( '._', '.'
                    ).replace( '__', '_'
                    ).replace( '+_', '+'
                    ).replace( '_+', '+'

                    ).replace( '"',  ''
                    ).replace( "'",  ''
                    ).replace( '(',  '['   #sh
                    ).replace( ')',  ']'   #sh
                    ).replace( ':',  ''    #mplayer,make
                    ).replace( ',',  ''    #mplayer
                    #).replace( rI+'V'+p, '.4'
                    #).replace( 'V'+p,    '.5'
                    #).replace( 3*rI+p,'.3'
                    #).replace( 2*rI+p,'.2'
                    #).replace( 1*rI+p,'.2'
                    ##).replace( '\xA0',' '
                    ).split())

        dirname = fname_kanal+'/'+fname_kanal_vreme
        makedirs( dirname)
        ldirname = z.get( 'dirname_cyr','').rsplit('--радио')[0]
        if ldirname in ('радио', danni.rubrika_kysa, danni.rubrika, danni.rubrika.replace(' ','_'), z.get('rubrika_') ):
            ldirname = ''
        if danni.rubrika_kysa:
            rubr = rec2dir.filt_er( danni.rubrika)
            if ldirname.startswith( rubr):
                ldirname = ldirname[ len( rubr):].lstrip('-')
        #print( '33333333333333333', ldirname, danni.rubrika, file= sys.stderr)
        ldirname = '+'.join( n for n in [ fname_kanal_vreme,
                danni.rubrika_kysa or x.get('ime'),
                ldirname[:60] ]
                if n )

        for d in glob.glob( fname_kanal_vreme+'*'):
            try: os.remove( d)
            except: pass
        try:
            os.symlink( dirname, ldirname)
        except: pass

        fname = (z.dirname or fname_kanal)[:60]
        fname = filtr( sykr( fname))
        fname = dirname + '/' + fname
        usability.Dumper.force_block = '>'
        usability.Dumper.shorten_width = 15
        komentari = [ (k + ': ' +str(opis.pop(k))) for k in list( opis.keys()) if k[0]=='#' ]
        VIMtail = '# v' + 'im:ts=4:sw=4:expandtab:ft=yaml' #separated!
        r = usability.dump( opis)
        r += '\n'+'\n'.join( komentari)
        r += '''

срез:
участници:
 редактор:
 превод:
 драматизация:
 адаптация:
 изпълнение:
 музика:
 зв.реж:
 зв.оп:
 зв.оформ:
 муз.оформ:
 запис:
 режисьор:
съдържание:

''' + 0*'''
#излишните полета може да се оставят празни или да се изтрият
#срез:
# 12:34.5 - 890.7
#или
# 722 -
# - 900.2
#или
# име.на.парче1
# от-до
# име.на.парче2
# от-до
# ...

''' + VIMtail
        fopis0 = os.path.join( dirname, 'opis')
        fopis = fopis0 + '1'
        while os.path.exists( fopis):
            ro = open( fopis).read()
            if ro == r: break
            fopis += '1'
        else:
            with fopen( fopis) as f:
                f.write( r)

        #opis = link( opis1)
        if os.path.exists( fopis0):
            s = os.stat( fopis0)
            if s.st_nlink >1:
                os.remove( fopis0)
            else:
                f0 = fopis0
                while os.path.exists( f0):
                    f0 += '0'
                os.rename( fopis0, f0)
        os.link( fopis, fopis0)

        if o.cron_earlier_minutes:
            t -= datetime.timedelta( minutes= o.cron_earlier_minutes)

        if sizemins:
            if o.cron_later_percent:
                sizemins += (sizemins * o.cron_later_percent) // 100
            if o.cron_earlier_minutes: sizemins += o.cron_earlier_minutes
            if o.cron_later_minutes:
                sizemins += o.cron_later_minutes

        print( t.minute, t.hour, t.day, t.month, '*',
                o.cron_user or '',
                o.cron,
                sizemins and '-m '+str(sizemins) or '',
                '--fname', fname,
                '--stream', x.stream,
             )

if __name__ == '__main__':

    from svd_util import optz
    optz.bool( 'html_strict',   help= 'хтмл-парсер: стриктен' )
    optz.bool( 'html_notfixed', help= 'хтмл-парсер: непоправен оригинален' )
    optz.text( 'ienc',          help= 'входно кодиране [автоматично]' )
    optz.text( 'oenc',          help= 'изходно кодиране [%default] (напр. за crontab)', )
    optz.text( 'cron',          help= 'прави crontab, пускайки тази команда (може с аргументи)')
#    optz.text( 'cron_file',     help= 'записва го в този файл, иначе stdout')
    optz.text( 'cron_user',     help= 'потребител за crontab, ако трябва' )
    optz.bool( 'cron_fname_notime',     help= 'без дата/час в резултатното име' )
    optz.int(  'cron_earlier_minutes',  help= 'пуска толкова минути по-рано')
    optz.int(  'cron_later_minutes',    help= 'спира толкова минути по-късно')
    optz.int(  'cron_later_percent',    help= 'спира толкова процента по-късно')
    optz.bool( 'nofilter',      help= 'всичко, без филтри' )
    optz.int(  'days',          help= 'филтър толкова дни от днес [%default]', default=1 )
    optz.append( 'force',       help= 'включва на запис, формат: канал-чч:мм-чч:мм[-име] но може без име', )
#   optz.bool( 'preferdaily',   help= 'при наличие на дневна и всичко, без филтри' )

    choices= list( bnr_kanali.keys())
    optz.append( 'channel',   choices= choices,
                    help= 'канал за запис (разписание+източник) - от ('+ ' '.join(choices) + '); може няколко пъти; ['+kanal_default.name+']',
                    )
    optz.append( 'weekly',  help= 'входно седмично разписание: URL или файл; може няколко пъти' )
    optz.append( 'daily',   help= 'входно дневно разписание: URL или файл; може няколко пъти' )
    optz.append( 'stream',  help= 'източник за запис; може няколко пъти - към всяко разписание' )
    optz.append( 'filter',  help= 'допълнителен филтър съдържа-се-в-заглавието; може няколко' )
    optz.text(   'save_plan',  help= 'запис на резултатния списък в ТОВА.datetime' )
    optz.text(   'save_input', help= 'запис на входящите данни в ТОВА.wd.kanal.datetime' )
    optz.bool(   'save_text',  help= 'запис на текста отделно ако не се събира в името в име.text' )
    optz.bool(   'yesterday',  help= 'днеска е вчера' )
    optz.bool(   'today_daily',     help= 'извлича датата от името на файла с дневното разписание' )
    optz.str(    'channel_daily',   help= 'за кой канал е файла с дневното разписание' )
    optz.str(    'nalichni_opisi',  help= 'файлов-шаблон за достъп до наличните описи' )
    o,args = optz.get()

    if o.oenc:
        from svd_util.eutf import fix_std_encoding, filew
        fix_std_encoding( ENC= o.oenc)
        #print( '#', sys.stdout.encoding)

    def fopen( fn):
        if o.oenc: f = filew( o.oenc, fn)
        else: f = open( fn, 'w')
        return f

    for f in (o.filter or ()):
        INTITLES.append( f.lower().strip() )

    import itertools

    kanali = []
    kanali += [ da(
                    bnr_kanali.get( o.channel_daily) or
                        da( name= None, abbr= 'oo', weekly= None, stream= None, daily= None),
                    **dict( (k,v) for k,v in dict( weekly= w, stream= s, daily= d).items() if v)
                    )
                for w,s,d in itertools.zip_longest(
                        o.weekly or (), o.stream or (), o.daily or ())]
    kanali += [ bnr_kanali[k] for k in o.channel or () ]
    if not kanali: kanali.append( kanal_default)

    today = datetime.date.today()
    if o.yesterday: today -= datetime.timedelta( days=1)

    now = datetime.datetime.now()
    def pnow(): return now.strftime( '%Y%m%d.%H.%M') #.%S')

    retry = 3
    while retry:
        kanali_neuspeh = []
        for k in kanali:
            wdta = ddta = None
            neuspeh = None
            try:
                wdta = bnr_weekly.get( k, o)
            except:
                traceback.print_exc( file= sys.stderr)
                print( '  ??weekly', k, file= sys.stderr)
                neuspeh= True

            today_daily = today
            if o.today_daily and k.get('daily'):
                m = re.search( '(\d+)(\.(\d+)\.(\d+))', k.daily or '')
                if m:
                    td = m.group(1)
                    today_daily = datetime.date( year= int(td[:4]), month= int(td[4:6]), day= int(td[6:]))
                    if m.group(3):
                        now = datetime.datetime.combine( today_daily,
                                    datetime.time( hour= int(m.group(3)), minute= int(m.group(4)) ))
                    today = today_daily   #HACK
            try:
                ddta = bnr_daily.get( k, o, today_daily)
            except:
                traceback.print_exc( file= sys.stderr)
                print( '  ??daily', k, file= sys.stderr)
                neuspeh= True

            if neuspeh: kanali_neuspeh.append( k)

            if o.save_input:
                for pfx,dta in [['w',wdta], ['d',ddta]]:
                    if not dta: continue
                    if not isinstance( dta, dict): dta = { '': dta}
                    for key,val in dta.items():
                        fn = '.'.join( [ o.save_input, pfx, k.abbr, pnow(), key.rsplit('/',1)[-1], 'html' ])
                        with fopen( fn) as f:
                            f.write( val)

        retry -=1
        if kanali_neuspeh and retry:
            kanali = kanali_neuspeh
            sleep(7)
        else: break


    if 10:
        print( '\n#ww...', file= sys.stderr)
        for d in bnr_weekly.days:
            print( '\n#w...', d, file= sys.stderr)
    if 0:
        print( '\n#dd...', file= sys.stderr)
        for d in bnr_daily.today_items:
            print( '\n#d...', d, file= sys.stderr)

    rw = bnr_weekly.filter( today, ndays= o.days, nofilter= o.nofilter )
    rd = bnr_daily.filter(  today, ndays= o.days, nofilter= o.nofilter )

    r = rd
    for k,v in rw.items():
        if k not in rd:
            r[k] = v

    nasila = [ x.split('-',3) for x in (o.force or ())]
    rr = dictOrder()
    for dayofs in range( o.days):
        tday = today + datetime.timedelta( days= dayofs )
        for k_ot_do_ime in nasila:
            k,ot,do,*ime = k_ot_do_ime
            if '/' in do:
                do,dni = do.split('/')
                dni = dni.replace( ':', '-')
            else: dni = None
            kk = bnr_kanali[k]
            i = da( channel= kk.name, time= time4str( ot), endtime= time4str( do), stream= kk.stream, dni= dni)
            for a in r.values():
                if (a.today, a.stream, a.channel) != (tday, i.stream, i.channel):
                    continue
                if i.time >= a.endtime or a.time >= i.endtime:
                    continue
                a.time = min( a.time, i.time)
                a.endtime = max( a.endtime, i.endtime)
                break
            else:
                key = i.channel, tday, i.time
                a = rr[ key ] = da( i, today= tday, stream= i.stream, channel= i.channel )
            if ime: a.ime = ime[0]
    r.update( rr)

    def sortit( x, asdict =True, ignore =()):
        r = dictOrder()
        y = x.copy()
        r['tmdt'] = '%2d:%02d ' % y.get('time',(-1,-1)) + str( y.get('today', None))
        r.update( (k, y.pop(k)) for k in 'ime title text'.split() if k in y )
        r.update( (k, v) for k,v in sorted( y.items()) )
        if asdict: return r
        return 'dict( ' + ', '.join( k+'='+repr(v) for k,v in r.items() if k not in ignore)  + ' )'

    fzaglavia = ' '.join( str(x) for x in [
            '#филтър:', today, '+', o.days, 'дни;',
            'заглавия', INTITLES,
            'незаглавия', NOTINTITLES,
            ])

    if o.save_plan:
        fn = o.save_plan +'.'+ pnow()
        with fopen( fn) as f:
            print( fzaglavia, file=f )
            print( '[', file=f )
            for x in r.values():
                #print( ' ', x, ',', file=f)
                print( ' ', sortit( x, asdict=False), ',', file=f)
            print( ']', file=f )
            print( '#всички за деня:', file=f )
            for x in bnr_daily.today_items:
                print( '# ', sortit( x, asdict=False), file=f)

    if o.cron:
        cron( r.values(), o )

    print( fzaglavia, file= sys.stderr)
    for x in r.values():
        r = sortit(x)
        xx = [ r['tmdt'] ]
        xx += [ k+'= '+str(v) for k,v in r.items() if k not in 'time today tmdt'.split() ]
        #y = x.copy()
        #xx =  [ '%2d:%02d ' % y.pop('time',(-1,-1)) + str( y.pop('today', None)) ]
        #xx += [ k+': '+str(y.pop(k)) for k in 'ime title text'.split() if k in y ]
        #xx += [ k+': '+str(v) for k,v in sorted( y.items()) ]
        print( ' #', '; '.join( xx), file= sys.stderr)
    if not r: raise SystemExit(1)

# vim:ts=4:sw=4:expandtab

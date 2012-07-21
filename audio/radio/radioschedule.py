#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
1. cron.daily : radiorec-scheduler: прочита разписанието (http://programs..)
   и за всяко предаване прави ред в /etc/cron.d/radiorec
2. /etc/cron.d/radiorec: съдържа редове пускащи radiorec в съответното време
'''
from util.struct import DictAttr
da = DictAttr

bnr_kanali = da(
    hristobotev = da(
        weekly  = 'http://bnr.bg/sites/hristobotev/Pages/ProgramScheme.aspx',
        daily   = 'http://bnr.bg/sites/hristobotev/Daily/Pages/{yymmdd}.aspx',
        daily2  = 'http://bnr.bg/sites/hristobotev/Daily/Pages/{yymmdd}_izbrano.aspx',
        stream  = 'http://streaming.bnr.bg/HristoBotev',
        abbr = 'hb',
    ),
    horizont = da(
        weekly  = 'http://bnr.bg/sites/horizont/Pages/ProgramScheme.aspx',
        #daily   = 'http://bnr.bg/sites/horizont/Daily/Pages/{yymmdd}.aspx',
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

from util.txt import strip, slim

#Радиотеатър
#Златния фонд
#Златните гласове
#хлапета
#документално студио
INTITLES = strip('''
Радиотеат
театър
театр
за деца
Романи за деца
Златни
колекция
приказк
документа
''').lower().split('\n')

def title_match( title):
    if not title: return False
    title = title.lower().replace('  ',' ')
    for f in INTITLES:
        if f in title: return True

def time4str( t): #hh:mm or hh.mm ...
    x = re.split( '(\d+)', t)
    hm = x[1],(len(x)>3 and x[3] or 0)
    return tuple( int(a) for a in hm)

PROGRAMS = kanal_default.weekly
STREAM   = kanal_default.stream


import sys
from util.html_visitor import visit
from util.py3 import dictOrder
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
    def filter( me, today, n =1, nofilter =False):
        todays = [ today + datetime.timedelta( days= dayofs )
                    for dayofs in range( n) ]

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

from util import html_visitor
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

class bnr_daily:
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
        ''', re.X|re.DOTALL)
    @classmethod
    def get( me, kanal, o, today):
        for url in [ kanal.get('daily'), kanal.get('daily2'), ]:
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
            tds = re.split( '([оo][тt] *\d+([.:]\d+)? *[дd][оo] *\d+([.:]\d+)? *часа)', whole, flags= re.IGNORECASE )
            print( '#...', len(tds), len(me.today_items) -m, file= sys.stderr)
            #print( '#...', tds, file= sys.stderr)
            allitems = [ (tds[ i], tds[i+3])
                        for i in range( 1,len( tds),4) ]

            for times,data in allitems:
                times = re.split( '(\d+(.\d+)?)', times)
                m = me.re_titles.search( data)
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
    def filter( me, today, nofilter =False):
        items = dictOrder()
        for i in me.today_items:
            if not nofilter:
                if not title_match( i.title): continue
            key = i.channel, today, i.time
            items[ key ] = da( i, today= today, stream= i.stream, channel= i.channel )
        return items



def cron( items, o ):
    '''
cron/crontab plain:  # m h dom mon dow  command
cron.d/crontab direct: # m h dom mon dow (user) command
'''
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

        channel = x.channel
        if not channel:
            if x.stream:
                channel = x.stream.split('://')[-1].replace('/','_')
        if channel in bnr_kanali:
            channel = bnr_kanali[ channel ].abbr

        fname = str( channel)
        if not o.cron_fname_notime:
            fname += '-{t.month:02d}{t.day:02d}-{t.hour:02d}{t.minute:02d}'.format( **locals())
        if x.get('title'): fname += '+'+x.title
        if x.get('text'): fname += '+'+x.text

        #rI = '\u0406'   #І
        #p = ' част'
        fname = fname.replace('"',''
                    ).replace("'",''
                    ).replace('(','['   #sh
                    ).replace(')',']'   #sh
                    ).replace(':',''    #mplayer
                    ).replace(',',''    #mplayer
                    #).replace( rI+'V'+p, '.4'
                    #).replace( 'V'+p,    '.5'
                    #).replace( 3*rI+p,'.3'
                    #).replace( 2*rI+p,'.2'
                    #).replace( 1*rI+p,'.2'
                    ##).replace( '\xA0',' '
                    ).replace( '\u2013','-'     #-
                    ).replace( '\u0406','I'     #І
                    #).replace( '\u0425','X' cyrХ latX ?
                    ).replace(' - ','-'
                    ##).replace('  ',' '
                    ).replace('  ',' '
                    ).replace(' ','_'
                    )
        fname = fname[:120]

        if o.cron_earlier_minutes:
            t -= datetime.timedelta( minutes= o.cron_earlier_minutes)

        if sizemins:
            if o.cron_earlier_minutes: sizemins += o.cron_earlier_minutes
            if o.cron_later_minutes: sizemins += o.cron_later_minutes

        print( t.minute, t.hour, t.day, t.month, '*',
                o.cron_user or '',
                o.cron,
                sizemins and '-m '+str(sizemins) or '',
                '--fname', fname,
                '--stream', x.stream,
             )

if __name__ == '__main__':

    from util import optz
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
    optz.bool( 'nofilter',      help= 'всичко, без филтри' )
    optz.int(  'days',          help= 'филтър толкова дни от днес [%default]', default=1 )
    optz.append( 'force',       help= 'включва на запис, формат: канал-чч:мм-чч:мм', )
#   optz.bool( 'preferdaily',   help= 'при наличие на дневна и всичко, без филтри' )

    choices= list( bnr_kanali.keys())
    optz.append( 'channel',   choices= choices,
                    help= 'канал за запис (разписание+източник) - от ('+ ' '.join(choices) + '); може няколко пъти; ['+kanal_default.name+']',
                    )
    optz.append( 'weekly',  help= 'входно седмично разписание: URL или файл; може няколко пъти' )
    optz.append( 'daily',   help= 'входно дневно разписание: URL или файл; може няколко пъти' )
    optz.append( 'stream',  help= 'източник за запис; може няколко пъти - към всяко разписание' )
    optz.text(   'save_plan',  help= 'запис на резултатния списък в ТОВА.datetime' )
    optz.text(   'save_input', help= 'запис на входящите данни в ТОВА.wd.kanal.datetime' )
    optz.bool(   'yesterday',  help= 'днеска е вчера' )
    o,args = optz.get()

    if o.oenc:
        from util.eutf import fix_std_encoding, filew
        fix_std_encoding( ENC= o.oenc)
        #print( '#', sys.stdout.encoding)

    import itertools

    kanali = []
    kanali += [ da( name= None, weekly= w, stream= s, daily= d)
                for w,s,d in itertools.zip_longest(
                        o.weekly or (), o.stream or (), o.daily or ())]
    kanali += [ bnr_kanali[k] for k in o.channel or () ]
    if not kanali: kanali.append( kanal_default)

    today = datetime.date.today()
    if o.yesterday: today -= datetime.timedelta( days=1)

    now = datetime.datetime.now().strftime( '%Y%m%d.%H.%M') #.%S')

    for k in kanali:
        wdta = ddta = None
        try:
            wdta = bnr_weekly.get( k, o)
        except:
            traceback.print_exc( file= sys.stderr)
            print( '  ??weekly', k, file= sys.stderr)

        try:
            ddta = bnr_daily.get( k, o, today)
        except:
            traceback.print_exc( file= sys.stderr)
            print( '  ??daily', k, file= sys.stderr)

        if o.save_input:
            for pfx,dta in [['w',wdta], ['d',ddta]]:
                if not dta: continue
                fn = '.'.join( [ o.save_input, pfx, k.abbr, now, 'html' ])
                if o.oenc: f = filew( o.oenc, fn)
                else: f = open( fn, 'w')
                with f:
                    f.write( dta )
    if 0:
        for d in bnr_daily.today_items:
            print( '\n#...', d, file= sys.stderr)

    rw = bnr_weekly.filter( today, n= o.days, nofilter= o.nofilter )
    rd = bnr_daily.filter( today, nofilter= o.nofilter )

    r = rd
    for k,v in rw.items():
        if k not in rd:
            r[k] = v

    nasila = [ x.split('-') for x in (o.force or ())]
    rr = dictOrder()
    for dayofs in range( o.days):
        tday = today + datetime.timedelta( days= dayofs )
        for k,ot,do in nasila:
            kk = bnr_kanali[k]
            i = da( channel=kk.name, time= time4str( ot), endtime= time4str( do), stream= kk.stream)
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
                rr[ key ] = da( i, today= tday, stream= i.stream, channel= i.channel )
    r.update( rr)

    if o.save_plan:
        fn = o.save_plan +'.'+ now
        if o.oenc: f = filew( o.oenc, fn)
        else: f = open( fn, 'w')
        with f:
            print( '#филтър:', today, '+', o.days, 'дни;', 'заглавия', INTITLES, file=f )
            for x in r.values(): print( ' ', x, file=f)
            print( '#всички за деня:', file=f )
            for x in bnr_daily.today_items: print( '# ', x, file=f)

    if o.cron:
        cron( r.values(), o )

    print( '#филтър:', today, '+', o.days, 'дни;', 'заглавия', INTITLES, file= sys.stderr)
    for x in r.values(): print( ' #', x, file= sys.stderr)
    if not r: raise SystemExit(1)

#!/usr/bin/python3
# -*- coding: utf-8 -*-
#/home/tmp/hb+Запазена_марка_Радиотеатър+“Жак_фаталистът”от_Дени_Дидро-20110822.02.00.02.flac

import re,subprocess,sys,os
from os.path import join, isdir, splitext, basename, exists
from svd_util import lat2cyr, eutf, rim_digit as rim
from svd_util import optz, osextra
from svd_util.dicts import DictAttr
from instr import zaglavie
from glob import glob
import datetime

def c2l( x): return lat2cyr.zvuchene.cyr2lat( x).lower()
def spc(x): return x.replace( '_', ' ').replace('  ',' ').strip()
lc = 'oо aа eе cс xх '.split()
def rlatcyr( x, idx =1):
    for a in lc:
        x = x.replace( a[idx], '['+a+']')
    return x

def opravi_tireta( x, spc =' '):
    return (x
        ).replace( '\u2013','-' #- = x2013
        ).replace( '\xA0', spc
        )

_2cyr = lc + [
    ('а̀', 'а'),
    ('ѐ', 'е'),
    ('ѝ', 'и'),
    ( '\u0406','I'),     #І
    #( '\u0425','X' ) cyrХ latX ?
    ]

def opravi_cyr( x, **ka):
    x = opravi_tireta( x, **ka)
    for a,b in _2cyr:
        x = x.replace( a,b)
    return x

def razglobi( fime ):
    f,ext = splitext( basename( fime))
    f = opravi_tireta( f, '_')
    f = (f
            #.replace( 'o','о')   #lat-cyr
            #.replace( 'a','а')   #lat-cyr
            #.replace( 'e','е')   #lat-cyr
            .replace( '__','_')
            .replace( '__','_')
            )
    f = rim.rim2fix( f, doX=False)

    #bez datetime
    fd = re.split( r'(-\d{3,})', f, 1)
    f = fd[0]
    data = len(fd)>1 and fd[1].strip('-') or None

    dirname = f

    #> kanal + rubrika + imena
    m = re.match( r'^[^+]+ \+ ([^+]+) \+ (.*)', f, re.VERBOSE)
    if not m:
        print( '   xxx NOMATCH', fime)
        return locals() # data=data)

    rubrika = spc( m.group(1))
    imena = m.group(2).strip('_')
    #print( rubrika, ':', imena)
    return dict( razglobi_imena( imena=imena, rubrika=rubrika), data=data, dirname=dirname)

def rextract( regexp, txt, repl='', flags =0):
    if isinstance( regexp, str): regexp = re.compile( regexp, flags= flags)
    m = regexp.search( txt)
    if not m: return None,txt
    extracted = txt[ :m.start()] + repl + txt[ m.end(): ]
    return m,extracted

rend = '.,_-'
rquo = '„"”“'
requo= '['+rquo+']'
rnquo= '[^'+rquo+']'

rezlf = re.compile( rlatcyr( requo+'?златният?_*фонд'+requo+'?'), re.IGNORECASE)
reakm = re.compile( rlatcyr( '(лятна_*)?'+requo+'?академия_*комика'+requo+'?'), re.IGNORECASE)
rehs  = re.compile( rlatcyr( requo+'?хумор_*и_*сатира'+requo+'?'), re.IGNORECASE)
zlf = 'ЗлФ'
akomika = 'АКомика'
hs = 'ХС'

rerubrika = re.compile( rlatcyr( 'дядовата *ръкавичка|вицомания|звезди *посред'), re.IGNORECASE)

reteatyr_ime = re.compile( rlatcyr( '(_театър_)'+requo + '('+rnquo+'+)' + requo), re.IGNORECASE)

rIme = '([А-Я][а-я]+_*)'
rIme_= r'([А-Я]([а-я]{0,2}\.|[а-я]+)_*)'
rImeIme = rIme_ + '*([а-я]{1,3}_*){0,2}' + rIme +'+'
reime = re.compile( rImeIme )

regodishnina = re.compile( r'(?P<godini>\d+_години)_(след_)?(?P<avtor>[^:]+):_(?P<ime>.*)' )

def filt_er( x): return (x
                    ).strip(
                    ).replace( '  ',' '
                    ).replace( ' ', '_'
                    ).replace( '..','.'
                    ).replace( '__','_'
                    ).replace( '.-','-').replace( '-.','-'
                    ).replace( '_-','-').replace( '-_','-'
                    ).replace( '_.','.').replace( '._','.'
                    ).replace( '_:',':').replace( ':_',':'
                    ).replace( '+_','+').replace( '_+', '+'
                    ).replace( '---','--'
                    ).strip('_-'
                    )

def filt_er2( fname ): return filt_er( fname
                    ).replace( '"',  ''
                    ).replace( "'",  ''
                    ).replace( '(',  '-'   #sh
                    ).replace( ')',  '-'   #sh
                    ).replace( '[',  '-'   #sh
                    ).replace( ']',  '-'   #sh
                    ).replace( '{',  '-'   #sh
                    ).replace( '}',  '-'   #sh
                    ).replace( '/',  '-'
                    ).replace( ':',  '-'    #mplayer,make
                    #).replace( ',',  ''    #mplayer ? XXX
                    ##).replace( '\xA0',' '
                    )


slovom10 = 'първа втора трета четвърта пета шеста седма осма девета десета'.split()
slovom11 = 'единадесета дванадесета тринадесета четиринадесета петнадесета шестнадесета седемнадесета осемнадесета деветнадесета двадесета'.split()
slovom11+= ['двадесет и '+s for s in slovom10[:-1]] + ['тридесета']
slovom11+= ['тридесет и '+s for s in slovom10[:-1]] + ['четиридесета']
slovom11+= ['четиридесет и '+s for s in slovom10[:-1]]
#+ ['петдесета'] .. различно
re_rod = re.compile( 'а$')
def rodove(x): return re_rod.sub( '[аи]', x)
slovom10 = dict(
    (rodove(x).replace(' ','_'), i)
    for i,x in enumerate( slovom10 +
            [ s.replace( 'десета', '(десе|йсе?)та'
              ).replace( 'десет ', '(десет|йсе?т?) ')
                for s in slovom11 ]
            , 1))

def nomera( txt):
    nomer = ''
    ostatyk = txt

    rchast = rlatcyr( r'((част|епизод)и?|ч\.?)') #|глава
    rnomer = rim.re_nomer_extrafix

    rnomer = rnomer.replace( ')',
        ''.join( '|'+slovom[:-1]+'[аи]'
            for slovom in slovom10 #първ[аи] част/епизод
            )
            +')')

    rx1 = '(?P<nomer>_*' +rnomer+')_?'+rchast
    rx11= '(?P<nomer>_*('+rnomer+'_(и_)?)*' +rnomer+')_?'+rchast
    rx2 = '[-_]'+rchast+'_?(?P<nomer>'+rnomer+')'

    for rx in rx11,rx2:
        m,t = rextract( rx, txt, flags= re.IGNORECASE)
        if m:
            ostatyk = t
            nomer = m.group( 'nomer')
            break

    if nomer:
        nomer = nomer.strip('_')
        nomer = nomer2int( nomer)
    #print( 333333333, txt, nomer, ostatyk,m)
    return nomer,ostatyk

def nomer2int( nomer):
    n = slovom10.get( nomer)
    if n: nomer = n
    else:
        for slo,i in reversed( list(slovom10.items())):
            if re.fullmatch( slo, nomer):
                nomer = i
                break
        else:
            nomer = rim.rim2fix( nomer)
            nomer = rim.rim2int( nomer,nomer)
    return nomer

_test_nomera = '''
2 част      = 2
IV част     = 4
3 и 4 част  = 3 и 4
трета част  = 3
трета и 4 част  = трета и 4
двадесета част  =20
двайсета част   =20
двайста част    =20
двайсе и трета част     =23
двайсет и трета част    =23
двадесет и трета част   =23
двайсе и осма и девета част = двайсе и осма и девета
'''

def test_nomera():
    print( 'test_nomera')
    for tr in _test_nomera.strip().split('\n'):
        t,r = [a.strip().replace(' ','_') for a in tr.split('=')]
        n,o = nomera( t)
        if r != str(n): print( '??', n, ':', t, r, )

def sykr( x, lat =False):
    #def resubi( x,y): return re.sub( x,y, flags=re.IGNORECASE)
    x = re.sub( requo, '', x.strip())
    fn = opravi_cyr if not lat else opravi_tireta
    x = fn( x
            ).replace('  ',' '
            ).replace(' -','-'
            ).replace('- ','-'
            ).replace('--','-'
            ).replace(' ','_'
            ).replace('__','_'
            ).replace('__','_'
            )
    for a,b in [
              ('Документално_студио','Док_ст'
            ),('Ради?околекция',     'Ркц'
            ),('(.*?)?Р[ао]ди?отеатъ?р[аи]?_?за_?деца',       'Рт_деца'
            ),('Детски_радиотеатър', 'Рт_деца'
            ),('(.*?)?Р[ао]ди?отеатъ?р.*',    'Рт'      #(?!деца) negative-lookahead
            #),('Р[ао]ди?отеатъ?р',   'Рт'
            #),('(.*?_)?Рт_за_деца',     'Рт_деца'
            #),('(.*?_)?Рт_(?!деца).*',  'Рт'
            ),('Време_за_пр(иказка)?',  'ВзаП'
            ),('събуди_ме_с_пр(иказка)?', 'СъбП'
            ),('Ранобудно_петленце', 'СъбП'
            ),('Ваканционн?а_програма',   'Вкц'
            ),('Избрано_от_програма_{q}?Христо_Ботев{q}?'.format( q= requo), 'ХБ'
            ),('Избрано_от_', ''
            ),('фонда_на_(редакция)?',''
            ),('_на_БНР',''
            ),('Златните_гласове_на_радиото', 'Златните_гласове'
            ),('Запазе?на_марка',''
            ),('Семейно_радио', '' #Сем
            ),('Голямата_къща_на_смешните_хора', 'ГКСХ'
            ),('словестност',   'словесност'
            ),('Салон_за_класифицирана_словесност', 'ССл'
            ),('Съвременна',    'съвр.'
            ),(r'Драматург\w+',  'др.'
            ),('Незабравими_български_спектакли_във_фонда', 'бълг.др.'
            ),('българск[аи]',  'бълг.'
            ),(r'Документа\w+',  'док.',
            ),('Летящата_читалня', 'ЛЧ'
            )]:
            x = re.sub( a,b, x, flags= re.IGNORECASE)

    x = re.sub( rezlf, zlf, x)
    x = re.sub( reakm, akomika, x)
    x = re.sub( rehs, hs, x)
    x = x.strip( rend+':')
    return x


detski_rubr = 'деца детск приказк ВзаП СъбП'.lower().split()
#detski_ime  = 'събуди_ме_с_пр време_за_пр'.lower().split()  #radio/radioschedule-automatics

def razglobi_imena( imena, rubrika, ):
    imena = (imena.replace( '\u2013','-')  #- = x2013
            .replace( '\xA0','_')
            .replace( ' ','_')
            .replace( '__','_')
            )

    dok = False
    ime = avtor = ''
    ostatyk = ''
    opisanie = avtor_ot_opisanie = None
    bez_ime = False
    for q in rquo: rubrika = rubrika.replace( q, '')

    rubrika_kysa = sykr( rubrika)
    if rubrika_kysa == 'ХБ' and 'радиотеатър' in imena.lower():
        rubrika_kysa = 'Рт'
        rubrika = 'Радиотеатър'
    elif 'СКЛСЛ' in imena or 'ССл' in imena:
        rubrika = rubrika_kysa = 'ССл'
    rubrika_ = rubrika.replace(' ','_')

    for a,b in [
          ( '^Предаването.е.посветено.на', '',
        ),( '^Гост_*:', '',
        ),( 'редактор:_'+rImeIme, ''
        ),( 'поредица_[^:]+:_*', ''
        )]:
        imena = re.sub( a,b, imena, flags=re.IGNORECASE)
    if rezlf.search( rubrika_ ):
        opisanie = imena
        m = reime.search( imena)
        if m:
            avtor_ot_opisanie = m.group(0)
        ime = zlf
        bez_ime = True
    elif regodishnina.search( imena):
        m = regodishnina.search( imena)
        ime = m.group('ime')
        avtor = m.group('avtor')
    elif rerubrika.search( rubrika ):
        opisanie = imena
        ime = rubrika_
        bez_ime = True
    else:
        imena = rezlf.sub( zlf, imena)
        imena = reakm.sub( akomika, imena)
        imena = rehs.sub( hs, imena)
        imena = reteatyr_ime.sub( r'\1\2', imena)
        #imena > ime + (tip) + avtor.opis
        #imena = imena.lstrip( rquo+rend)
        imena = imena.strip( rend)
        tipove= '|'.join( 'документална_радиопиеса драматизация документално_студио'.split())
        razdelitel = rlatcyr( '_(от|по|на)_')
        ss = re.split( requo, imena)
        #print('#',5555555, ss)
        if len(ss)>1:   #nonquoted quoted nonquoted [quoted nonquoted]...
            avtor = ss.pop( len(ss)>2 and 2 or -1).strip( rend)
            if len(ss)>1: opisanie = ss.pop(0).strip( rend)
            ime = '_'.join( ss)
            razdelitel = '_?'+razdelitel.lstrip('_')
            #print( 3333, avtor, opisanie, ime)
            if opisanie:
                #... в романа на ... ; панорама на ...
                #Механизмът на едиквоси, разтълкуван от ... в
                if 10:
                    m,_t = rextract( rlatcyr( '_(на|от)_') + '('+rImeIme+')', opisanie)
                    if m:
                        avtor_ot_opisanie = m.group( 2)
                    else:
                        m,_t = rextract( '^('+rImeIme+')', opisanie)
                        if m:
                            avtor_ot_opisanie = m.group( 1)
        elif '-' in imena:
            ime,avtor = imena.split('-',1)
        else:
            ime = ''
            avtor = imena
        #print( 4444, avtor)
        m = re.match( '(?P<ime>.*?)'+razdelitel+'(?P<avtor>'+rImeIme+ ')(?P<ost>.*)', avtor)
        #print( 4444, m)
        if m:
            avtor = m.group( 'avtor').strip( rend)
            ostatyk = m.group( 'ost').strip( rend)
            if not ime:
                ime = m.group('ime')
                m,ime = rextract( rlatcyr( tipove), ime, flags= re.IGNORECASE)
                if m:
                    if 'док' in (m.group('tip') or '').lower(): dok = True
        else:
            ostatyk = avtor
            avtor = ''

    ime = ime.strip( rquo+rend)
    ime = spc( ime)
    if not ime:
        ime = rubrika
        bez_ime = True

    ostatyk = ostatyk.strip( rend)
    ostatyk = rim.rim2fix( ostatyk, doX= False)
    #print( 222222222, ostatyk)
    #avtor.opis > avtor + nomer.chast (+opis)

    nomer,ostatyk = nomera( ostatyk)

    ostatyk = ostatyk.strip( rend)
    m,ostatyk = rextract( ( rlatcyr(
            r'_? o? ((?P<g1>\d{4})_?г\.? | (?P<g3>премиера)) c?'
            .replace( 'o', r'[\[\(]')
            .replace( 'c', r'[\)\]]')
            )),
            ostatyk,
            flags= re.VERBOSE+re.IGNORECASE)
    if m:
        godina = m.group( 'g1') or m.group( 'g3') and datetime.date.today().year
    else: godina = None
    ostatyk = ostatyk.strip( rend)
    #print( 444444444, ostatyk, godina)

    if not avtor: avtor = ostatyk
    if not avtor and avtor_ot_opisanie: avtor = avtor_ot_opisanie
    #avtori
    m,_t = rextract( rImeIme, avtor)
    if m:
        avtor = m.group( 0)
    else:
        if len(avtor)>40: avtor = ''

    avtor = spc( avtor)
    avtor = ' '.join( a for a in avtor.split() if a.lower().strip(':') != 'автор' )
    avtori = re.split( ' и ', avtor)
    avtori = [ re.sub( r'(по )?(.+?)((народна|приказка|радиоадаптация|премиера)[ \.]?)+', r'\2',
                a.strip().strip('()'), re.IGNORECASE )
                    .replace( '[]','')
                    .strip()
                    .rstrip( rend)
                for a in avtori]
    avtori = [ a for a in avtori if a]

    avtori_kysi = []
    for a in avtori:
        avtor_imena = a.split()

        if avtor_imena:
            kys = len( avtor_imena)>1 and avtor_imena[0][0]+'.'+avtor_imena[-1] or avtor_imena[0]
            avtori_kysi.append( kys)
    avtor_kys = '-'.join( avtori_kysi)

    avtor_dylyg = '-'.join( avtori)
    ime4dir = '' if 'еко-ехо' in rubrika.replace(' ','').lower() else ime
    dirname_cyr = filt_er( '--'.join( a for a in [ ime4dir, avtor_dylyg, nomer and '#'+str(nomer), 'радио'] if a ))
    dirname_cyr = (dirname_cyr
                    #).replace('--:','--'
                    ).replace( ':','-'
                    ).replace( '--#','-'
                    ).replace( '----','--'
                    ).replace( '---','--'
                    ).replace( '---','--'
                    ).strip('-'
                    )
    dirname = c2l( dirname_cyr)

    avtori_plus = ' '.join( '_'.join( zaglavie(e) for e in a.split()) for a in avtori)
    avtori_plus = avtori_plus.replace( 'Детско_Творчество', 'Дете')

    otdeca = 'дете' == avtori_plus.lower()
    zagolemi = dok or not (
        sum( x in rubrika_kysa.lower()
            for x in detski_rubr )
        or otdeca
       )

    zagolemi = zagolemi and 'възрастни' or 'детски'
    dok = dok and 'док' or ''
    return locals()

def go( fime, fdir, nedei =False, command =None, move =True, decode =False):
    class Ddf( DictAttr):
        def __missing__( az, k): return ''
    ot_ime = Ddf( razglobi( fime))
    ot_ime.setdefault( 'ime', '_')
    cnomer = ot_ime.get( 'nomer')
    opis = '''
име: {ime}
етикети: {zagolemi} {dok}
издание: радио
откъде: {rubrika} {data}
'''.format( **ot_ime ) + '\n'.join(
        v+': '+str(ot_ime[k]) for k,v in dict(
        godina  = 'година',
        nomer   = '#част',
        avtori_plus = 'автор',
        opisanie= 'опис',
        ).items() if ot_ime.get(k) )

    opis = opis.strip()
    print( opis)
    opis += '''
повреда:
съдържание:
участници:
 редактор:
 превод:
 драматизация:
 изпълнение:
 музика:
 запис:
 з.реж:
 з.оп:
 з.оф:
 м.оф:
 режисьор:
описание:

# vim:ts=4:sw=4:expandtab:ft=yaml:ic'''

    dirname = ot_ime.get( 'dirname', fime )
    nomer   = cnomer

    print( '-----'*4)
    if nedei: return

    dir = join( fdir, dirname)
    orgdir = join( dir, '0')

    osextra.makedirs( orgdir, exist_ok= True)

    fnomer = nomer and '.'+str( nomer) or ''
    if not command: ext = '.wav'
    else: ext = ot_ime.ext
    wime = join( dir, dirname + fnomer + ext)
    print( ' > ', dir)
    print( ' >>', wime)

    if command:
        command( fime, wime)
        return

    fopis = join( dir, 'opis')
    while exists( fopis): fopis+='1'
    with eutf.filew_utf( fopis ) as f:
        print( opis, file= f)

    print( move and 'mv' or 'ln', fime, orgdir)
    bezext,ext = splitext( fime)
    ima_wav = False
    for f in glob( osextra.globescape( bezext)+'.*'):
        bf = basename( f)
        if f.endswith( '.wav'):
            ima_wav = True
            if cnomer: bf = str(cnomer)+'.'+bf
        (move and os.rename or os.link)( f, join( orgdir, bf ))

    #os.rename( fime, nime)
    if not ima_wav and optz.decode:
        bf = basename( fime)
        nime = join( orgdir, bf)
        if cnomer: bf = str(cnomer)+'.'+bf
        wwime = splitext( join( orgdir, bf))[0]+'.wav'
        if nime.endswith('.flac'):
            cmds = [ 'flac', '-d', '-o', wwime, nime ]
            print( cmds)
            subprocess.call( cmds)
        elif nime.endswith('.mp3'):
            cmds = 'lame --nohist -h -v -V 0 -S --decode'.split() + [ nime, wwime ]
            print( cmds)
            subprocess.call( cmds)

#   if not exists( wime):
#       open( wime, 'w').close()


if __name__ == '__main__':
    optz.bool( 'decode', '-d')
    optz.bool( 'nothing', '-n')
    optz.bool( 'link',    help= 'само връзка към новото име')
    optz.bool( 'nomove',  help= 'не мести към .../0/, а направи връзка')
    optz.str( 'where',  default= '.', help= '[%default]')    #'/zapisi/novo/'
    optz.str( 'test',  help= 'пуска eval( този-текст)')

    optz,argz = optz.get()
    if optz.test:
        print( eval( optz.test))
    else:
        command = optz.link and os.link
        for fime in argz:
            print( fime)
            go( fime, optz.where, nedei= optz.nothing, command= command, move= not optz.nomove, decode= optz.decode)

# vim:ts=4:sw=4:expandtab

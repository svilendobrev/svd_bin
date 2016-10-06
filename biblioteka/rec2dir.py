#!/usr/bin/python3
# -*- coding: utf-8 -*-
#/home/tmp/hb+Запазена_марка_Радиотеатър+“Жак_фаталистът”от_Дени_Дидро-20110822.02.00.02.flac

import re,subprocess,sys,os
from os.path import join, isdir, splitext, basename, exists
from svd_util import lat2cyr, eutf, rim_digit as rim
from svd_util import optz, osextra
from svd_util.struct import DictAttr
from instr import zaglavie
from glob import glob
import datetime

def c2l( x): return lat2cyr.zvuchene.cyr2lat( x).lower()
def spc(x): return x.replace( '_', ' ').strip()
lc = 'oо aа eе cс'.split()
def rlatcyr( x, idx =1):
    for a in lc:
        x = x.replace( a[idx], '['+a+']')
    return x

def opravi_tireta( x, spc =' '):
    return (x
        .replace( '\u2013','-')  #- = x2013
        .replace( '\xA0', spc)
        )

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
    fd = re.split( '(-\d{3,})', f, 1)
    f = fd[0]
    data = len(fd)>1 and fd[1].strip('-') or None

    dirname = f

    #> kanal + rubrika + imena
    m = re.match( '^[^+]+ \+ ([^+]+) \+ (.*)', f, re.VERBOSE)
    if not m:
        print( '   xxx NOMATCH', fime)
        return locals() # data=data)

    rubrika = spc( m.group(1))
    imena = m.group(2).strip('_')
    #print( rubrika, ':', imena)
    return razglobi_imena( imena=imena, rubrika=rubrika, data=data, dirname=dirname)

def rextract( regexp, txt, flags =0):
    if isinstance( regexp, str): regexp = re.compile( regexp, flags= flags)
    m = regexp.search( txt)
    if not m: return
    extracted = txt[ :m.start()] + txt[ m.end(): ]
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
rIme_= '([А-Я]([а-я]{0,2}\.|[а-я]+)_*)'
rImeIme = rIme_ + '+([а-я]{1,3}_*){0,2}' + rIme +'+'
reime = re.compile( rImeIme )

regodishnina = re.compile( '(?P<godini>\d+_години)_(след_)?(?P<avtor>[^:]+):_(?P<ime>.*)' )

def filt_er( x): return (x
                    ).replace( '  ',' '
                    ).replace( ' ', '_'
                    ).replace( '..','.'
                    ).replace( '__','_'
                    ).replace( '.-','-'
                    ).replace( '-.','-'
                    ).replace( '_-','-'
                    ).replace( '-_','-'
                    ).replace( '_.','.'
                    )

slovom10 = 'първа втора трета четвърта пета шеста седма осма девета десета'.split()
slovom10 = dict(
    (x, i)
    for i,x in enumerate( slovom10, 1)
    )

def razglobi_imena( imena, rubrika, data, dirname):
    imena = (imena.replace( '\u2013','-')  #- = x2013
            .replace( '\xA0','_')
            .replace( ' ','_')
            )

    dok = False
    ime = avtor = ''
    ostatyk = ''
    opisanie = avtor_ot_opisanie = None
    bez_ime = False
    for q in rquo: rubrika = rubrika.replace( q, '')
    rubrika_ = rubrika.replace(' ','_')
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
        tipove= 'документална_радиопиеса драматизация документално_студио'.replace(' ','|')
        razdelitel = rlatcyr( '_(от|по|на)_')
        ss = re.split( requo, imena)
        if len(ss)>1:
            avtor = ss.pop(-1).strip( rend)
            if len(ss)>1: opisanie = ss.pop(0).strip( rend)
            ime = '_'.join( ss)
            razdelitel = razdelitel.lstrip('_')
            if opisanie:
                #... в романа на ... ; панорама на ...
                #Механизмът на едиквоси, разтълкуван от ... в
                if 10:
                    m = rextract( rlatcyr( '_(на|от)_') + '('+rImeIme+')', opisanie)
                    if m:
                        m,_ostavi = m
                        avtor_ot_opisanie = m.group( 2)
                    else:
                        m = rextract( '^('+rImeIme+')', opisanie)
                        if m:
                            m,_ostavi = m
                            avtor_ot_opisanie = m.group( 1)

        elif '-' in imena:
            ime,avtor = imena.split('-',1)
        else:
            ime = ''
            avtor = imena

        m = re.match( '(?P<ime>.*?)'+razdelitel+'(?P<avtor>'+rImeIme+ ')(?P<ost>.*)', avtor)
        if m:
            avtor = m.group( 'avtor').strip( rend)
            ostatyk = m.group( 'ost').strip( rend)
            if not ime:
                ime = m.group('ime')
                m = rextract( rlatcyr( tipove), ime, flags= re.IGNORECASE)
                if m:
                    m,ime = m
                    if 'док' in (m.group('tip') or '').lower(): dok = True
        else:
            ostatyk = avtor
            avtor = ''

    ime = ime.strip( rquo+rend)
    ime = (spc( ime)
            .replace( '  ',' ')
            )
    if not ime:
        ime = rubrika
        bez_ime = True

    ostatyk = ostatyk.strip( rend)
    ostatyk = rim.rim2fix( ostatyk, doX= False)
    #print( 222222222, ostatyk)
    #avtor.opis > avtor + nomer.chast (+opis)
    nomer = ''

    rchast = rlatcyr( '((част|епизод)и?|ч\.?)') #|глава
    rnomer = rim.re_nomer_extrafix

    rnomer = rnomer.replace( ')',
        ''.join( '|'+slovom[:-1]+'[аи]'
            for slovom in slovom10 #първ[аи] част/епизод
            )
            +')')

    m = rextract( '(?P<nomer>_*('+rnomer+'_(и_)?)*' +rnomer+')_?'+rchast, ostatyk, flags= re.IGNORECASE)
    if m:
        m,ostatyk = m
        nomer = m.group( 'nomer')
    else:
        m = rextract( '[-_]'+rchast+'_?(?P<nomer>'+rnomer+')', ostatyk, flags= re.IGNORECASE)
        if m:
            m,ostatyk = m
            nomer = m.group( 'nomer')

    n = slovom10.get( nomer)
    if n: nomer = n
    else:
        nomer = rim.rim2fix( nomer)
        nomer = rim.rim2int( nomer,nomer)
    #print( 333333333, ostatyk, nomer)

    ostatyk = ostatyk.strip( rend)
    m = rextract( ( rlatcyr(
            r'_? o? ((?P<g1>\d{4})_?г\.? | (?P<g3>премиера)) c?'
            .replace( 'o', r'[\[\(]')
            .replace( 'c', r'[\)\]]')
            )),
            ostatyk,
            flags= re.VERBOSE+re.IGNORECASE)
    if m:
        m,ostatyk = m
        godina = m.group( 'g1') or m.group( 'g3') and datetime.date.today().year
    else: godina = None
    ostatyk = ostatyk.strip( rend)
    #print( 444444444, ostatyk, godina)

    if not avtor: avtor = ostatyk
    if not avtor and avtor_ot_opisanie: avtor = avtor_ot_opisanie
    #avtori
    m = rextract( rImeIme, avtor)
    if m:
        m,_ostavi = m
        avtor = m.group( 0)
    else:
        if len(avtor)>40: avtor = ''

    avtor = spc( avtor)
    avtori = re.split( ' и ', avtor)
    avtori = [ re.sub( '(по )?(.+?)((народна|приказка|радиоадаптация|премиера)[ \.]?)+', r'\2',
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
    dirname_cyr = filt_er( '--'.join( a for a in [ ime, avtor_dylyg, 'радио'] if a ))
    dirname = c2l( dirname_cyr)

#    [0].upper()+a[1:]
    avtori_plus = ' '.join( ''.join( zaglavie(e) for e in a.split()) for a in avtori)

    zagolemi = (dok or not sum( x.lower() in rubrika.lower() for x in 'деца приказк ВзаП'.split()) ) and 'възрастни' or ''
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
срез:
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
съдържание:
описание:

# vim:ts=4:sw=4:expandtab:ft=yaml'''

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

    optz,argz = optz.get()
    command = optz.link and os.link

    for fime in argz:
        print( fime)
        go( fime, optz.where, nedei= optz.nothing, command= command, move= not optz.nomove, decode= optz.decode)

# vim:ts=4:sw=4:expandtab

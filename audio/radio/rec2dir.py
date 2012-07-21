#!/usr/bin/python3
# -*- coding: utf-8 -*-
#/home/tmp/hb+Запазена_марка_Радиотеатър+“Жак_фаталистът”от_Дени_Дидро-20110822.02.00.02.flac

import re,subprocess,sys,os
from os.path import join, isdir, splitext, basename, exists
from util import lat2cyr, eutf, rim_digit as rim

def go( fime, fdir):
    f,ext = splitext( basename( fime))
    f = (f  .replace( '\u2013','-')  #- = x2013
            .replace( '\xA0','_')
            #.replace( 'o','о')   #lat-cyr
            #.replace( 'a','а')   #lat-cyr
            #.replace( 'e','е')   #lat-cyr
            .replace( '__','_')
            .replace( '__','_')
            )
    f = rim.rim2fix( f, doX=False)

    def spc(x): return x.replace( '_', ' ').strip()

    def rlatcyr(x): return (x
            .replace( 'o','[oо]')   #lat-cyr
            .replace( 'a','[aа]')   #lat-cyr
            .replace( 'e','[eе]')   #lat-cyr
            )

    #bez datetime
    fd = re.split( '(-\d{3,})', f, 1)
    f = fd[0]
    data = fd[1].strip('-')

    #> rubrika + imena
    m = re.match( '^[^+]+ \+ ([^+]+) \+ (.*)', f, re.VERBOSE)
    if not m:
        print( '   xxx NOMATCH', fime)
        return 1111111

    rubrika = spc( m.group(1))
    imena = m.group(2).strip('_')
    #print( rubrika, ':', imena)

    dok = False

    #imena > ime + (tip) + avtor.opis
    imena = imena.lstrip( '„"”“_')
    tipove= 'документална_радиопиеса драматизация'.replace(' ','|')
    razdelitel = rlatcyr( '_(?P<tip>'+tipove+')?_?(от|по)_')
    ss = re.split( '["”“]', imena)
    if len(ss)>1:
        avtor = ss[-1]
        ime = '"'.join( ss[:-1])
        razdelitel = razdelitel.lstrip('_')
    else:
        ime = ''
        avtor = imena

    m = re.match( '(?P<ime>.*?)'+razdelitel+'(?P<avtor>.*)', avtor, flags= re.I)
    if m:
        if not ime: ime = m.group('ime')
        avtor = m.group('avtor').lstrip('_')
        if 'док' in (m.group('tip') or '').lower(): dok = True

    #print( ime, '      :'+avtor, m and '', dok)
    if not m:
        print( '   yyy', repr( avtor), imena)
        #return 22222222

    m = re.match( rlatcyr( '(документално_студио_*)(.*)'), ime, flags= re.I )
    if m and m.group(2):
        ime = m.group(2)
        dok = True

    ime = ime.strip( '„"”“_-.,')
    avtor = avtor.strip('_-')
    avtor = rim.rim2fix( avtor)

    ime = spc( ime)

    #avtor.opis > avtor + nomer.chast (+opis)
    nomer = ''

    rchast = rlatcyr( '(част|епизод)')
    rnomer = rim.re_nomer
    ss = re.split( rnomer+'_?'+rchast, avtor)
    if len(ss)>1:
        avtor,nomer = ss[:2]
    else:
        ss = re.split( '[-_]'+rchast+'_?'+rnomer, avtor)
        if len(ss)>1:
            avtor,chast,nomer = ss[:3]
    #print( ss)

    avtor = avtor.strip('_-')
    nomer = rim.rim2int( nomer, nomer)

    #avtori
    avtor = spc( avtor)
    avtori = re.split( ' и ', avtor)
    avtori_kysi = []
    for a in avtori:
        avtor_imena = a.split()
        if avtor_imena:
            kys = len( avtor_imena)>1 and avtor_imena[0][0]+'.'+avtor_imena[-1] or avtor_imena[0]
            avtori_kysi.append( kys)

    def c2l( x): return lat2cyr.zvuchene.cyr2lat( x).lower()

    avtor_kys = '-'.join( avtori_kysi)
    dirname = '--'.join( [c2l( ime), c2l(avtor_kys), 'radio'] ).replace(' ', '.')

    avtori = '+'.join( ''.join( a.split()) for a in avtori)

    dir = join( fdir, dirname)
    orgdir = join( dir, '0')
    fnomer = nomer and '.'+str( nomer)

    if not command: ext = '.wav'
    wime = join( dir, dirname + fnomer + ext)
    print( ' > ', dir)
    print( ' >>', wime)

    if command:
        command( fime, wime)
        return

    zagolemi = (dok or 'деца' not in rubrika.lower() or 'приказк' not in rubrika.lower()) and 'възрастни' or ''
    cnomer = nomer and '#част: '+str(nomer)
    dok = dok and 'док' or ''
    opis = '''
име: {ime}
етикети: {zagolemi} {dok}
издание: радио
автор: {avtori}
участници:
опис:
{cnomer}

#{data}
# vim:ts=4:sw=4:expandtab:ft=yaml
'''.format( **locals()).strip()

    print( opis)
    print( '-----'*4)
    if nedei: return 33333333

    try: os.makedirs( orgdir)
    except: pass

    fopis = join( dir, 'opis')
    while exists( fopis): fopis+='1'
    with eutf.filew_utf( fopis ) as f:
        print( opis, file= f)

    nime = join( orgdir, os.path.basename( fime))
    print( 'mv', fime, nime)
    os.rename( fime, nime)
    if nime.endswith('.flac'):
        cmds = [ 'flac', '-d', '-o', wime, nime ]
        print( cmds)
        subprocess.call( cmds)
    elif not exists( wime):
        open( wime, 'w').close()


def opt(x):
    try: sys.argv.remove( x ); return True
    except ValueError: return None

nedei = opt('-n')
command = (opt('-ln') or opt('--ln')) and os.link

fdir = '/zapisi/novo/'
args = []
for f in sys.argv[1:]:
    if f[-1] == '/' or isdir( f):
        fdir = f
        continue
    args.append( f)

for fime in args:
    print( fime)
    go( fime, fdir)

# vim:ts=4:sw=4:expandtab

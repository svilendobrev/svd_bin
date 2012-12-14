#!/usr/bin/python3
# -*- coding: utf-8 -*-
#/home/tmp/hb+Запазена_марка_Радиотеатър+“Жак_фаталистът”от_Дени_Дидро-20110822.02.00.02.flac

import re,subprocess,sys,os
from os.path import join, isdir, splitext, basename, exists
from svd_util import lat2cyr, eutf, rim_digit as rim
from svd_util import optz, osextra
from svd_util.struct import DictAttr
from glob import glob

def c2l( x): return lat2cyr.zvuchene.cyr2lat( x).lower()

def razglobi( fime ):
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
        return locals() # data=data)

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
        ime = '_'.join( ss[:-1])
        razdelitel = razdelitel.lstrip('_')
    elif '-' in imena:
        ime,avtor = imena.split('-',1)
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
        print( '   ??? ', repr( avtor), imena)
        #return 22222222

    m = re.match( rlatcyr( '(документално_студио_*)(.*)'), ime, flags= re.I )
    if m and m.group(2):
        ime = m.group(2)
        dok = True

    ime = ime.strip( '„"”“_-.,')
    avtor = avtor.strip('_-')
    avtor = rim.rim2fix( avtor, doX= False)

    ime = spc( ime)

    #avtor.opis > avtor + nomer.chast (+opis)
    nomer = ''

    rchast = rlatcyr( '(част|епизод)и?')
    rnomer = rim.re_nomer
    ss = re.split( '(('+rnomer+'_(и_)?)*' +rnomer+')_?'+rchast, avtor)
    #print( 1111111111111111111111111111, ss)
    if len(ss)>1:
        avtor,nomer = ss[:2]
    else:
        ss = re.split( '[-_]'+rchast+'_?'+rnomer, avtor)
        if len(ss)>1:
            avtor,chast,nomer = ss[:3]

    avtor = avtor.strip('_-')
    nomer = rim.rim2int( nomer, nomer)

    #avtori
    avtor = spc( avtor)
    avtori = re.split( ' и ', avtor)
    avtori = [ re.sub( '(.+?)((народна|приказка|радиоадаптация)[_ \.]?)+', r'\1', a.strip(), re.IGNORECASE
                    ).replace( '[]',''
                    ).rstrip('.'
                    ).rstrip('_'
                    ).strip()
                for a in avtori]

    avtori_kysi = []
    for a in avtori:
        avtor_imena = a.split()
        if avtor_imena:
            kys = len( avtor_imena)>1 and avtor_imena[0][0]+'.'+avtor_imena[-1] or avtor_imena[0]
            avtori_kysi.append( kys)
    avtor_kys = '-'.join( avtori_kysi)

    avtor_dylyg = '-'.join( avtori)
    dirname = '--'.join( [c2l( ime), c2l(avtor_dylyg), 'radio'] ).replace(' ', '.')

    avtori_plus = '+'.join( ''.join( a.split()) for a in avtori)

    zagolemi = (dok or 'деца' not in rubrika.lower() and 'приказк' not in rubrika.lower()) and 'възрастни' or ''
    dok = dok and 'док' or ''
    return locals()

def go( fime, fdir, nedei =False, command =None):
    ot_ime = DictAttr( razglobi( fime))
    cnomer = ot_ime.get( 'nomer')
    opis = '''
име: {ime}
етикети: {zagolemi} {dok}
издание: радио
автор: {avtori_plus}
откъде: {rubrika} {data}
{cnomer}
'''.format( cnomer= cnomer and '#част: '+str(cnomer), **ot_ime ).strip()

    print( opis)
    opis += '''
срез:
участници:
 ред:
 изп:
 др:
 муз:
 з.реж:
 з.оп:
 з.еф:
 м.оф:
 реж:
опис:

# vim:ts=4:sw=4:expandtab:ft=yaml'''

    dirname = ot_ime.dirname
    nomer   = ot_ime.nomer

    print( '-----'*4)
    if nedei: return

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

    try: os.makedirs( orgdir)
    except: pass

    fopis = join( dir, 'opis')
    while exists( fopis): fopis+='1'
    with eutf.filew_utf( fopis ) as f:
        print( opis, file= f)

    print( 'mv', fime, orgdir)
    bezext,ext = splitext( fime)
    ima_wav = False
    for f in glob( osextra.globescape( bezext)+'.*'):
        os.rename( f, join( orgdir, basename( f) ))
        if f.endswith( '.wav'): ima_wav = True

    #os.rename( fime, nime)
    if not ima_wav and optz.decode:
        nime = join( orgdir, basename( fime))
        wwime = splitext( join( orgdir, basename( fime)))[0]+'.wav'
        if nime.endswith('.flac'):
            cmds = [ 'flac', '-d', '-o', wwime, nime ]
            print( cmds)
            subprocess.call( cmds)
        elif nime.endswith('.mp3'):
            cmds = 'lame --nohist -h -v -V 0 -S --decode'.split() + [ nime, wwime ]
            print( cmds)
            subprocess.call( cmds)

    if not exists( wime):
        open( wime, 'w').close()


if __name__ == '__main__':
    optz.bool( 'decode', '-d')
    optz.bool( 'nothing', '-n')
    optz.bool( 'link',  '--ln')
    optz.str( 'where',  default= '.', help= '[%default]')    #'/zapisi/novo/'
    #print( optz.oparser._short_opt)
    optz,argz = optz.get()
    command = optz.link and os.link

    for fime in argz:
        print( fime)
        go( fime, optz.where, nedei= optz.nothing, command= command)

# vim:ts=4:sw=4:expandtab

# -*- coding: utf-8 -*-
from opisvane import prevodi_parse, zaglavie, prn #XXX zaglavie(xyz)-> info.setup
import textwrap
textwrap = textwrap.TextWrapper(
    width =80,
    subsequent_indent = '  ',
    break_long_words = False,
    break_on_hyphens = False,
)

'''
заглавие
още...
.ru: руско заглавие
.ru: още...

детски дълги игрални
кукли парцалки
автор: пиксар
звук: бг
година: 2005
описание: ред1
описание: ред2
друго: ред1.1
 ред1.2

 ред2
още:: ред1
 ред2
 ред3
#коментар
съдържание:
 ред1
 ред2
преводи:
 файл1==име1
 файл2==име2
 група: имегрупа
 файл3==име3
'''

rest_keyvalue = '''
key: val
key1: v.1
    v.2
    v.3

    v.4
    v.5
key2:
    v.1
    v.2
'''


class opis_io:
    '''syntax:
заглавие
...
  празен ред
етикет : стойност
етикет етикет
...
съдържание: #за единичен файл съдържащ няколко неща
 редове
...
преводи:    #за няколко отделни файла
 файл-име == заглавие
...
'''
    @classmethod
    def procheti( klas, az, redove):
        dbg=0
        nomer = 0
        ime = ''
        systoyanie = 'ime'
        prevodi = []
        stoinost = []   #key, values
        sydyrzhanie = []
        def popylni_stoinost():
            k = stoinost[0]
            vv = stoinost[1:]
            if k == az.stoinosti.sydyrzhanie:
                vv = [ r for r,n in vv ]  #не маха празните, за разделител - освен отпред и отзад
                if vv[0][:1]==':':   #много-редове; ключ:: ... ; всеки нов ред е нов ред
                    vv[0] = vv[0][1:]
                while vv and not vv[0]: del vv[0]
                while vv and not vv[-1]: del vv[-1]
                sydyrzhanie.extend( vv)
            elif k == az.stoinosti.prevodi:
                prevodi.extend( (r,n) for r,n in vv if r )  #също?
            else:
                vv = [ r for r,n in vv ]
                if vv[0][:1]==':':   #много-редове; ключ:: ... ; всеки нов ред е нов ред
                    vv[0] = vv[0][1:]
                    v = '\n'.join( vv ).strip()
                else:   #много-абзаци; ключ: ... ; 2 нови реда са нов ред, иначе се слепват
                    v = ' '.join( (r or '\n') for r in vv ).strip().replace( ' \n ', '\n')
                az.slaga_etiket( k,v, zamesti= False )
            stoinost[:] = []

        for red in redove:
            nomer += 1
            red = red.expandtabs(4)
            red = red.rstrip()
            red0 = red.lstrip()
            if red0.startswith( '#'):
                az.komentari.append( red0)
                continue

            az.redove.append( red)
            if systoyanie == 'ime':
                red = red0
                #if dbg: print( '?ime', red)
                if red:
                    mezik = az.re_ezik_ime and az.re_ezik_ime.match( red)
                    if mezik:
                        e = mezik.group(1)
                        r = mezik.group(2)
                        az.imena[e] = zaglavie( az.imena.get( e, '') + ' ' + r)
                        continue

                    ime += ' ' + red
                    if dbg: print( '+ime', red)
                else:
                    systoyanie = 'etiketi'
                continue

            if stoinost:
                if not red:
                    stoinost.append( (red, nomer) )
                    continue

                krai = red[0].strip()    #non-space
                #prazno = len( red) - len( red1)
                sydyrzhanie_izvynredno = stoinost[0] in [az.stoinosti.sydyrzhanie, az.stoinosti.prevodi] and ':' not in red
                if not krai or sydyrzhanie_izvynredno:
                    #if not stoinost_prefix: stoinost_prefix = prazno
                    stoinost.append( (red0, nomer) )
                    if dbg: print( 221, '+stoinost', red)
                    continue
                if dbg: print( 22, '-stoinost')
                popylni_stoinost()

            elif not red: continue

            stst = red.find( ':')
            prev = red.find( '=')
            e_stst = stst >0
            e_prev = prev >0
            if e_prev and e_stst:
                if prev<stst: e_stst = 0
                else: e_prev = 0

            if e_prev:
                if dbg: print( 11, 'prev', red)
                prevodi.append( (red, nomer) )
            elif e_stst:
                if dbg: print( 11, 'stoinost', red)
                kv = [a.strip() for a in red.split(':',1)]
                k = kv[0]
                v = len(kv)>=1 and kv[-1] or ''
                if k == az.stoinosti.grupa:
                    stoinost = [az.stoinosti.prevodi, (red,nomer) ]
                else:
                    stoinost = [k, (v,nomer) ]
            else:   #etiketi
                if dbg: print( 11, 'etiketi', red)
                for k in red.split():
                    az.slaga_etiket( k, True)


        if stoinost:
            popylni_stoinost()

        grupa = None
        for red,nomer in prevodi:
            grupa = klas.procheti_prevod( az, red, nomer, grupa)

        if ime and ime.strip(): az.slaga_ime( ime.strip())
        if sydyrzhanie: az.etiketi.sydyrzhanie = sydyrzhanie

    @classmethod
    def procheti_prevod( klas, az, red, nomer, igrupa):
        gg = red.split( az.stoinosti.grupa+':', 1)
        if len(gg)>1 and not gg[0].strip():
            g = gg[1].strip()
            dop = kyso = ime = ''
            if '+=' in g:
                kyso,dop = (s.strip() for s in g.split('+='))
            elif '==' in g:
                ime,kyso = (s.strip() for s in g.split('=='))
            else: ime = g
            igrupa = az.nova_grupa( dylgo= ime, kyso= kyso, dop= dop)
            return igrupa

        try:
            k,v,o = prevodi_parse( red, nomer)
        except AssertionError as e:
            err( 'PARSING ', az.fname, e.message, stderr=1)
            raise
        v = zaglavie( v)
        k = az.bez_ext( k)
        q = az.prevodi.get( k)
        if q and q.ime != v: err( 'повтаря се:', k, az.fname, v, '\n;;', q.ime)
        az.nov_prevod( fname= k, ime= v, grupa= igrupa, original= o, roditel= az.fname)
        return igrupa

    @classmethod
    def zapis( klas, az, d =None, naistina =False):
        d = d or az.danni()

        MIN_BROI_BUKVI = 20

        r = [ d.ime ]
        r+= [ '.'+k+': '+v  for k,v in d.imena.items() ]
        r+= [ '']

        if d.simvoli: r+= [ ' '.join( d.simvoli)]

        if az.options.shirina_tekstove>0: textwrap.width = az.options.shirina_tekstove
        for k,vv in d.etiketi:
            if isinstance( vv, str): vv = vv.splitlines()
            if not isinstance( vv, list): vv = [vv]
            if len(vv)==1 or not az.options.mnogoredovi_etiketi:   # много редове k:v ; с пренасяне
                textwrap.initial_indent = k+': '
                for v in vv:
                    tv = textwrap.wrap( v)
                    r+= tv
                    #r+= [ k+':'+(v and ' '+v) for v in tv]
            else: # k:: много редове v ; без пренасяне
                r+= [ k+'::']
                r+= [ (v and ' '+v) for v in vv]

        lkmin = MIN_BROI_BUKVI
        if not az.options.podravni_po_grupi and az.prevodi:
            lkmin = max( lkmin, max( len(k) for k in az.prevodi))
        def prev2zapis( pr):
            if not pr: return pr
            lk = max( lkmin, max( len(p.fname) for p in pr))
            lv = max( MIN_BROI_BUKVI, max( len(p.ime) for p in pr))
            return [ ' '+(p.fname.ljust(lk) +' == '+ p.ime
                        + (p.original and ' '*(lv-len(p.ime)) +' == '+p.original or '')
                     ) for p in pr ]

        if d.prevodi or d.grupi:
            r+= [ az.stoinosti.prevodi+':']
            r+= prev2zapis( d.prevodi)

        for g in d.grupi:
            if g.dop: gime = g.kyso + ' += ' + g.dop
            elif g.kyso != g.ime: gime = g.ime + ' == ' + g.kyso
            else: gime = g.ime
            r+= [ '', az.stoinosti.grupa+':' + (gime and ' '+gime or '') ]
            r+= prev2zapis( g.elementi)

        org = az.redove
        if d.komentari:
            r += [ ''] + d.komentari
            org = org + d.komentari

        return az._zapis( r, org, naistina= naistina, ext='.txt' )

# vim:ts=4:sw=4:expandtab

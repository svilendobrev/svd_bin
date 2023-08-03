#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opisvane import info
import re

if __name__ == '__main__':

    class film_info( info):
        avtori_en = [
            'дисни  disni disney',
            'пиксар pixar',
            'ДУ     дриймуоркс дрийм-уоркс dreamworks',
            'уорнър warner',
            'БС     НС блюскай блю-скай bluesky blue_sky blue-sky',

            'Дис    Discovery Дискавъри dis',
            'ББС    BBC',
            'НГ     NG',
            'АП     AP AnimalPlanet Animal-Planet',
            'ПБС    PBS',
            'Имакс  IMAX',
        ]
        zamestiteli_po_stoinost = dict( info.zamestiteli_po_stoinost,
            avtor = avtori_en,  #+ ..
            )

        re_xy = re.compile( '[-. _]?(w\d{3,4}|\d{3,4}p)')
        svoistva_ot_fname__shabloni = [ re_xy, info.re_godina, ]    #всички
        svoistva_ot_fname__red      = list( reversed( svoistva_ot_fname__shabloni)) #само тези се запазват, в този ред

        @classmethod
        def ime_ot_prevod( klas, name ):
            names = [ name ]
            if   name.endswith('.bg'): names.append( name[:-3])
            elif name.endswith('.ru'): names.append( name[:-3])
            else:
                names.append( name+'.bg')
                names.append( name+'.ru')
            return info.ime_ot_prevod( *names)

        def samopopylva_etiketi( az):
            if az.etiketi.zvuk: return
            avtor = az.etiketi.avtor
            if not avtor: return
            r = avtor in az.zamestiteli_po_stoinost.zvuk
            if r:
                az.slaga_etiket( 'zvuk', avtor)
            #else:
            #    r = az.etiketi.avtor in ' '.join( az.avtori_en).split()
            #    if r: az.slaga_etiket( az.stoinosti.zvuk, az.stoinosti.en)
            return r

    film_info.main()

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prikazki import info, DictAttr

opts2 = DictAttr(
    bez     =   '0',
    yaml    =   True,
    sykr2dylgo = True,
    sykr    =   '../abbr',
    prevodi_meta=   '../meta_prevodi',
    mnogoredovi_etiketi =True,
    html_enc    =   'utf8',
    html_index  =   'aindex.tmp',

    tags_app    = 'eyed3',
    tags_enc    = 'utf8',
    tags_po_papki= 'e3.tags.spisyk',
    #tags_po_otdelno='e3.tags'

    spisyk_samo_papki = True,

    simvolni    = True,
    dveniva     = True,

#    debug='items',
    vnosa_e_obiknoven= True,
    davai =True,
    #zapis_opisi =True,
    html_papka = 'apapka.tmp',

)

if __name__ == '__main__':
    import sys
    info.main( opts2, sys.argv[1:] or ['.'] )

# vim:ts=4:sw=4:expandtab

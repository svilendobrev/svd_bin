#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prikazki import info, DictAttr

opts2 = DictAttr(
    yaml=   True,
    html_index= 'aaab',
    bez=    '0',
    simvolni= True,
    dve_niva= True,
    sykr=   '../abbr',
    prevodi_meta=   '../meta_prevodi',
#    debug='items',
    vnosa_e_obiknoven= True,
    davai =True,
)

if __name__ == '__main__':
    import sys
    info.main( opts2, sys.argv[1:] or ['.'] )

# vim:ts=4:sw=4:expandtab

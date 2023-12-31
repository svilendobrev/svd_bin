#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function #,unicode_literals

import sys, os.path
def opt( *xx):
    for x in xx:
        if x in sys.argv: return sys.argv.remove( x ) or True
    return None

html    = opt( '--html')
rename  = opt( '--rename')
doit    = opt( '-f')
assert not (html and rename)
'''
 <a href="./a mozhet bit vorona.mp3"> А может быть ворона</a>
 '''

href_l2c = opt( '--href-tx') and sys.argv[1]
if href_l2c:
    '''
    nebivalica-1-pet.mp3
    ->
    небивалица-1-пет.mp3
    '''
    tx = [ a.strip() for a in open( href_l2c ) if a.strip() ]
    divider = tx.index( '->' )
    tx_from = tx[ :divider ]
    tx_to   = tx[ 1+divider: ]
    assert len( tx_from) == len( tx_to), tx
    href_l2c = dict( zip( tx_from, tx_to ))

for l in sys.stdin:
    l = l.rstrip()
    if 'href' not in l or '.mp3' not in l:
        if html: print( l)
        continue
    spfx = 'href="'
    ssfx = '</a>'
    smid = '">'
    pfx,l = l.split( spfx)
    l,sfx = l.split( ssfx)
    href,text = (x.strip() for x in l.split( smid))
    pathhead,fname = os.path.split( href)
    if href_l2c:
        cyr = href_l2c[ fname ]
    else:
        cyr = text.lower(
            ).replace( 'ь', ''      #ru32->bg29
            ).replace( 'ы', 'и'
            ).replace( 'э', 'е'
            ).replace( ':', '-'     #FAT
            ).replace( '/', '-'     #fs
            ).replace( ' ', '_'
            )
    fname1 = href
    fname2 = os.path.join( *pathhead, cyr )
    _,ext = os.path.splitext( fname1)
    if not fname2.endswith( ext):
        fname2 += ext

    if rename:
        print( 'mv', fname1, fname2)
        if doit:
            if os.path.exists( fname1):
                os.rename( fname1, fname2)
                print( ' ++')
            else:
                print( ' --')
    elif html:
        e1 = e2 = ''
        if not os.path.exists( fname2):
            e1,e2 = '<!-- ',' -->'
        print( e1+ pfx+ spfx+ fname2+ smid+ ' '+ text+ ssfx+ sfx+ e2)
    else:
        print( cyr, '<-', href)

# vim:ts=4:sw=4:expandtab

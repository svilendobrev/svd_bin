#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,glob
join = os.path.join

try:
    from urllib import unquote_plus, unquote
except:
    from urllib.parse import unquote_plus, unquote

keepplus = 0
unquote = keepplus and unquote or unquote_plus

for a in sys.argv[1:] or glob.glob( os.path.expanduser( '~/.local/share/Trash/info/*nfo')):
    fpath = [ l.split('=',1)[-1] for l in open(a) if l.startswith('Path=') ][0].strip()
    fpath = unquote( fpath)
    #print( fpath)
    #continue
    delpath = join( os.path.dirname( fpath), 'del')
    os.makedirs( delpath, exist_ok= True)
    fname = os.path.basename( fpath)
    delfpath = join( delpath, fname)
    try:
        os.rename( fpath, delfpath)     #ако случайно е възкръснал ???
    except:
        tfname = os.path.basename(a).split('.trashinfo')[0]
        try:
            os.rename( join( os.path.dirname( a), '..', 'files', tfname), delfpath)
        except:
            print( '??', a)
            continue

    print( '> ', delfpath)
    os.rename( a, a+'.del')

# vim:ts=4:sw=4:expandtab

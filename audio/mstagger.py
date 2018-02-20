#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
''' read/write mp3 tags both ID3v2.3 and ID3v1
 read:  mstagger.py fname
 write: mstagger.py fname attr1=val attr2=val2 ...
'''
import stagger
from stagger.id3v1 import Tag1

stagger.Tag1._friendly_names = 'title artist album year comment genre track'.split()
all_names = stagger.Tag1._friendly_names + 'picture'.split()
_defaults= dict( genre=255, track=0)

encv1 = 'cp1251'

def write( fname, valuedict):
    if not isinstance( valuedict, dict):
        valuedict = dict( a.split('=',1) for a in valuedict )
    wrong = set(valuedict) - set(all_names)
    if wrong: print( '! wrong attrs', wrong, 'allowed:', *all_names)
    oknames = set(all_names) & set(valuedict)
    if oknames:
        for klas in stagger.Tag23, stagger.Tag1:
            t = klas()  #always empty
            for k in t._friendly_names:
                ik = 'year' if k == 'date' else k #v = v.split('-')[0]     #see Tag._friendly_date_string
                v = valuedict.get( ik)
                if v or klas is stagger.Tag1 :
                    setattr( t, k, v or _defaults.get( k,''))
            if klas is stagger.Tag1:
                t.write( fname, encoding= encv1)
            else:
                t.write( fname)

if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    valuedict = sys.argv[2:]

    if valuedict: write( fname, valuedict)

    class options: quiet = False

    print( fname)
    for reader in [ stagger.read_tag, lambda *a: stagger.Tag1.read( *a, encoding= encv1) ] :
        isv2 = reader is stagger.read_tag
        tag = None
        with stagger.util.print_warnings( fname, options):
            try:
                tag = reader(fname)
                ver = isv2 and '2.'+str(tag.version) or '1'
                print( f' :ID3v{ver} tags')
            except stagger.NoTagError:
                print( fname,  ": No tag", isv2 and 'v2' or 'v1', file=sys.stderr)
            except stagger.Error as e:
                print( fname,  ":error: " + ", ".join(e.args), file=sys.stderr)
            except EOFError:
                print( fname,  ":error: End of file while reading tag", file=sys.stderr)
        if not tag: continue

        with stagger.util.print_warnings( fname, options):
            for name in tag._friendly_names:
                val = getattr( tag, name.replace("-", "_"))
                if val: print( ' ', name.ljust(8), ':', val)
            sys.stderr.flush()
            sys.stdout.flush()


    #stagger.default_tag = stagger.Tag23
    #stagger.delete_tag( f)
    #Tag1.delete( f)
    #stagger.util.set_frames( f, valuedict)

# vim:ts=4:sw=4:expandtab

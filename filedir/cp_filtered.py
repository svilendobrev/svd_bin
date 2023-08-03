#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

from shutil import copy2, copytree
import os,errno

copyargs = {}
try: #use dirs_exist_ok, py 3.8+
    copytree( '', None, dirs_exist_ok =True)
except TypeError:
    #XXX HACK shutil.copytree
    _makedirs = os.makedirs
    def makedirs( *a,**ka):
        if 1:
            ka['exist_ok'] = True
            return _makedirs( *a,**ka)
        else:
            #see svd_util.osextra.makedirs... py<=3.4
            try:
                _makedirs( *a,**ka)#, exist_ok =True)
            except OSError as e:
                if e.errno != errno.EEXIST: raise
    os.makedirs = makedirs
except FileNotFoundError:
    copyargs.update( dirs_exist_ok = True)

try: #use ignore_dangling_symlinks, py 3.2+
    copytree( '', None, ignore_dangling_symlinks=True)
except TypeError: pass
except FileNotFoundError:
    copyargs.update( ignore_dangling_symlinks = True)

# docs-as-of-py3.9: shutil.copytree( src, dst,
#   symlinks=False,             #if True: copy symlinks as is
#   ignore=None,                #func to filter dir-list
#   copy_function=copy2,
#   ignore_dangling_symlinks=False,     #if True: dont error if symlinks = False and symlink is dangling
#   dirs_exist_ok=False         #if True: dont error if dir/s exists
#   )
#
#print( copyargs)

if __name__ == '__main__':
    #from svd_util import optz
    import optparse, sys
    class OptionParser( optparse.OptionParser):
        '--ab_c=--ab-c'
        def _match_long_opt( self, opt):
            return optparse.OptionParser._match_long_opt( self, opt.replace('_','-'))
    oparser = OptionParser()
    def optany( name, *short, **k):
        if sys.version_info[0]<3:
            h = k.pop( 'help', None)
            if h is not None:
                k['help'] = isinstance( h, unicode) and h or h.decode( 'utf8')
        return oparser.add_option( dest=name, *(list(short)+['--'+name.replace('_','-')] ), **k)
    def optbool( name, *short, **k):
        return optany( name, action='store_true', *short, **k)

    oparser.set_usage( '''%prog [options] from to
        patterns below are regexp.match over whole path, for example:
        - use .*/[^/]*xyz[^/]* or .*xyz[^/]* to match just filename having xyz
        - use .*xyz.* to match anything having xyz in path
        - use (?i:pattern..) for ignorecase
        '''.rstrip())
    optany( 'include', '-i', help= 'these-only, regexp.match over whole path' )
    optany( 'exclude', '-x', help= 'these-skip, regexp.match over whole path, before --include' )
    optbool( 'symlinks_dereference', '-L', help= 'dereference symlinks into files')
    optbool( 'verbose', '-v', help= 'print what is copied or not')
    optz,argz = oparser.parse_args()

    import re
    exclude = None
    if optz.exclude:
        print( 'excluding:', optz.exclude)
        exclude = re.compile( optz.exclude)
    include = None
    if optz.include:
        print( 'including:', optz.include)
        include = re.compile( optz.include)

    src,dst = argz[:2]
    if 1:
        def copy( src, dst, **ka):
            if exclude and exclude.match( src):
                if optz.verbose: print( 'excluded:', src)
                return
            if include and not include.match( src):
                if optz.verbose: print( 'not included:', src)
                return
            if optz.verbose: print( 'copy:', src, '>>', dst)
            return copy2( src, dst, **ka)
        copyargs.update( copy_function= copy)
    else:
        def ignore( dir,listdir):
            #TODO make proper exclude include here
            skipped = filter( dir, listdir) if filter else ()
            return skipped
        copyargs.update( ignore= ignore)

    copytree( src, dst, symlinks= not optz.symlinks_dereference, **copyargs)

# vim:ts=4:sw=4:expandtab

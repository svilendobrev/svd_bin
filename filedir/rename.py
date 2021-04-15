#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys,re,glob
def run( *parse_args):
    from svd_util import optz

    optz.bool( 'fake', '-n', help= 'do nothing')
    optz.bool( 'link', help= 'link instead of move/rename')
    optz.bool( 'lower', '-l', help= 'just lower-case, all args are filepaths, see --levels')
    optz.bool( 'upper', '-u', help= 'just upper-case, all args are filepaths, see --levels')
    optz.bool( 'space2under', help= 'whitespace-to-_, all args are filepaths, see --levels')
    optz.bool( 'under2space', help= '_-to-whitespace, all args are filepaths, see --levels')
    optz.bool( 's2u', help= 'space2under')
    optz.bool( 'u2s', help= 'under2space')
    optz.int(  'levels',    default=0, help= 'levels above leaf to rename lower/upper/_, default [%default]') #TODO only works for last-level-changes.. TODO apply to all renaming
    optz.str(  'movepath',  help= 'rename and move into')
    optz.str(  'command',   help= 'exec this with 2 args instead of os.rename/os.link')
    optz.bool( 'insymlink', help= 'rename inside symlinks (text it points to), ignore non-symlinks')
    optz.bool( 'outsymlink', help= 'if --insymlink, also rename/cmd actual symlinked-path')
    optz.bool( 'thesymlink', help= 'if --insymlink, also rename/cmd the symlink itself')
    optz.bool( 'symlink',   help= '--insymlink --outsymlink --thesymlink together')
    #optz.bool( 'filter',    help= 'additional filter for inside symlinks; action applies if this matches inside symlink')  mmm use instead find -lname ?
    optz.bool( 'abssymlink', help= 'change symlinks to point to abs-full-path, ignore non-symlinks')
    optz.bool( 'dirfiles', '-r', help= 'dir and then files inside') #?
    optz.bool( 'noerror',   help= 'skip errors')
    optz.bool( 'overwrite', '-f',   help= 'allow overwriting existing files')
    optz.bool( 'quiet', )
    optz.bool( 'verbose', '-v')
    optz.help( '''
    %prog [options] regexp subst filepaths
       subst can also use $1..$6 for groups
       if filepath is - , reads stdin, one filepath per line
       ! put -- before args if any filepath/regexp/subst starts with -
    %prog -u/-l [options] filepaths
    renu* [options] filepaths
    renl* [options] filepaths
    '''.strip() )
    optz,argz = optz.get( *parse_args)

    prg = os.path.basename( sys.argv[0] )
    if prg.startswith( 'renu'): optz.upper = True
    if prg.startswith( 'renl'): optz.lower = True
    if prg.startswith( 'ren_'): optz.space2under = True
    if optz.u2s: optz.under2space = True
    if optz.s2u: optz.space2under = True

    if   optz.upper:   func = lambda x: renul_( x, True,  optz.levels)
    elif optz.lower:   func = lambda x: renul_( x, False, optz.levels)
    elif optz.under2space: func = lambda x: renul_( x, '_2 ', optz.levels)
    elif optz.space2under: func = lambda x: renul_( x, ' 2_', optz.levels)
    elif optz.abssymlink:
        assert not optz.insymlink
        func = os.path.realpath
    else:
        regexp = argz.pop(0)
        subst  = argz.pop(0)
        for a in range(1,6):
           subst = subst.replace( '$'+str(a), '\\'+str(a))
        repl = re.compile( regexp)
        def func( x):
            return repl.sub( subst, x)
        if not optz.quiet: print( '#', repr(regexp), '=>', repr(subst))
    optz.func = func

    if optz.symlink:
        optz.insymlink = optz.thesymlink = optz.outsymlink = True
    if optz.insymlink and not optz.quiet:
        print( '# inside symlinks')

    if optz.fake or optz.verbose:
        print( '...', *argz)
    for a in argz:
        if a == '-':
            for f in sys.stdin:
                doit( f.strip(), optz)
            continue
        b = doit( a, optz)
        if optz.dirfiles:
            for f in glob.glob( b+'/*'):
                doit( f, optz)

###########

def renul_( x, up, levels =0):
    r = os.path.split( x)
    r0 = r[0]
    if levels>0: r0 = renul_( r0, up, levels-1)
    if up==' 2_': to = '_'.join( r[1].split())
    elif up=='_2 ': to = ' '.join( r[1].split('_'))
    else: to = r[1].upper() if up else r[1].lower()
    return os.path.join( r0, to)


_print = print
def print(*aa):
    _print( *(a.encode('utf8','ignore').decode('utf8') for a in aa))

def doit( a, optz):
    a = a.rstrip('/')
    a = a.replace('//','/')
    a = a.replace('//','/')
    if optz.movepath == a:
        print( '!ignore movepath target', a)
        return
    func = optz.func
    org = a
    orgb = org
    symlink = optz.insymlink or optz.abssymlink
    outsymlink = optz.outsymlink
    if symlink:
        if not os.path.islink( a):
            print( '!ignore non-symlink', a)
            return a
    if optz.insymlink:
        a = os.readlink( a )
    if optz.thesymlink:
        orgb = func( org)

    b = func(a)
    if optz.abssymlink:
        a = os.readlink( a )

    if optz.verbose: print( '?<', a, org)
    if optz.verbose: print( '?>', b, orgb)
    if b == a:
        if optz.thesymlink and orgb != org:
            symlink = False
            outsymlink = False
            a,b = org,orgb
        else: return b
    if optz.movepath:
        b = os.path.join( optz.movepath, b)

    if not optz.quiet or optz.fake:
        print( *( (org!=a) * [ org,'->', ] + [ a, ] ))
        print( ':>', *( (orgb!=a) * [ orgb,'->', ] + [ b ] ))
        if optz.insymlink and optz.outsymlink:
            print( ' ', a, )
            print( ' ', ':>', b )
    if optz.fake: return b

    renames = []
    if symlink:     #insymlink +/- thesymlink
        os.remove( org)
        os.symlink( b, orgb)
    if not symlink or outsymlink:
        renames += [ (a,b) ]
    if not symlink and optz.thesymlink:
        renames += [ (org,orgb) ]
    for a,b in renames:
    #if not symlink or optz.outsymlink or optz.thesymlink:
        if optz.command:
            import subprocess
            print( optz.command, a, b)
            subprocess.call( optz.command.split() + [ a, b] )
        else:
            if not os.path.exists( a):
                print( '!ignore inexisting', a)
                continue
            if os.path.exists( b) and not optz.overwrite:
                print( '!not overwriting', b)
            else:
                #print( optz.link and 'os.link' or 'os.rename', a, b)
                try:
                    (optz.link and os.link or os.rename)( a,b)
                except Exception as e:
                    if optz.noerror: print( '??', e )
                    else: raise
    return b

if __name__ == '__main__':
    run()

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys,re,glob
def run( *parse_args):
    from svd_util import optz

    optz.bool( 'fake', '-n', help= 'do nothing')
    optz.bool( 'once', '-1', help= 'sub-stitute once-only per filename')
    optz.bool( 'link', help= 'link instead of move/rename')
    optz.bool( 'symlink',   help= 'symlink instead of move/rename, be careful with output-name')
    optz.str(  'command',   help= 'exec this with 2 args instead of os.rename/os.link')
    optz.bool( 'lower', '-l', help= 'just lower-case, all args are filepaths, see --levels')
    optz.bool( 'upper', '-u', help= 'just upper-case, all args are filepaths, see --levels')
    optz.bool( 'mediate',     help= 'go through intermediate name, for FAT/ignorecase-filesystems')
    optz.bool( 'space2under', help= 'whitespace-to-_, all args are filepaths, see --levels')
    optz.bool( 'under2space', help= '_-to-whitespace, all args are filepaths, see --levels')
    optz.bool( 's2u', help= 'space2under')
    optz.bool( 'u2s', help= 'under2space')
    optz.bool( 'ignorecase', '-i',  help= 'ignore upper/lower case')
    optz.int(  'levels',    default=0, help= 'levels above leaf to rename lower/upper/_, default [%default]') #TODO only works for last-level-changes.. TODO apply to all renaming
    optz.bool( 'funcsubst', help= 'subst is a func to eval( m=match)')
    optz.str(  'movepath',  help= 'rename and move into')
    optz.bool( 'mkdirs',    '-p',   help= 'make missing dirs in target path')
    optz.bool( 'insymlink', help= 'rename inside symlinks (text it points to), ignore non-symlinks')
    optz.bool( 'outsymlink', help= 'if --insymlink, also rename/cmd actual symlinked-path')
    optz.bool( 'thesymlink', help= 'if --insymlink, also rename/cmd the symlink itself')
    optz.bool( 'allsymlink', help= '--insymlink --outsymlink --thesymlink together')
    #optz.bool( 'filter',    help= 'additional filter for inside symlinks; action applies if this matches inside symlink')  mmm use instead find -lname ?
    optz.bool( 'abssymlink', help= 'change symlinks to point to abs-full-path, ignore non-symlinks')
    optz.bool( 'dirfiles', '-r', help= 'dir and then files inside') #?
    optz.bool( 'noerror',   help= 'skip errors')
    optz.bool( 'overwrite', '-f',   help= 'allow overwriting existing files')
    optz.bool( 'delete_if_overwrite', '-d',   help= 'delete before overwriting existing files ; --symlink always does this if overwriting allowed, like ln -sf')
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
    elif optz.under2space: func = lambda x: renul_( x, '_2s', optz.levels)
    elif optz.space2under: func = lambda x: renul_( x, 's2_', optz.levels)
    elif optz.abssymlink:
        assert not optz.insymlink
        func = os.path.realpath
    else:
        regexp = argz.pop(0)
        subst  = argz.pop(0)
        if not optz.funcsubst:
            for a in range(0,9):
                subst = subst.replace( f'${a}', f'\\g<{a}>')
        repl = re.compile( regexp, **( dict( flags= re.IGNORECASE) if optz.ignorecase else {}))
        if not optz.quiet: print( '#', repr(regexp), '=>', repr(subst))
        if optz.funcsubst:
            evalsubst = subst
            def funcsubst( m):
                try:
                    return eval( evalsubst, dict( m=m), dict( m=m))
                except:
                    _print( '???', m.string, m.groups())
                    raise
            subst = funcsubst
        def func( x):
            return repl.sub( subst, x, count= bool( optz.once) )
    optz.func = func

    if optz.allsymlink:
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
    if up=='s2_': to = '_'.join( r[1].split())
    elif up=='_2s': to = ' '.join( r[1].split('_'))
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

    cmd = os.rename
    if optz.link: cmd = os.link
    elif optz.symlink: cmd = os.symlink

    for a,b in renames:
    #if not symlink or optz.outsymlink or optz.thesymlink:
        if optz.command:
            import subprocess
            print( optz.command, a, b)
            subprocess.call( optz.command.split() + [ a, b] )
        else:
            if not os.path.lexists( a):     #do not ignore broken symlinks
                print( '!ignore inexisting', a)
                continue
            if os.path.lexists( b):         #do not ignore broken symlinks
                if cmd == os.rename and  a.lower() == b.lower() and optz.mediate: # FAT: x==X, so x->x1->X
                    if not optz.quiet: print( ':: exists and mediated:', b)
                    b1 = b+str(os.getpid())
                    cmd( a, b1)
                    a = b1
                elif not optz.overwrite:
                    print( '!not overwriting', b)
                    continue
                elif optz.delete_if_overwrite or optz.symlink:
                    if not optz.quiet: print( ':: exists and removed:', b)
                    os.remove( b)

            bpdirs = os.path.split( b)[:-1]
            if bpdirs and optz.mkdirs:
                bpdir = os.path.join( *bpdirs)
                if not os.path.exists( bpdir):
                    os.makedirs( bpdir, exist_ok= True)
            #print( cmd, a, b)
            try:
                cmd( a,b)
            except Exception as e:
                if optz.noerror: print( '??', e )
                else: raise
    return b

if __name__ == '__main__':
    run()

# vim:ts=4:sw=4:expandtab

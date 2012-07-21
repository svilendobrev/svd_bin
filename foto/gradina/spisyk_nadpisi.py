#!/usr/bin/env python
# -*- coding: utf-8 -*-
#$Id$
import sys,os
import lat2cyr

def parse( fname_spisyk, verbose =False):
    '''format:
    img_2234.jpg	прякор вляво , име пълно вдясно
    #получава горните
    img_2235.jpg
    img_2393.jpg	само прякор
    img_2377.jpg	, само име пълно , filename
    '''

    spisyk = {}
    priakor = ime = oname_priakor = ''
    for a in file( fname_spisyk):
        a = a.strip()
        if not a or a.startswith('#'): continue
        l = a.split()
        if len( l ) > 1:
            a = ' '.join( l[1:] )
            r = a.split(',')
            if len(r) >= 2: ime = r[1]
            else: ime = ''

            oname_priakor = priakor = r[0]
            pp = priakor.split()
            if len(pp)>1: oname_priakor = pp[-1]
            if len(r) >2: oname_priakor = r[2]

        fname = l[0].strip()
        ime = ime.strip()
        priakor = priakor.strip()
        oname_priakor = oname_priakor.strip()
        oname = lat2cyr.zvuchene.cyr2lat( oname_priakor) + '_' + fname
        if verbose: print >>sys.stderr, ' :', fname, priakor, ime, ':', oname

        xfname = os.path.splitext( fname)[0]
        spisyk[ xfname] = oname,priakor,ime
    return spisyk

if __name__ == '__main__':
    import optz
    optz.add1( 'nothing', '-n', help= 'do nothing')
    optz.add1( 'force',   '-f', )
    optz.add1( 'verbose', '-v', )
    optz.add1( 'cjpeg', )
    optz.add1( 'stdin', )
    options,args = optz.get()

    fname_spisyk = args.pop(0)
    spisyk = parse( fname_spisyk, verbose= options.verbose)
    if options.nothing: raise SystemExit

    from nadpis1pil import label
    opath = 'nadpisi'

    for fname in args:
        xfdir,xfname = os.path.split( fname)
        yfname = os.path.splitext( xfname)[0]
        r = spisyk.get( yfname)
        if not r:
            print >>sys.stderr, 'unknown', yfname, fname
            continue
        oname,priakor,ime = r
        print >>sys.stderr, fname, priakor, ime, '>', oname
        tl,tr = (p.decode('cp1251') for p in (priakor,ime))

        try:
            os.symlink( xfname, os.path.join( xfdir, oname) )
        except Exception, e: print >>sys.stderr, 'symlink:', e

        if options.stdin:
            from StringIO import StringIO
            tmp = StringIO( sys.stdin.read() )
            out = label( tl,tr, src= tmp)
            out.save( sys.stdout, 'PPM')
            continue

        try: os.makedirs( opath)
        except: pass
        try:
            oname = os.path.join( opath, oname)
            onamep = oname+'.ppm'
            onamej = oname+'.jpeg'
            if os.access( onamej, os.F_OK):
                if options.force: print >>sys.stderr, '  overwrite existing', oname
                else:
                    print >>sys.stderr, '  skip existing', oname
                    continue
            out = tt( tl,tr, src=fname)
            out.save( onamep)
            #out.save( oname+'.jpg', 'JPEG', quality=90)#, progressive=True, optimize=True)
            if options.cjpeg:
                for l in ('''
                        cjpeg -q 90 -progressive %(onamep)s > %(onamej)s
                        jhead -te %(fname)s -dt %(onamej)s
                        '''.strip() % locals() ).split('\n'):
                    print >>sys.stderr, l
                    os.system( l)
        except Exception, e: print >>sys.stderr, e

# vim:ts=4:sw=4:expandtab

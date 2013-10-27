#!/usr/bin/env python
# sdobrev 2006-2008-2012
from __future__ import print_function
import sys
from util import optz
import uno

from unohelper import Base, systemPathToFileUrl, absolutize
from os import getcwd
from os.path import splitext
from com.sun.star.beans import PropertyValue
from com.sun.star.uno import Exception as UnoException
from com.sun.star.io import IOException, XOutputStream


class OutputStream( Base, XOutputStream ):
    def __init__( self ):
        self.closed = 0
    def closeOutput(self):
        self.closed = 1
    def writeBytes( self, seq ):
        sys.stdout.write( seq.value )
    def flush( self ):
        pass

class cfg:
    filters = {
        #filename-extension: filterName
        'txt':  'Text (Encoded)',
        'pdf':  'writer_pdf_Export',
        'html': 'HTML (StarWriter)',
        'csv':  'Text - txt - csv (StarCalc)',
        'doc97':  'MS Word 97',
    }
    connect = 'socket,host=localhost,port=2002'
    office  = 'soffice'

optz.text( 'filter',
    help= 'output filter type; one of: '
            + ' '.join( sorted( cfg.filters.keys())) + '; default: %default',
    choices= list( cfg.filters.keys()),
    default= 'txt',
    )
optz.text( 'filter2',
    help= 'output filter in direct OpenOffice notation, e.g. ' + str( cfg.filters.values())
            + '. has priority over --filter' )
optz.text( 'out',
    help= 'output file - only if single input; default: input.filtertype' )
optz.bool( 'stdout',    help= 'Redirect output to stdout. has priority over --out' )

optz.text( 'connect',
    help= 'The part of uno url needed to drive OpenOffice. default: %default',
    default= cfg.connect )
optz.bool( 'office',
    help= 'what to execute to start OpenOffice, default: %default',
    default= cfg.office )
optz.int( 'wait',
    help= 'seconds to wait when auto-starting OpenOffice (=%default)',
    default=5 )

connect2 = ';urp;StarOffice.ComponentContext'
cmd = '%(office)s "--accept=%(connect)s'+connect2+'"'

optz.epilog( '''\
save-as document to output format, or extracts text and prints it to stdout.
output-file is overwritten. default output-file is input.filtertype.
Requires a listening OpenOffice.org instance - or auto-starts one.
The script and OpenOffice must be able to access the input documents with same path.
To have a listening OpenOffice.org instance, run it like:
''' + cmd % cfg.__dict__
)


retVal = 0

opts,args = optz.get()
if not args:
    optz.oparser.error( 'at least one input file')

try:
    ctxLocal = uno.getComponentContext()
    resolver = ctxLocal.ServiceManager.createInstanceWithContext(
                    'com.sun.star.bridge.UnoUrlResolver', ctxLocal )
    url = 'uno:' + opts.connect + connect2
    try:
        ctx = resolver.resolve( url )
    except:
        import os
        cmd = cmd % opts.__dict__ + ' &'
        try:
            os.system( cmd)
            ctx = resolver.resolve( url)
        except:
            print >> sys.stderr, 'wait to start: ', cmd
            import time
            time.sleep( opts.wait)
            ctx = resolver.resolve( url)

    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext( 'com.sun.star.frame.Desktop', ctx )

    filt = opts.filter2 or cfg.filters[ opts.filter]
    cwd = systemPathToFileUrl( getcwd() )
    outProps = (
        PropertyValue( 'FilterName' , 0, filt, 0 ),
        PropertyValue( 'Overwrite' , 0, True , 0 ),
        PropertyValue( 'OutputStream', 0, OutputStream(), 0)
    )

    inProps = PropertyValue( 'Hidden' , 0 , True, 0 ),
    for path in args:
        try:
            fileUrl = absolutize( cwd, systemPathToFileUrl( path) )
            doc = desktop.loadComponentFromURL( fileUrl, '_blank', 0, inProps )

            if not doc:
                raise UnoException( 'Could not open stream for unknown reason', None )

            if not opts.stdout:
                out = len(args)==1 and opts.out or path + '.' + (opts.filter2 or opts.filter)
                destUrl = absolutize( cwd, systemPathToFileUrl( out) )
                print( destUrl, file= sys.stderr)
                doc.storeToURL( destUrl, outProps)
            else:
                doc.storeToURL( 'private:stream',outProps)
        except IOException as e:
            print( 'Error during conversion of %(path)s:' % locals(), e.Message, file= sys.stderr)
            retVal = 1
        except UnoException as e:
            print( 'Error ('+repr(e.__class__)+') during conversion of %(path)s:' % locals(), e.Message, file= sys.stderr)
            retVal = 1
        if doc:
            doc.dispose()

except UnoException as e:
    print >> sys.stderr, 'Error ('+repr(e.__class__)+') :' + e.Message
    retVal = 1

raise SystemExit( retVal)
# vim:ts=4:sw=4:expandtab

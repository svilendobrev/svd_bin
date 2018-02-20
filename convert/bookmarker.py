#!/usr/bin/env python3
#$Id: opera-adr-sort.py,v 1.2 2007-01-04 14:19:00 sdobrev Exp $
# opera-adr-parser

def escape( x):
    return x.replace( '\\', '\\\\'
            ).replace( "'", "\\'"
            ).replace( '\n', '\\n'
            ).replace( '\t', '\\t'
            ).replace( '\r', '\\r'
            )

from svd_util import lat2cyr
l2c = lat2cyr.zvuchene.lat2cyr

def h(x):  return '<'+x+'>'
def h_(x): return '</'+x+'>'
def hh(x,y): return h(x) + y + h_(x)

import json

class Node:
    ATTRS = 'NAME URL UNIQUEID trash'.split()
    def __init__( me, parent =None, NAME =None, URL =None, items =None, bgNAME =None, UNIQUEID =None, trash =False):
        me.parent = parent
        if parent and not parent.trash: parent.items.append( me)
        if bgNAME: NAME = l2c( bgNAME)#.decode('utf8') )
        #elif NAME: NAME = NAME.decode('utf8')
        me.NAME = NAME
        me.URL = URL
        me.UNIQUEID = UNIQUEID
        me.items = items or []
        me.trash = trash
        for i in me.items: i.parent = me

    def fixparent( me):
        for i in me.items:
            i.parent = me
            i.fixparent()

    def empty( me): return not me.NAME and not me.URL

    def __str__( me ):
        if me.URL:
            r = '%(URL)s, NAME=%(NAME)s'
        else:
            r = 'folder: NAME=%(NAME)s'
        #if me.parent: r+= ', parent=%(parent)r'
        return r % me.__dict__
    def __repr__( me):
        r = str(id(me)) #'' #not me.URL and 'folder: ' or ''
        if me.URL:  r+= ' URL=%(URL)s,'
        if me.NAME: r+= ' NAME=%(NAME)s,'
        if me.parent: r+= ' parent='+str(id(me.parent))
        return r % me.__dict__

    def find( me, names =()):
        if not names: return me
        #if me.NAME == names[0]: return me.find( names[1:])
        for i in me.items:
            if i.NAME == names[0]:
                return i.find( names[1:])
            #r = i.find( name)
            #if r: return r

    def sort( me, **k):
        if not me.items: return
        me.items.sort( **k)
        for i in me.items:
            i.sort( **k)


    class dumper:
        indent = 2
        def __init__( me, **kargs):
            me.__dict__.update( kargs)
        def enter( me, o, pfx):
            if o.items: print()
            print( pfx + str( o))
        def leave( me, o, pfx): pass

    class htmler:
        indent = 2
        ITEM    = 'li'
        FOLDER  = 'ul'
        FOLDNAME= 'b'
        def __init__( me, rootname =None):
            me.rootname = rootname
            me.on = False
            print( '''\
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<title>bookmarks</title>
<h1>bookmarks</h1>
''')
        def prefolder( me): return h_( me.ITEM) +'\n'

        def enter( me, o, pfx):
            if not me.on:
                if not me.rootname or me.rootname == o.NAME:
                    me.on = True
            if o.URL:
                if me.on: print( pfx+ h( me.ITEM),
                        h('a href="'+o.URL+'"') , o.NAME,
                        #':', o.URL,
                        h_('a') )
            elif o.NAME and o.items:    #no empty folders
                prefolder = me.prefolder()
                if me.on:
                    if prefolder.endswith( '\n'):
                        print( pfx+ prefolder.strip())
                        prefolder = ''
                    print( pfx+ prefolder+ hh( me.FOLDNAME, o.NAME ) )
            if o.items:
                if me.on: print( pfx+ h( me.FOLDER) )
        def leave( me, o, pfx):
            #if not o.URL:
            if o.items:
                if me.on: print( pfx+ h_( me.FOLDER) )
            #else:
            #    print( pfx , h_('li') )
            if me.on and me.rootname and me.rootname == o.NAME:
                me.on = False

    def dump( me, level=0, dumper =None ):
        if not dumper: dumper = me.dumper()
        pfx = max(0,level)*' '*dumper.indent
        dumper.enter( me, pfx)
        level+=1
        for i in me.items:
            i.dump( level, dumper=dumper)
        level-=1
        dumper.leave( me, pfx)

    class pydumper( dumper):
        indent = 2
        def enter( d, me, pfx):
            if me.items: print()
            r = 'dict('
            for a in me.ATTRS:
                v = getattr( me, a, None)
                if v:
                    if a == 'trash': v = 'True'
                    else: v = "'"+ escape( v) +"'"
                    r += ' {a}= {v},'.format( **locals())
            print( pfx + r, end=' ')
            if me.items: print( 'items=[')
        def leave( d, me, pfx):
            if me.items: print( pfx+']', end=' ')
            print( ')'+ (me.parent and ',' or ''))

    def py( me):
        print( '# -*- coding: utf-8 -*-')
        return me.dump( dumper= me.pydumper() )

class json_opera:
    @staticmethod
    def userRoot( io): return io['roots']['custom_root']['userRoot']

    @classmethod
    def save( klas, rootnode, notrash =False, subst_in_iofilename =None, rootpath =(), sortkey =None):
        nodeinfo = dict(
                    meta_info= dict( layoutMode= '1',), #lines-of-text-view
                    )
        def operajson( node, is_root =False):
            if not is_root:
                assert node.NAME, node
            else:
                assert not node.NAME, node
            url = node.URL
            r = dict(
                    #date_added   = "13152369808004368",
                    #date_modified= "13152806511366460",
                    name= node.NAME,
                    type= 'folder' if not url else 'url',
                    **nodeinfo
            )
            if node.UNIQUEID: r.update( id  = node.UNIQUEID)
            if url: r.update( url= url)
            else:   r.update( children= [ operajson( i) for i in node.items if i.NAME.lower() != 'trash' or not notrash] )
            return r
        jtree = operajson( rootnode, is_root= True)
        children = jtree['children']
        #jtree.update( name = "All bookmarks",)
        #import pprint
        #pprint.pprint( jtree)
        if not subst_in_iofilename:
            print( json.dumps( children, indent=4, ensure_ascii=False))
        else:
            with open( subst_in_iofilename, encoding='utf-8') as fi:
                io = json.load( fi)

            rt = klas.userRoot( io)
            rt.setdefault( 'name', 'useRoot')
            for p in rootpath:
                cc = rt['children']
                for c in cc:
                    if c['name'] == p:
                        rt = c
                        break
                else:   #not found
                    rt = dict( name= p, type='folder', children=[], **nodeinfo)
                    cc.append( rt )
            rt['children'] = children
            #rint( json.dumps( i, sort_keys=0*True, indent=4))
            with open( subst_in_iofilename, 'w', encoding='utf-8') as fo:
                json.dump( io, fo, indent=4, ensure_ascii=False, sort_keys=True)

    @classmethod
    def load( klas, itext):
        io = json.loads( itext)
        userRoot = klas.userRoot( io)
        def operajson( node, is_root =False):
            return Node(
                NAME= node[ 'name'].strip(),
                URL = (node.get( 'url') or '').strip(),
                UNIQUEID = (node.get('id') or '').strip(),
                items = [ operajson( c) for c in node.get( 'children', ()) ]
                )
        r = operajson( userRoot, is_root=True)
        r.NAME = r.URL = r.UNIQUEID = None
        return r

class dldt_html_firefox:
    @classmethod
    def load( klas, itext):
        # e = lxml.html.fromstring( itext) ... is broken; gets only first dt in dt dt dt series; puts dl after dt instead of inside dt..
        import html5lib
        e = html5lib.parse( itext, namespaceHTMLElements=False)
        uroot = e.find('body')
        def findall_direct_dl_dt(node): return node.findall( 'dl/dt')
        def find_direct(node, x): return node.find( x)
        def attrib(node): return node.attrib

        import sys
        def dldt( node, l=1, root =False):
            #print( l*'  ', 3333, node)#list(node))
            if not root:
                a = find_direct( node, 'a')
                aa = a is not None
                h3 = find_direct( node, 'h3')
                NAME= a.text if aa else (h3.text if h3 is not None else None)
                if not NAME:
                    print( '????? name=', NAME, ':', node.tag, [(x.tag,x.attrib) for x in node ], file= sys.stderr)
                    NAME='?'
            return Node(
                NAME= None if root else NAME.strip(),
                URL = None if root else (attrib(a)['href'].strip() if aa else ''),
                UNIQUEID = None if root else (attrib(a).get('id','').strip() if aa else ''),
                items = [ dldt( c,l+1) for c in findall_direct_dl_dt( node) ]
                )
        return dldt( uroot, root= True)

    class dldthtmler( Node.htmler):
        indent = 2*2
        ITEM    = 'dt'
        FOLDER  = 'dl'
        FOLDNAME= 'H3'  #UPPER!
        def prefolder( me): return h( me.ITEM)
    @classmethod
    def save( klas, rootnode, options):
        rootnode.dump( dumper= klas.dldthtmler())

class json_firefox:
    @staticmethod
    def userRoot( io):
        for c in io['children']:
            if c['root'] == 'bookmarksMenuFolder':
                return c
    @classmethod
    def load( klas, jsonlz4_binary):
        b = jsonlz4_binary
        assert b[:8] == b'mozLz40\0', b[:8]
        import lz4
        jsn = lz4.block.decompress( b[8:])
        io = json.loads( jsn)
        userRoot = klas.userRoot( io)
        def ffoxjson( node, is_root =False):
            return Node(
                NAME= node[ 'title'].strip(),
                URL = (node.get( 'uri') or '').strip(),
                UNIQUEID = str( node.get('id') or ''),
                items = [ ffoxjson( c) for c in node.get( 'children', ()) ]
                )
        r = ffoxjson( userRoot, is_root=True)
        r.NAME = r.URL = r.UNIQUEID = None
        return r


def key4tree(x): return x.NAME #getattr( x, 'URL', '')
def key4flat(x): return x.URL, x.NAME
def key4tree4folder_last(x):  return (not x.URL, x.NAME.lower())
def key4tree4folder_first(x): return (bool(x.URL), x.NAME.lower())

formats = 'python html adr_opera dldt_html_firefox json_opera lz4json_firefox'.split()
#opera-htmlexport = firefox = netscape
def fullmap( names, **aliases):
    oo = dict( (f,f) for f in names)    #with aliases
    for v in aliases.values():
        assert v in oo, v
    oo.update( aliases)
    fmts = list( oo)
    for i in range(1,5):
        for f in fmts:
            k = f[:i]
            if k in oo: assert oo[k] == f, (f,oo[k])
            else: oo[k] = f
        #oo.update( (f[:i],f) for f in fmts)
    return oo

iformats = formats
oformats = formats + 'text'.split()
ifmts = fullmap( iformats)
ofmts = fullmap( oformats)

from svd_util import optz
optz.usage( '%prog [options] files')
optz.str( 'input',  default='python', type='choice', choices = list(ifmts), help= f'input format [%default]: {", ".join(iformats)} ; initial letters also work')
optz.str( 'output', default ='html',  type='choice', choices = list(ofmts) + 'text'.split(), help= f'output format [%default]: {", ".join(oformats)} ; initial letters also work')
optz.str( 'subst_in',   help= 'file to put the output substituting some part (what/where depends on output-type, i.e. json_opera)')
optz.bool( 'flat' , help= 'dump')
#optz.bool( 'html',  help= 'out=.html')
#optz.bool( 'adr',   help= 'out=.adr')
#optz.bool( 'netscape',   help= 'out=.html, netscape/firefox/opera export dl/dt style')
optz.text( 'rootiname',  help= 'root = in[ /from/here ]')
optz.text( 'rootoname',  help= 'out[ /to/there ] = root')
optz.text( 'skip',   help= 'path/to/skip')
optz.bool( 'nounique',  help= 'ignore UNIQUEID' )
optz.bool( 'align',     help= '(for out=.adr)')
optz.bool( 'notrash',   help= 'ignore trash (for out=.adr)' )
optz.bool( 'nosort',    help= 'dont sort items' )
options,args = optz.get()

if options.nounique:
    Node.ATTRS.remove( 'UNIQUEID')
#from svd_util.eutf import readlines

options.output = ofmts[ options.output ]
options.input  = ifmts[ options.input ]

def rootpath2list( rootpath): return [ a for a in (rootpath or '').split('/') if a]


class io:
    class python:
        @staticmethod
        def load( r): return eval( r, dict(dict=Node) )
        @staticmethod
        def save( root, options): root.py()
    if 0:
        class adr_opera:
            import opera_adr
            @classmethod
            def load( klas, r): return klas.opera_adr.parse_adr( r, Node)
            @classmethod
            def save( klas, root, options):
                klas.opera_adr.adr_opera( root, align= options.align, notrash= options.notrash )
    class json_opera( json_opera):
        @classmethod
        def save( klas, root, options):
            root.sort( key= key4tree4folder_first)
            super().save( root, notrash= options.notrash,
                                subst_in_iofilename= options.subst_in,
                                rootpath= rootpath2list( options.rootoname),
                                )
    dldt_html_firefox = dldt_html_firefox
    class lz4json_firefox( json_firefox):
        @staticmethod
        def read( fname): return open( a, 'rb').read()
    class html:
        @staticmethod
        def save( root, options):
            root.dump( dumper= Node.htmler())
    class text:
        @staticmethod
        def save( root, options):
            if options.flat:
                root.allitems.sort( key=key4flat)
                for i in root.allitems:
                    print( repr(i))
            else:
                root.dump()

def reader( fname):
    return open( fname, encoding='utf-8').read().strip()

#inp = codecs.getreader('utf-8')
for a in args:
    #r = '\n'.join( readlines( open( a )))

    i = getattr( io, options.input )
    reader = getattr( i, 'read', reader)
    r = reader( a)
    root = i.load(r)

    root.fixparent()
    if not options.nosort:
        root.sort( key=key4tree4folder_last)

    if options.rootiname:
        root = root.find( rootpath2list( options.rootiname)) or Node()
        #print( root , root.NAME)

    if options.skip:
        skip = root.find( rootpath2list( options.skip))
        if skip:
            #print( 2222, skip.NAME, repr(skip.parent))
            skip.parent.items.remove( skip)
        else: print( 'cannot find+skip', options.skip)

    o = getattr( io, options.output )
    o.save( root, options)

# vim:ts=4:sw=4:expandtab

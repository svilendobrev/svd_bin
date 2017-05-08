#!/usr/bin/env python3
#$Id: opera-adr-sort.py,v 1.2 2007-01-04 14:19:00 sdobrev Exp $
# opera-adr-parser

ATTRS = 'NAME URL UNIQUEID trash'.split()
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

class Node:
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
        def __init__( me, rootname =None):
            me.rootname = rootname
            me.on = False
        def enter( me, o, pfx):
            if not me.on:
                if not me.rootname or me.rootname == o.NAME:
                    me.on = True
            if o.URL:
                if me.on: print( pfx, h('li'), h('a href="'+o.URL+'"') , o.NAME,
                        #':', o.URL,
                        h_('a') )
            elif o.NAME and o.items:    #no empty folders
                if me.on: print( pfx , h_('li') )
                if me.on: print( pfx + hh( 'b', o.NAME ) )
            if o.items:
                if me.on: print( pfx + h('ul') )
        def leave( me, o, pfx):
            #if not o.URL:
            if o.items:
                if me.on: print( pfx + h_('ul') )
            #else:
            #    print( pfx , h_('li') )
            if me.on and me.rootname and me.rootname == o.NAME:
                me.on = False

    def find( me, name =None):
        if not name or me.NAME == name: return me
        for i in me.items:
            r = i.find( name)
            if r: return r

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
            for a in ATTRS:
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
        return me.dump( dumper= me.pydumper() )

    class operadumper( dumper):
        indent  = 4
        align   = False
        notrash = False
        def enter( d, me, pfx):
            if me.trash and d.notrash: return
            r = []
            if me.URL:
                r += ['#URL']
            elif me.parent:
                r += ['#FOLDER']
            subpfx = (d.align and d.indent or 1 ) * ' '
            for a in ATTRS:
                v = getattr( me, a, None)
                if v:
                    if a == 'trash': a,v = 'TRASH FOLDER','YES'
                    r.append( subpfx+a+'='+ v)
            #    r += [ subpfx+'TRASH FOLDER=YES', subpfx+'DELETABLE=NO' ]
            for p in r: print( pfx + p)
        def leave( d, me, pfx):
            if me.trash and d.notrash: return
            subpfx = (d.align and d.indent or 0 ) * ' '
            if not me.URL and me.parent:
                print( pfx+subpfx+'-')

    def opera( me, align =False, notrash =False):
        print( '''\
Opera Hotlist version 2.0
Options: encoding = utf8, version=3
''')
        return me.dump( dumper= me.operadumper( align= align), level=-1 )

    def sort( me, **k):
        if not me.items: return
        me.items.sort( **k)
        for i in me.items:
            i.sort( **k)

    def http( me):
        ht = 'http://'
        if k == 'URL' and v.startswith( ht):
            v = v[len(ht):]

import re
def parse( r):
    header = None
    allitems = []
    parent = root = Node( parent=None, )
    root.allitems = allitems
    level = 1
    for i in re.split( '\n *#', r):
        if not header:
            header = i
            continue
        ll = level
        item = Node( parent=parent)
        for l in i.split('\n'):
            l = l.strip()
            if not l: continue
            if l == '-':
                level -=1
                parent = parent.parent
                continue
            kv = l.split('=',1)
            v = kv[-1].strip()
            if len(kv)==1:
                k='typ'
                if v == 'FOLDER':
                    level+=1
                    parent = item
                    v = v.lower()   #go behind URL
                    continue
            else:
                k = kv[0].strip()
            if k =='TRASH FOLDER':
                item.trash = True
                continue
            if k in ATTRS:
                #v = v.decode('utf-8').encode('cp1251','replace')
                setattr( item, k, v )

        if item.empty():    #item.trash or
            if item.parent:
                try:
                    item.parent.items.remove( item)
                except: pass
        else:
            allitems.append( item)
    return root


def key4tree(x): return x.NAME #getattr( x, 'URL', '')
def key4flat(x): return x.URL, x.NAME


from svd_util import optz
optz.usage( '%prog [options] files')
optz.bool( 'o2py' , help= 'in=.adr out=python')
optz.bool( 'py2o' , help= 'in=python out=.adr')
optz.bool( 'ipy'  , help= 'in=python')
optz.bool( 'flat' , help= 'dump')
optz.bool( 'html',  help= 'out=html')
optz.text( 'root',  help= 'root from here')
optz.bool( 'nounique',  help= 'ignore UNIQUEID' )
optz.bool( 'align',     help= '(for out=.adr)')
optz.bool( 'notrash',   help= 'ignore trash (for out=.adr)' )
options,args = optz.get()

if options.nounique:
    ATTRS.remove( 'UNIQUEID')
#from svd_util.eutf import readlines

#inp = codecs.getreader('utf-8')
for a in args:
    #r = '\n'.join( readlines( open( a )))
    r = open( a, encoding='utf-8').read().strip()

    if options.ipy or options.py2o:
        root = eval( r, dict(dict=Node) )
    else:
        root = parse( r)

    root.sort( key=key4tree)

    if options.root:
        root = root.find( options.root) or Node()
        #print( root , root.NAME)

    if options.py2o:
        root.opera( align= options.align, notrash= options.notrash )
        continue
    if options.html:
        root.dump( dumper= Node.htmler())
        continue

    if options.o2py:
        print( '# -*- coding: utf-8 -*-')
        root.py()

    elif options.flat:
        root.allitems.sort( key=key4flat)
        for i in root.allitems:
            print( repr(i))

    else:
        root.dump()

# vim:ts=4:sw=4:expandtab

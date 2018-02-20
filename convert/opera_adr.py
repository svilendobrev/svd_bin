#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

#from bookmarker import Node

import re
def parse_adr( r, Node):
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
            if k in Node.ATTRS:
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

def adr_opera( rootnode, align =False, notrash =False):
    Node = rootnode.__class__
    class opera_adr_dumper( Node.dumper):
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
            for a in me.ATTRS:
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

    print( '''\
Opera Hotlist version 2.0
Options: encoding = utf8, version=3
''')
    return rootnode.dump( dumper= opera_adr_dumper( align= align), level=-1 )


# vim:ts=4:sw=4:expandtab

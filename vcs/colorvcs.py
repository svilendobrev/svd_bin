#!/usr/bin/env python
from __future__ import print_function
qrint = print
##for python 2.4:
##import sys #has no print_function, print/exec are operators, cannot catch SyntaxError
##def qrint(*a): sys.stdout.write( ' '.join(a)+'\n' )

import re

#colors
black,red,green,brown, blue,magenta,cyan,white = range(8)
bright = 100
yellow = brown+bright
gray   = black+bright   #! highlighting such text on black background is invisible

#categories
(
 update,
 modified,
 conflict,
 merge,
 add,

 delete,
 unknown,
 ignored,
 error,
 replace,
 external,
 other,

 diff_add,
 diff_del,
 diff_file,
 diff_chunk,
) = range(1,17)
rename = replace


#category -> color
colors = {
 update  : green,
 modified: red,
 conflict: yellow,
 merge   : blue +bright,
 add     : cyan,
 delete  : magenta,
 unknown : blue,
 ignored : blue,
 error   : yellow,
 other   : white,
 external: brown,
 replace : green +bright,
 diff_add: green,
 diff_del: red,
 diff_file: white+bright,
 diff_chunk: yellow,
}

class Colorer:
    all = {}
    def __init__( me, name, regexp, table, whole =False):
        me.all[ name ] = me
        me.regexp = re.compile( regexp)
        me.table = table
        me.whole = whole
        me.name = name
    def alias( me, name ): me.all[ name] = me
    def check( me, line):
        status = None
        m = me.regexp.match( line)
        if m:
            #qrint( `m.group(1)`, me.name)
            g = m.group(1)
            if me.whole:
                status = me.table.get( g )
            else:
                for c in g:
                    status = me.table.get( c)
                    if status: break
        return status

class Chain( Colorer):
    def __init__( me, name, *colorers):
        me.all[ name ] = me
        me.colorers = colorers
    def check( me, line):
        status = None
        for c in me.colorers:
            status = c.check(l)
            if status: break
        return status


Colorer( 'svn', r'^([ A-Z?!~]{2}) +\S+', {
#update
 'U': update
,'C': conflict
,'G': merge
#status
,'M': modified
,'A': add
,'R': replace
,'D': delete
,'I': ignored
,'X': external
,'?': unknown
,'!': error #missing/incomplete
,'~': error #obstructed
})

Colorer( 'cvs', r'^(\S) \S+', {
#update
 'P': update    #patch
,'U': update
,'C': conflict
,'N': add     #new   #import
,'L': ignored #link  #import
#status
,'M': modified
,'A': add
,'R': delete
,'I': ignored
,'?': unknown

#,'server':  reset
,'warning': bright+cyan
})


Colorer( 'diffC', '^(diff|Only|[<>])', {
     #'Index': diff_file,
     'diff': diff_file,
     'Only': diff_file,
     '>': diff_add,
     '<': diff_del,
}, whole=True ).alias( 'diff')

Colorer( 'diffU', '^([-+@=])', {    #only 1st char matters: allows for things like adding line starting with +++, or @
     '=': diff_file,
     '+': diff_add,
     '-': diff_del,
     '@': diff_chunk,
}, whole=True )

bzru = Colorer( 'bzrupd', r'^([- A-Z?+*]{1,3}) +\S+', {
#update
#Column 1 - versioning/renames:
 '+': add       #File versioned
,'-': other     #File unversioned
,'R': rename    #File renamed
,'?': unknown   #File unknown
,'C': conflict  #File has conflicts
,'P': other     #Entry for a pending merge (not a file)
#Column 2 - contents:
,'N': add       #File created
,'D': delete    #File deleted
,'K': other     #File kind changed
,'M': modified  #File modified
#Column 3 - execute:
,'*': other     #The execute bit was changed
# ignored ?
})

bzrs = Colorer( 'bzrstat', r'^(\w+):', {
#status???
 'added':    add
,'modified': modified
,'renamed':  rename
,'removed':  delete
,'unknown':  unknown
,'conflicts': conflict
#...
}, whole=True )

Chain( 'bzr', bzru, bzrs)


hgs = Colorer( 'hgstat', r'^(\S) \S+', {
 'A': add
,'M': modified
,'R':  delete
,'?':  unknown
,'I': ignored
#?? rename? conflict ?
#  C = clean
#  ! = deleted, but still tracked
#...
}#, whole=True
)

hgresolv = Colorer( 'hgresolv', r'^(\S) \S+', {
 'U': conflict
#,'R': resolved     #hg is bullshit
})

Chain( 'hg', hgs, hgresolv)


gitstat = Colorer( 'git', r'^([ A-Z?!]{1,2}) +\S+', {
#see git help status
#Column 1 - there, Column2: here
 '?': unknown   #File unknown
,'M': modified  #File modified
,'A': add       #File created
,'D': delete    #File deleted
,'R': rename    #File renamed
# ignored ?
})

###

ESC = chr(27)
def CLR(fg, bg =0, hi=0):
    'see colortable8x16.py'
    if fg is None: fg=0
    else:
        fg += 30
        bg += 40
    return ESC+'[%(hi)d;%(fg)d;%(bg)dm' % locals()

def clr(fg):
    hi=0
    if fg is not None:
        hi = fg>=bright
        if hi: fg-=bright
    return CLR( fg, hi=hi)


import sys
colorer = None
if sys.argv[1:]:
    colorer = Colorer.all.get( sys.argv[1] )
    if not colorer:
        qrint( 'opa!', sys.argv[0], ': unknown type', repr( sys.argv[1]))
else: #if not colorer:
    ks = list( Colorer.all.keys()); ks.sort()
    qrint( '''\
usage: colorvcs.py <type>
    filters stdin to stdout
    <type> can be:''', ' '.join( ks)
    )

    raise SystemExit( 1)

for l in sys.stdin:
    l = l.rstrip()
    status = colorer and l.strip() and colorer.check( l)
    if status:
        qrint( clr( colors.get( status) ) + l + clr( None))
    else: qrint( l)
#qrint( clr(None),'===')

# vim:ts=4:sw=4:expandtab

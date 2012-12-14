#!/usr/bin/env python2
#$Id: dircolor.py,v 1.2 2007-03-02 17:30:28 sdobrev Exp $

help = '''
 generates ls colorization:
    -ls         straight LS_COLORS (ignored TERMs); e.g.
                 $ export LS_COLORS=`dircolor.py -ls`
    -dircolors  make dircolors format; e.g.
                 $ dircolor.py -dircolors > _tmp; dircolors _tmp
    -dosexe     colorize dos-executables extensions as executables

 edit it and put your preferences in TERMs,TYPEs,SUFFIXEs.
 SUFFIXEs are classified in groups (of same attribute):
    '''

# a TERM entry for each termtype that is colorizable
TERMs = '''
linux
linux-c
mach-color
console
con132x25
con132x30
con132x43
con132x60
con80x25
con80x28
con80x30
con80x43
con80x50
con80x60
cygwin
dtterm
putty
xterm
xterm-color
xterm-debian
rxvt
screen
screen-bce
screen-w
vt100
Eterm

konsole
konsole-16
'''


# Below are the color init strings for the basic file types. A color init
# string consists of one or more of the following numeric codes:
# Attribute codes:
# 00=none 01=bold 04=underscore 05=blink 07=reverse 08=concealed
# Text color codes:
# 30=black 31=red 32=green 33=yellow 34=blue 35=magenta 36=cyan 37=white
# Background color codes:
# 40=black 41=red 42=green 43=yellow 44=blue 45=magenta 46=cyan 47=white

class COLORs:   #do not touch these
    Attributes = dict(
        none=0, bold=1, underscore=4, blink=5, reverse=7, concealed=8,
    )
    Text_colors = dict(
        black=30, red=31, green=32, yellow=33, blue=34, magenta=35, cyan=36, white=37,
    )
    Background_colors = dict(
        black=40, red=41, green=42, yellow=43, blue=44, magenta=45, cyan=46, white=47,
    )

for a in (COLORs.Attributes, COLORs.Text_colors):
    exec '; '.join( [ '%s=%s' % kv for kv in a.iteritems() ] )
a = COLORs.Background_colors
exec '; '.join( [ 'bg_%s=%s' % kv for kv in a.iteritems() ] )



class TYPEs:
    NORMAL  = 'no',none                 #00 # global default, although everything should be something.
    FILE    = 'fi',none                 #00 # normal file
    DIR     = 'di',blue,bold            #01;34 # directory
    LINK    = 'ln',cyan,bold            #01;36 # symbolic link. (If you set this to 'target' instead of a
                                            # numerical value, the color is as for the file pointed to.)
    FIFO    = 'pi',yellow               #40;33 # pipe
    SOCK    = 'so',magenta,bold         #01;35 # socket
    DOOR    = 'do',SOCK                 #01;35 # door
    BLK     = 'bd',yellow,bold          #40;33;01 # block device driver
    CHR     = 'cd',yellow,bold          #40;33;01 # character device driver
    ORPHAN  = 'or',red,bold             #40;31;01 # symlink to nonexistent file
    SETUID  = 'su',white,bg_red         #37;41 # file that is setuid (u+s)
    SETGID  = 'sg',black,bg_yellow      #30;43 # file that is setgid (g+s)
    STICKY_OTHER_WRITABLE = 'tw',DIR    #30;42 # dir that is sticky and other-writable (+t,o+w)
    OTHER_WRITABLE = 'ow',DIR           #34;42 # dir that is other-writable (o+w) and not sticky
    STICKY  = 'st',DIR,bg_green         #37;44 # dir with the sticky bit set (+t) and not other-writable
    EXEC    = 'ex',green                #01;32 # files with execute permission



class SUFFIXEs:
    DOS_EXEC = '''
cmd
exe
com
btm
bat
''', TYPEs.EXEC

    # archives or compressed
    ARCHIVE = '''
tar
tgz
tbz
arj
taz
lzh
zip
rar
z
Z
7z
gz
bz2
deb
rpm
jar
apk
egg
pk3
''', red

    # image formats
    IMAGE = '''
bmp
gif
jpeg
jpg
pbm
pgm
png
pnm
ppm
tga
tif
tiff
xbm
xpm

raw
nef

asf
avi
dl
fli
gl
m2ts
webm
mkv
mov
mp4
mpeg
mpg
ts
wmv
xcf
xwd
flv
m4v
''', magenta

    # audio formats
    SOUND = '''
ape
flac
mp3
mpc
ogg
wav
wma
wv
''', magenta

    # compiled/intermediate stuff
    BINARY_OBJ = '''
pyc
obj
o
so
a
dll
''', black,bold

############################## no more configs below ######

class FMT4dircolors:
    keys =' '
    values =';'
    items ='\n'
    suffix_pfx = '.'
    use_abbr = False

class FMT4ls:
    keys ='='
    values =';'
    items =':'
    suffix_pfx = '*.'
    use_abbr = True

FMT = FMT4dircolors


def type_valueonly_flat( values, ignore_abbr =1):   #recursive lookup/flatten
#    abbr = values[0]
    r = []
    for v in values[ ignore_abbr:]:
        if isinstance(v,tuple):
            r += type_valueonly_flat( v)
        else:
            r.append(v)
    return r

def types():
    typs = []
    for k,value in TYPEs.__dict__.iteritems():
        if not k.startswith('_'):
            abbr = value[0]
            name = FMT.use_abbr and abbr or k
            typs.append( [name, type_valueonly_flat( value)])
    return typs

#print type_valueonly_flat( TYPEs.DIR)
#print type_valueonly_flat( TYPEs.STICKY_OTHER_WRITABLE )
#print type_valueonly_flat( TYPEs.STICKY)

def suffixes( what, *colors):
    a = what + what.upper() + what.lower()
    a = a.split()
    d = dict.fromkeys( a, 1 ).keys()
    d.sort()
    c = type_valueonly_flat( colors, ignore_abbr =0)
    return ( ( FMT.suffix_pfx + key, c)   for key in d )


def itemize( pairs):
    return [ FMT.keys.join( [k, FMT.values.join(
                        isinstance( c,(tuple,list)) and [ str(a) for a in c ] or [str(c)]
                        ) ]
                )
            for k,c in pairs
            if not k.startswith('_') and c ]



import sys
do_dir = do_ls = False
do_dosexe = False
for a in sys.argv[1:]:
    if a.startswith( '-dircolor'): do_dir = True
    if a.startswith( '-ls'): do_ls = True
    if a.startswith( '-dosexe'): do_dosexe = True

if do_ls == do_dir:
    raise SystemExit, help + ', '.join( k for k in SUFFIXEs.__dict__.iterkeys() if not k.startswith('_'))
if not do_dosexe:
    del SUFFIXEs.DOS_EXEC

p = []
if do_dir:
    FMT = FMT4dircolors
    p += itemize( ('TERM',a)   for a in TERMs.split() )
else:   #do_ls
    #ignore term-check -- don't be too smart
    FMT = FMT4ls

p+= itemize( types())
for k,s in SUFFIXEs.__dict__.iteritems():
    if not k.startswith('_'):
        p+= itemize( suffixes( *s))

print FMT.items.join( p )

# vim:ts=4:sw=4:expandtab

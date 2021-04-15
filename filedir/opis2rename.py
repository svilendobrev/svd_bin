#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys,re
import subprocess, glob
from svd_util import optz
from svd_util import lat2cyr
l2c = lat2cyr.zvuchene.lat2cyr
c2l = lat2cyr.zvuchene.cyr2lat

f_by_number = '*{n}*'
f_by_title  = '*{t}*'
optz.bool( 'fake',  '-n',   help= 'do nothing')
optz.bool( 'verbose', '-v', )
optz.bool( 'enumerate',  '-e',   help= 'enumerate title-per-lines from 1')
optz.text( 'input_pattern', default= '(NUM[-. ]+)?(<t>.*?)( TIME)?(EXT)?$', help= 'input pattern ~ re., names: n/umber t/itle y/ear a/rtist b:album; pre-processed: /=-, del spaces,",text after #')
optz.text( 'command', '-c', default= 'renpy', help= 'command to run may be with args: fromwhat intowhat whichfiles, builtins: renpy meyed3, default=%default')
optz.text( 'extensions',    default= 'mp3,flac,wav', help= 'file-extensions to match (as one text, comma-separated), default=%default')
optz.list( 'paths', '-p',   help= 'paths to walk, may be multiple or glob, default=./')
optz.text( 'separator',     default= '. ',  help= 'separator between number and title, default="%default"')
optz.text( 'startswith',    default='',     help= 'filenames must start with this')
#optz.bool( 'nounder2space', help= 'do not turn _ into space')
optz.bool( 'cyr2lat', )
optz.bool( 'lat2cyr', )
optz.bool( 'noinnumber',    help= 'do not look for number in name; use with --enum')
optz.bool( 'nonumber',      help= 'do not put number in name')
optz.bool( 'noextension',   help= 'do not put file-extension')
optz.text( 'filename_pattern', help= f'file-name pattern, args: n/umber t/itle a/rtist b:album l:whole-line, default={f_by_number} or if --noinnumber {f_by_title})')
optz.bool( 'notrack',       help= 'remove track-prefix')
optz.text( 'artist_after_title',  help= 'separator to split into title and artist')
optz.help( '''
%prog [options] [-- ...command args]
   args after -- are passed to command
   ''')
#defaults = optz.oparser.defaults
_optz = optz
optz,argz = optz.get()

if not optz.filename_pattern:
    optz.filename_pattern = f_by_title if optz.noinnumber else f_by_number
_re_time = '\d+:\d+'
re_time = re.compile( _re_time)
re_time_only = re.compile('^'+_re_time+'$')

re_num_title = re.compile('[-+\s]*(\d+)[!-._,:\s]+(.*)')
optz.verbose = optz.verbose or optz.fake
print( '###', optz, argz)
extensions = optz.extensions.split(',')
extensions2re = '(?P<ext>'+'|'.join( extensions)+')'
runs = []
used = {}

re_input_pattern = (optz.input_pattern
                ).replace( 'EXT',   '\.'+extensions2re
                ).replace( 'TIME',  _re_time
                ).replace( 'NUM',   '(?P<n>\d+(-\d+)?)'
                ).replace( '(<',    '(?P<'
                )
print( '::', re_input_pattern)
re_input_pattern = re.compile( re_input_pattern)

nn = 0
for l in sys.stdin:
    l = l.strip()
    if not l: continue
    l = l.split( '#')[0].strip()
    if not l: continue
    l = l.replace( '/', '-')
    #if not optz.nounder2space: l = l.replace( '_', ' ') ??
    l = l.split()
    if re_time_only.match( l[-1]): l.pop()
    l = ' '.join( l)
    l = l.rstrip(' -:_,=')
    l = '_'.join( l.split('_'))
    l = l.replace( '"', '')
    l = l.replace( '/', '-')
    nn += 1
    tags = {}
    m = re_input_pattern.match( l)
    if optz.verbose: print( l, m and m.groupdict())
    if m:
        ##n t y a l
        tags = dict( (k,v if v is None else v.strip().strip('_').strip()) for k,v in m.groupdict().items())
    if optz.enumerate:
        n = nn
    else:
        n = tags.get('n') or None
    if n:
        try:
            n = int(n)
            ns = f'{n:02d}'
        except ValueError:
            #n = nn
            ns = n
    elif not optz.noinnumber: continue  #XXX ??
    tags['n'] = ns
    #elif not tags:
    #    m = re_num_title.match( l)
    #    if not m: continue
    #    n,l = m.groups()
    #    n = int(n)
    if 0:
        if n in used:
            print( ' !?? dup', n, l , '==', used[n])
            continue
        if n is not None: used[n] = l

    l = re.sub( '\.'+extensions2re+'$', '', l)
    rfiles = optz.startswith + optz.filename_pattern.format( l=l, **tags) #f'*{n:02d}*'
    args = [
        ('track' if optz.notrack else '') + ('' if optz.nonumber or optz.noinnumber or not n else f'(?<!\d)0?{ns}(?!\d)') + '[^/]*\.' + extensions2re,
        ('' if optz.nonumber or not n else (ns + optz.separator)) + (tags.get('t') or l) + ('' if optz.noextension else '.$1'),
        ]    #nondigit?-digit-digit-nondigit?...whatever
    files = []
    for p in optz.paths or ['.']:
        for e in extensions:
            #if optz.verbose: print( p.rstrip('/')+'/'+rfiles+'.'+e)
            files += glob.glob( p.rstrip('/')+'/'+rfiles+'.'+e)     #glob.escape if needed
    if optz.verbose: print( ' ', rfiles + '.{'+','.join(extensions)+'}', ':', optz.command, argz, *(repr(a) for a in (args + files )))
    if not files: continue
    runs.append( (tags, argz, args, files))
#separate exec from file-find..
if optz.verbose:
    for r in runs: print( '>', r)

for (tags, argz, args, files) in runs:
    if optz.command == 'renpy':
      if not optz.fake:
        oparser = _optz.oparser
        _optz.make()
        import rename
        rename.run( argz + args + files)
        _optz.oparser = oparser
    elif optz.command == 'meyed3' or optz.command.startswith( 'mey'):
        for f in files:
            meyed3_tags = 'meyeD3 --v12 --encv1=cp1251 --to-v2.3 --encoding=utf16 --remove-all-comments'.split()
            t = tags.get('t') or args[1] #'.'.join( args[1].split('.')[1:-1]).strip()
            a = tags.get('a')
            if optz.artist_after_title:
                ta = t.split( optz.artist_after_title, 1)
                if len(ta) == 2:
                    t,a = [x.strip() for x in ta]
                    tags.update( t=t,a=a)
            for k,v in tags.items():
                if isinstance( v,str):
                    v = v.replace('_',' ').strip()
                    if optz.cyr2lat: v = c2l(v)
                    elif optz.lat2cyr: v = l2c(v)
                    tags[k] = v
            if optz.nonumber: tags.pop('n',0)
            TAGS_OPTS = dict( ((k,k) for k in 'nta'), b='A',y='Y')
            sargs = meyed3_tags + argz
            for k,v in sorted( tags.items()):
                if k in TAGS_OPTS and v:
                    if k=='n': v= str(v).replace( '-','')
                    sargs += [ '-'+TAGS_OPTS[k], str(v) ]
            sargs += [f]
            if optz.verbose: print( '>>', *sargs)
            if not optz.fake:
                subprocess.call( sargs)
    elif optz.command:
      if not optz.fake:
        subprocess.call( optz.command.split() + argz + args + files )

# vim:ts=4:sw=4:expandtab

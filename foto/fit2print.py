#!/usr/bin/env python
# -*- coding: utf-8 -*-
#$Id: fit2print.py,v 1.8 2008-02-15 09:29:28 sdobrev Exp $

class Pixeler:
    def __getitem__( me, size):
        w,h = [ int(z) for z in size.split('x')]
        return w,h
pixeler = Pixeler()
formats = {
 'pixels': pixeler,
 'pix': pixeler,
 'kodak': { #obrazcov dom
    '9x13'  : [1600,1122],
    '10x15' : [1915,1286],
    '13x18' : [2243,1600],
    '15x20' : [2558,1915],
    '15x21' : [2558,1915],
    '20x30' : [3843,2588],
    },
 'konica': { #червен площад - собственик Стойков, 0887 330556
    '9x13'  : [1500,1051],
    '10x15' : [1795,1205],
    '13x18' : [2102,1500],
    '15x20' : [2551,1795],
    '15x21' : [2551,1795],
    '20x30' : [3602,2398],
    },
 'fuji-x': { #червен площад
    '9x13'  : [1500,1050],
    '10x15' : [1795,1205],      #152x102 300dpi
    '13x18' : [2102,1500],
    '15x20' : [2551,1795],
    '15x21' : [2551,1795],
    '20x30' : [3602,2398],
    },
 'fuji': { #черно море frontier 340
    #'9x13'  : [2369,1660],
    '9x13'  : [1500,1051],
    #'10x15' : [2592,1763],
    '10x15' : [1797,1206], #[1772,1185], #[1795,1205],
    #'13x18' : [2102,1500],
    #'15x20' : [2551,1795],
    #'15x21' : [2551,1795],
    #'20x30' : [3602,2398],
    },
}

import os
class command:
    def args2args( me, *args, **kargs): raise NotImplemented
    any = True
    name = None
    _input = None
    def __init__( me, command_pipe, *args, **kargs):
        cmd_args=[ me.name ]
        av = me.args2args( *args, **kargs)
        if isinstance( av, dict):
            for name,value in av.iteritems():
                if name is None and value is not None: cmd_args += [ str(value) ]
                elif value is True: cmd_args += [ name ]
                elif value is not None:
                    cmd_args += [ name, str(value) ]
        else:
            for value in av:
                if value is not None: cmd_args += [ str(value) ]
        me.cmd_args = cmd_args
        command_pipe.append( me)    #cmd_args)
    #return os.spawnvp( OS.P_WAIT, cmd_args[0], cmd_args)
    def input( me, name): me._input = [ '<', name ]
    def __str__( me):
        r = me.cmd_args
        if me._input: r = r + me._input
        return ' '.join( r)

class do_cut( command):
    name = 'pnmcut'
    def args2args( me, x=None, y=None, w=None, h=None):
        if '--portrait' in opts:
            w,h = h,w
            x,y = y,x
        return { '-left':x, '-top':y, '-width':w, '-height':h}

class do_scale( command):
    name = 'pnmscale'
    def args2args( me, w=None, h=None, reduce=None, scale=None ):
        if '--portrait' in opts: w,h = h,w
        return { '-xsize':w, '-ysize':h, '-reduce':reduce, None: scale }

class do_edge( command):
    name = 'pnmnlfilt'
    def args2args( me, edge='0.3', radius=None ): return [ str(-float(edge)), radius]

class do_gamma( command):
    name = 'pnmgamma'
    def args2args( me, gamma=None): return [gamma]

class do_djpeg( command):
    name = 'djpeg'
    r = [ '-pnm' ]
    def args2args( me, scale =None):
        return scale and me.r + [ '-scale', '1/'+str(scale) ] or me.r
    def input( me, name): me._input = [ name ]

class do_cjpeg( command):
    name = 'cjpeg'
    def args2args( me, quality =None):
        return { '-q': quality, '-optimize': True, '-progressive': True }

class to_png( command):
    name = 'pnmtopng'
    def args2args( me): return ()

class do_png( command):
    name = 'pngtopnm'
    def args2args( me): return ()
    def input( me, name): me._input = [ name ]

class do_flip( command):
    name = 'pnmflip'
    def args2args( me, rotate, cw ='cw'):
        if not rotate or not int( rotate):
            me.any = False
            return []
        assert rotate in '90 270 -90 -270 180 -180'.split()
        rotate = int(rotate)
        if rotate <0: rotate += 360
        if rotate != 180 and cw == 'ccw':
                rotate = 360 - rotate
        return [ '-r' + str(rotate) ]
	#$(FIT2) .. --flip=`jhead $< | grep rotate |sed -s 's/.*rotate //'`,ccw ..


class Command_pipe( list):
    _commands = dict( (k,v) for k,v in globals().items() if k.startswith('do_') and issubclass( v, command))
    def __getattr__( me, key):
        return lambda *a,**k: me._commands[ key]( me, *a, **k)


class opt:
    def __init__( me, name, default, values, optname ='', always_on =False):
        me.name = name.strip()
        me.default  = default
        me.values   = values
        me.always_on = always_on
        me.optname = '--' + ( optname or name.lower() ).strip()
    def help( me):
        return '%(name)s=%(default)s \t%(values)s' % me.__dict__
    __str__ = help
    def env( me):
        return os.environ.get( me.name, me.default)
    def get( me, opts):
        try:
            return opts[ me.optname] or me.env()
        except KeyError:
            if me.always_on: return me.env()
            raise


opt.foto    = opt( 'FOTO',    'fuji',  sorted( formats))
opt.size    = opt( 'SIZE',    '10x15', sorted( formats[ opt.foto.default]))
opt.edge    = opt( 'EDGE',    '0.5',   '0.1-0.9(harsh)' )
opt.radius  = opt( 'RADIUS',  '0.8',   '0.5-0.9' )
opt.gamma   = opt( 'GAMMA',   '1.1',   '<1 -darken; >1 - lighten' )
opt.cjpeg   = opt( 'QUALITY', '90',    '30-95(better/bigger)', optname= 'cjpeg' )
opt.ratio   = opt( 'RATIO',   '3,2',   'x,y or "auto"',     always_on= True )
opt.shift   = opt( 'SHIFT',   '0',     '0=center, -1=top/left, +1=bottom/right', always_on=True)

s_args = 'nqh248'
l_args = [
    'help',
    'size=[[SIZE][,FOTO]]',
    'edge=[[EDGE][,RADIUS]]',
    'gamma=[GAMMA]',
    'reduce=REDUCEFACTOR',
    'ratio=[RATIO]',
    'shift=[SHIFT]',
    'flip=[90|270|180|-90|-270|-180][,cw|ccw]',
    'djpeg',
    'cjpeg=[QUALITY]',
    'out=OUTPUTFILE',
    'png',
    'swapxy',
    'autooutpfx=PREFIX4_AUTO_INPUT2OUTPUT',
    'autoname=PYTHONEXPR(name)',
    'exifcopy',
    'portrait',
    'norm',
    'pipe=command-to-pipe-through',
]

import sys
import getopt
def help():
    print sys.argv[0], ' '.join( [('-'+a) for a in s_args]), ' '.join( [('--'+a) for a in l_args] ), '[INPUTFILE]'
    print ' all are optional but specify at least one (may have empty value) to proceed'
    print ' tries env vars for options with empty/non-specified arg-value'
    print ' non-specified output means stdout'
    print ' -n  builds the command pipe and only prints it'
    print ' -q  be quiet'
    print ' -h/--help  this help'
    print ' -2 -4 -8   fast downscale (only if djpeg)'
    print ' sizes:'
    print ' ', opt.foto
    print ' ', opt.size
    print ' ', opt.shift
#    print ' ', opt.ratio
    print ' sharpness:'
    print ' ', opt.edge
    print ' ', opt.radius
    print ' brightness:'
    print ' ', opt.gamma
    print ' cjpeg:'
    print ' ', opt.cjpeg
    raise SystemExit,2
ol_args = [ (a[:a.find('=')+1] or a) for a in l_args]
#print ol_args
try:
    optslist, args = getopt.getopt( sys.argv[1:],
                    s_args,
                    ol_args,
                )
except getopt.GetoptError:
    # print help information and exit:
    help()

opts = dict( optslist)
#print opts, args
#raise SystemExit,3

if not opts or '-h' in opts or '--help' in opts:
    help()

def go( input =None):
    cp = Command_pipe()

    if '--djpeg' in opts or input and os.path.splitext(input)[1].lower() in ['.jpg','.jpeg']:
        scale = None
        for a in [2,4,8]:
            if '-'+str(a) in opts:
                scale = a
                break
        cp.do_djpeg( scale)
    elif '--png' in opts or input and os.path.splitext(input)[1].lower() in ['.png']:
        cp.do_png()

    cp.whatsize = ''
    for o,v in optslist:
        if o in ['--djpeg', '--cjpeg', '--png']:
            continue
        elif o == '--edge':
            e = v.split(',')
            cp.do_edge( e[0] or edge.env(), len(e)>1 and e[1] or opt.radius.env() )
        elif o == '--reduce':
            cp.do_scale( scale=1/float( v))
        elif o == '--gamma':
            cp.do_gamma( opt.gamma.get( opts))
        elif o == '--norm':
            cp.append( 'pnmnorm' )
        elif o == '--pipe':
            cp.append( v)
        elif o == '--flip':
            e = v.split(',')
            cp.do_flip( *e)
        elif o == '--size':
            whatsize = v.split(',')
            size = whatsize[0] or opt.size.env()
            foto = len(whatsize)>1 and whatsize[1] or opt.foto.env()

            shift = int( opt.shift.get( opts) )
            ratio = opt.ratio.get( opts)
            if ratio.lower() == 'auto' and input:
                assert 0, 'cant auto: dont know picture size'
                ratio = '?'
            else: ratio = (int(a) for a in ratio.split(','))
            ratio_x,ratio_y = ratio
            w,h = formats[ foto][ size]
            if '--swapxy' in opts: h,w=w,h
            if w<h and ratio_x>ratio_y:
                ratio_x,ratio_y = ratio_y,ratio_x
            print w,h, ':'#, w1,hr, '/', wr,h1
            cp.whatsize = foto +' '+ size

            wh= w/float(h)
            rxy= ratio_x/float(ratio_y)
            if wh < rxy or wh==rxy and h>w:
                hr = h + ratio_y - (h % ratio_y or ratio_y)
                w1 = hr * ratio_x / ratio_y
                cp.do_scale( h=hr)
                #print 2222222222222, ratio_x, ratio_y, '>', w,h, ':', hr, w1
                if w1>w:
                    d = w1-w
                    if shift<0: d=0
                    elif not shift: d/=2
                    cp.do_cut( x=d, w=w, h=h )
            else:
                wr = w + ratio_x - (w % ratio_x or ratio_x)
                h1 = wr * ratio_y / ratio_x
                cp.do_scale( w=wr)
                if h1>h:
                    d = h1-h
                    if shift<0: d=0
                    elif not shift: d/=2
                    cp.do_cut( y=d, h=h, w=w )


    try:
        cp.do_cjpeg( opt.cjpeg.get( opts) )
    except KeyError:
        #if '--png' in opts:
        #    cp.do_png()
        pass

    if input: cp[0].input( input )
    return cp

def quote(x): return '"'+x+'"'

import os.path
for input in args:
    if input == '-': input = None
    command_pipe = go( quote(input) )
    cmd = ' | '.join( [str(c) for c in command_pipe if getattr( c, 'any',1) ])

    outputpfx = opts.get( '-autooutpfx', opts.get('--autooutpfx', None ))
    outname = opts.get( '-autoname', opts.get('--autoname', None ))
    output = opts.get( '-o', opts.get('--out', None ))
    if not output and input:
        output = outname and eval( outname, dict( name= input), globals()) or ''
        if outputpfx:
            output = outputpfx + (output or input)
        #print 'assume autooutput:', output
    assert output != input, input
    if output and cmd:
        dirname = os.path.dirname( output )
        if dirname:
            cmd = 'mkdir -p ' + quote( dirname) + ' ; ' + cmd
        cmd += ' > %(output)s'

    if '--exifcopy' in opts:
        if input and output:# and '--djpeg' in opts and [ c for c in command_pipe if isinstance( c, do_cjpeg)]:
            if cmd: cmd += ' ; '
            cmd += 'jhead -te %(input)s -dt %(output)s '

    if input:  input = quote( input)
    if output: output = quote( output)
    cmd = cmd % locals()
    if '-q' not in opts:
        print >> sys.stderr, command_pipe.whatsize, ':', cmd
    if '-n' not in opts:
        os.system( cmd )

# vim:ts=4:sw=4:expandtab

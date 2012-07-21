#$Id: diamif.py,v 1.2 2006-05-11 16:51:07 sdobrev Exp $
#  PyDia 2 MIF (Framemaker)

import sys, math, os
import dia

def _clr( *args):
    return tuple( [ int(100*a) for a in args ] )
#_clr = staticmethod( _clr)

_color_table = {
    _clr( 0,0,0,1) : 'Black',
    _clr( 0,0,0,0) : 'White',

    _clr( 0,1,1,0) : 'Red',
    _clr( 1,0,1,0) : 'Green',
    _clr( 1,1,0,0) : 'Blue',

    _clr( 1,0,0,0) : 'Cyan',
    _clr( 0,1,0,0) : 'Magenta',
    _clr( 0,0,1,0) : 'Yellow',
}

_font_translator_back = {
    'Helvetica': [ 'arial', 'helvetica', 'helv', 'sans' ],
    'Times' :    [ 'times new roman', 'times', 'serif' ],
    'Courier':   [ 'courier new', 'courier', 'monospace', 'fixed' ],
}
_font_translator = {}
for k,v in _font_translator_back.iteritems():
    for kk in v:
        _font_translator[ kk] = k


class MIFMaker:
    class Struct:
        def __init__( me, **kargs):
            me.__dict__.update( kargs)

    def __init__( me):
        me.f = None
        me.line_caps = 0
        me.line_join = 0
        me.line_style = 0
        me.dash_length = 0
        me.line_width = 0

    def _open( me, filename):
        me.filename = filename
        me.f = open( filename, "w")

    _scale = 0.3
    _x0 = _y0 = 0

    def _xy( me, x,y):
        x += me._x0
        y += me._y0
        return x * me._scale, y * me._scale
    def _wh( me, w,h):
        return w * me._scale, h * me._scale
    def _dist( me, w):
        return w * me._scale

    class cfg:
        as_aframe = os.environ.get( 'DIA2MIF_AS_AFRAME')
        font_scale = os.environ.get( 'DIA2MIF_FONT_SCALE')
        if font_scale: font_scale = float( font_scale)
        font_stretch = os.environ.get( 'DIA2MIF_FONT_STRETCH')
        if font_stretch: font_stretch = '<FStretch %f%%>' % (100.0*float(font_stretch))

    def begin_render( me, data, filename):
        me._open( filename)
        r = data.extents
        me._x0 = -r.left
        me._y0 = -r.top
        W,H = me._wh( r.right - r.left, r.bottom - r.top )
        extents = data.extents
        active_layer = data.active_layer.name
        scale = me._scale
        r = ''
        if me.cfg.as_aframe:
            r = '''<MML>
<AFrame # %(filename)s by diamif.py
'''
            #W += 0.5    #for texts sticking out / wrong fonts
        else:
            r = '''\
<MIFFile 5> # by diamif.py
<Units Ucm>
<AFrames
 <Frame
  <ID 1>
'''
        r += '''\
  <FrameType Below>
  <AnchorAlign Center>
  <Cropped No>
  <BRect 0 0 %(W).3fcm %(H).3fcm>
  # extents=%(extents)s
  # scale=%(scale)s
  # active_layer=%(active_layer)s
'''
        me.f.write( r % locals() )

    def end_render( me):
        filename = me.filename
        if me.cfg.as_aframe:
            r = '''
  # eo AFrame %(filename)s
>
'''
        else:
            r = '''
 > # eo Frame
> # eo AFrames

<TextFlow
 <TFAutoConnect Yes>
 <TFTag `B'>
 <Para
  <PgfTag `Body'>
  <ParaLine
	<String `%(filename)s'>
	<AFrame 1>
  >
 >
>
# eof %(filename)s
'''
        me.f.write( r % locals() )
        me.f.close()

    def set_linewidth( me, width):
        if width < 0.001: # zero line width is invisble ?
            me.line_width = 0.001
        else:
            me.line_width = width
    def set_linecaps( me, mode):
        me.line_caps = mode
    def set_linejoin( me, mode):
        me.line_join = mode
    def set_linestyle( me, style):
        me.line_style = style
    def set_dashlength( me, length):
        me.dash_length = length
    def set_fillstyle( me, style):
        # currently only 'solid' so not used anywhere else
        me.fill_style = style
    def set_font( me, font, size):
        me.font = font
        me.font_size = size
    def draw_line( me, start, end, color):
        me.draw_polyline( (start, end), color)

    def _obj_style( me, color, _fill =False):
        fill = not _fill and 15 or 0
        pen  = _fill and 15 or 0
        color = me._color( color)
        stroke_style = me._stroke_style()
        line_width = me._dist( me.line_width )
        return '''
    <Pen %(pen)d>
    <Fill %(fill)d>
    <PenWidth %(line_width).3fcm>
    %(color)s
    # stroke_style %(stroke_style)s
''' % locals()
#    <Comment ObColor `Green'>

    def draw_polyline( me, points, color, _gon =False, _fill =False, _smooth =False):
        what = _gon and 'Polygon' or 'PolyLine'
        style = me._obj_style( color, _fill)
        p = '''
  <%(what)s %(style)s'''
        if _smooth:
            p+= '''\
    <Smoothed Yes>
'''
        me.f.write( p % locals() )
        for pt in points:
            me.f.write( '\
    <Point %.3fcm %.3fcm> ' % me._xy( pt.x, pt.y) )
        me.f.write( '''
  > # eo %(what)s
''')
    def draw_polygon( me, *args, **kargs):
        me.draw_polyline( _gon=True, *args,**kargs)
    def fill_polygon( me, *args, **kargs):
        me.draw_polyline( _gon=True, _fill=True, *args,**kargs)

    def draw_rect( me, rect, color, _fill =False):
        L,T = me._xy( rect.left, rect.top )
        W,H = me._wh( rect.right - rect.left, rect.bottom - rect.top)
        style = me._obj_style( color, _fill)
        me.f.write( '''
  <Rectangle %(style)s
    <ShapeRect %(L).3fcm %(T).3fcm %(W).3fcm %(H).3fcm >
  > # eo Rectangle
''' % locals() )
    def fill_rect( me, *args,**kargs):
        me.draw_rect( _fill=True, *args,**kargs)

    def draw_arc( me, center, width, height, angle1, angle2, color, _fill =False):
#        _fill=True
#        rx,ry = width / 2.0, height / 2.0
#        mPi180 = math.pi / 180.0
#        ss = center.x + rx * math.cos(mPi180 * angle1), center.y - ry * math.sin(mPi180 * angle1)
#        ew = center.x + rx * math.cos(mPi180 * angle2), center.y - ry * math.sin(mPi180 * angle2)
        style = me._obj_style( color, _fill)
        L,T = me._xy( center.x - width/2.0, center.y - height/2.0 )
        W,H = me._wh( width,height )
        start_angle = 90 - angle1
        delta_angle = -(angle2 - angle1)
        if delta_angle >180: delta_angle -= 360
        if delta_angle <-180: delta_angle += 360
#        fss = L+W/2.0 + W/2.0 * math.cos(mPi180 * angle1), T + H/2 - H/2 * math.sin(mPi180 * angle1)
#        fee = L+W/2.0 + W/2.0 * math.cos(mPi180 * angle2), T + H/2 - H/2 * math.sin(mPi180 * angle2)
#        fc  = L+W/2.0, T+H/2.0

        degree = me.cfg.as_aframe and 'd' or ''

        me.f.write( '''
  <Arc %(style)s
    <ArcRect %(L).3fcm %(T).3fcm %(W).3fcm %(H).3fcm >
    <ArcTheta  %(start_angle)f%(degree)s >
    <ArcDTheta %(delta_angle)f%(degree)s >
  > # eo Arc
''' % locals() )
        # moveto sx,sy arc rx,ry x-axis-rotation large-arc-flag,sweep-flag ex,ey
        #me.f.write( ' d ="M %.3f,%.3f A %.3f,%.3f 0 %d,%d %.3f,%.3f ">\n' % (sx, sy, rx, ry, largearc, sweep, ex, ey) )

    def fill_arc( me, *args,**kargs):
        me.draw_arc( _fill=True, *args,**kargs)
    def draw_ellipse( me, center, width, height, color, _fill =False):
        L,T = me._xy( center.x - width/2.0, center.y - height/2.0 )
        W,H = me._wh( width,height )
        style = me._obj_style( color, _fill)
        me.f.write( '''
  <Ellipse %(style)s
    <ShapeRect %(L).3fcm %(T).3fcm %(W).3fcm %(H).3fcm >
  > # eo Ellipse
''' % locals() )
    def fill_ellipse( me, *args,**kargs):
        me.draw_ellipse( _fill=True, *args,**kargs)

    def draw_bezier( me, bezpoints, color, _fill =False):
        points = []
        for bp in bezpoints:
            if bp.type == 0: # BEZ_MOVE_TO
                points.append( bp.p1 )
            elif bp.type == 1: # BEZ_LINE_TO
                points.append( bp.p1 )
            elif bp.type == 2: # BEZ_CURVE_TO
                points.append( bp.p1 )
                points.append( bp.p2 )
                points.append( bp.p3 )
            else:
                dia.message( 2, "Invalid BezPoint type (%d)" * bp.type)
        me.draw_polygon( points, color, _smooth =True, _fill=_fill)
    def fill_bezier( me, *args,**kargs):
        me.draw_bezier( _fill=True, *args,**kargs)

    def draw_string( me, text, pos, alignment, color):
        if len(text) < 1:
            return # shouldn'this be done at the higher level
        talign = ('Left', 'Center', 'Right') [ alignment ]

        fstylemask = me.font.style
# see dia*/lib/font.h
            #DIA_FONT_STYLE_GET_SLANT
        italic = oblique = 'Italic'
        fangle = ('Regular', italic, italic) [ (me.font.style >> 2) & 0x03 ]
            #DIA_FONT_STYLE_GET_WEIGHT
        fweight = (400, 200, 300, 500, 600, 700, 800, 900) [(me.font.style  >> 4)  & 0x7]
        if fweight>400: fweight = 'Bold'
        else: fweight = 'Regular'

        fsize = me._dist( me.font_size )
        if me.cfg.font_scale:
            fsize *= me.cfg.font_scale
            #maybe use direct
            #DIA_FONT_STYLE_GET_FAMILY: (any,sans,serif,mono) [ me.font.style & 0x03 ]
        ffamily = me.font.family
        try:
            ffamily = _font_translator[ ffamily.lower() ]
        except KeyError: pass

        x,y = me._xy( pos.x, pos.y)
        fcolor = me._color( color, _just_colorname=True)
        style = me._color( color)
        # avoid writing XML special characters (ampersand must be first to not break the rest)
#        for rep in [('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ("'", '&apos;')]:
#            text = text.replace( rep[0], rep[1])
        font_stretch = me.cfg.font_stretch
        me.f.write( '''
  <TextLine
    <Comment %(style)s >
    <TLOrigin %(x).3fcm %(y).3fcm >
    <TLAlignment %(talign)s>
    <Font
      <FFamily `%(ffamily)s' >
      <FAngle `%(fangle)s' >    # %(fstylemask)d
      <FWeight `%(fweight)s' >
      <FSize  %(fsize).3fcm >  %(font_stretch)s
      <FColor `%(fcolor)s' >
    >
    <String `%(text)s'>
  > # eo TextLine
''' % locals() )

    def draw_image( me, point, width, height, image):
        #FIXME: do something better than absolute pathes ?
        me.draw_string( '<image "'+image.uri+'" w=%(width)s h=%(height)s>' % locals(),
            point, 0, me.Struct( red=1, blue=2, green=3) )

    # Helpers, not in the DiaRenderer interface

    def _color( me, color, _just_colorname =False): # color: dia rgb [0..1]
        r,g,b = color.red, color.green, color.blue
        #the CMYK color that uses the most black (K) and the least color (CMY)
        c1, m1, y1 = 1-r, 1-g, 1-b
        if not r+g+b: c,m,y,k = 0,0,0,1.0
        else:
            k = min( c1,m1,y1)
            k1 = 1-k
            c,m,y = (c1-k)/k1, (m1-k)/k1, (y1-k)/k1

        which = _clr( bool(c),bool(m),bool(y),bool(k) )
        n = -1
        try:
            name = _color_table[ which ]
            n = sum( which)/100
            if n==1: tint = (c+m+y+k)*100
            elif n==2: tint = (r+g+b)*100
            else: tint = 100
        except KeyError:
            name = str(color)
            tint = (r+g+b)*100/3    #some gray?

        if _just_colorname: return name

        cmyk = c,m,y,k
        tint *=100
        return '''
     <ObColor `%(name)s' > # rgb %(color)s
     <ObTint %(tint)d%%>   # cmyk %(cmyk)s
''' % locals()

    def _stroke_style( me):
        # return the current line style as svg string
        dashlen = me.dash_length
        # dashlen/style interpretation like the DiaGdkRenderer
        dotlen = dashlen * 0.1
        caps = me.line_caps
        join = me.line_join
        style = me.line_style
        st = ""
        if style == 0: # LINESTYLE_SOLID
            pass
        elif style == 1: # DASHED
            st = 'stroke-dasharray="%.2f,%.2f"' % (dashlen, dashlen)
        elif style == 2: # DASH_DOT,
            gaplen = (dashlen - dotlen) / 2.0
            st = 'stroke-dasharray="%.2f,%.2f,%.2f,%.2f"' % (dashlen, gaplen, dotlen, gaplen)
        elif style == 3: # DASH_DOT_DOT,
            gaplen = (dashlen - dotlen) / 3.0
            st = 'stroke-dasharray="%.2f,%.2f,%.2f,%.2f,%.2f,%.2f"' % (dashlen, gaplen, dotlen, gaplen, dotlen, gaplen)
        elif style == 4: # DOTTED
            st = 'stroke-dasharray="%.2f,%.2f"' % (dotlen, dotlen)

        if join == 0: # MITER
            pass # st = st + ' stroke-linejoin="bevel"'
        elif join == 1: # ROUND
            st += ' stroke-linejoin="round"'
        elif join == 2: # BEVEL
            st += ' stroke-linejoin="bevel"'

        if caps == 0: # BUTT
            pass # default stroke-linecap="butt"
        elif caps == 1: # ROUND
            st += ' stroke-linecap="round"'
        elif caps == 2: # PROJECTING
            st += ' stroke-linecap="square"' # is this the same ?

        return st

# dia-python keeps a reference to the renderer class and uses it on demand
dia.register_export( "MIF/FrameMaker", "mif", MIFMaker())

# vim:ts=4:sw=4:expandtab

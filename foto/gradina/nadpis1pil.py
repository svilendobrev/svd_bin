#$Id$
# -*- coding: utf-8 -*-
import Image, ImageDraw, ImageFont

sizept=12
dpi=320
h_cm=15.0

ttf = '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'
textcolor = (  40, 40, 40)
#textcolor = ( 40, 10, 50)
opaque = 60

############
sizepx= sizept/72.0*dpi


typ='RGB'
backgr=200,200,200

class Labeler:
    def __init__( me, tl, tr, src ):
        if not isinstance( src, Image.Image):
            src = Image.open( src)
        #src = me.crop( src)
        me.sizepx( sizepx * src.size[1] / (dpi* h_cm / 2.54) )
        me.out = me.tt( tl,tr,src)
    def crop( me, src):
        r = src.crop( (0,20) + src.size )
        r.load()
        return r
    def sizepx( me, sizepx):
        #print >>sys.stderr, 'sizepx', sizepx
        me.ofs  = int( sizepx/8)
        me.font = ImageFont.truetype( ttf, size= int( sizepx) )

    def t( me, text, src, pos ='L'):
        tsz = me.font.getsize( text)
        ofs = me.ofs
        dw = ofs+ofs/2
        dh = ofs

        p = ImageDraw.Draw( src)
        if pos.upper().startswith( 'L'):
            x = dw
        else:
            x = src.size[0] - tsz[0] -dw
        y = src.size[1] - tsz[1] -dh
        p.text( (x,y), text, font= me.font, fill= textcolor)

    def tt( me, tl, tr, src):
        totsize = me.font.getsize( tl+' '+tr)
        heigth = totsize[1] + 2*me.ofs

        x = Image.new( typ, src.size, backgr)
        m = Image.new( 'L', src.size, 0)
        mask = opaque/100.0*255
        ImageDraw.Draw(m).rectangle( ((0,src.size[1]-heigth), src.size), fill= mask )
        out = Image.composite( x,src,m)

        me.t( tl, out, 'L')
        me.t( tr, out, 'R')
        return out

def label( *a, **k):
    l = Labeler( *a, **k)
    return l.out


if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        fname = sys.argv[1]
        src = Image.open( fname)
        #m.save( 'a.ppm')

        out = label( u'Мими-Поли', u'Мария-Полина Минчева', src)
        out.save( fname+'.ppm')
        #src.show()

# vim:ts=4:sw=4:expandtab

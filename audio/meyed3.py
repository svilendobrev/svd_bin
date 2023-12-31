# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
'''
link into ~/.eyeD3/plugins/
maybe ~/.eyeD3/config.ini : default/plugin
'''

if 0*'v1:0.8-python-v2':
    #inside eyed3.main.main()
    #XXX HACK
    import pathlib
    pathlib._py2_fs_encoding = args.fs_encoding #'utf8'


class ed3:
    from eyed3.id3 import tag, frames, ID3_V1, ID3_V2
_Tag = ed3.tag.Tag

import os
import argparse
try:
    unicode
except:
    unicode = str
class enco( unicode):
    encoding1 = 'latin_1'
    on = False
    def __new__( me, *a,**ka):
        if not me.on or (not a[1:] and not ka):
            return unicode.__new__( me, *a,**ka)
        try:
            return unicode.__new__( me, a[0], me.encoding1)
        except:
            print( (me, a,k))
            raise
    def encode( me, *a,**k):
        if not me.on:
            return unicode.encode( me, *a,**k)
        try:
            return unicode.encode( me, me.encoding1)
        except:
            print( repr(me))
            raise

if 'new':
    x= '''
    _loadV1Tag:     четене от в.1
        me.title = unicode(title, v1_enc)
    _saveV1Tag:     писане
        tag += pack(me.title.encode("latin_1") if me.title else b"", 30)
        ...
        for c in me.comments:
            use c.text
        ##########
    тъй че title,artist,album,comment някакси стават enco()?
    но май трябва и _setTitle... виж core.Tag
    или само .title ??
    може enco да поправи и конструктора / latin_1
    може enco да сработва само при искан latin_1
        '''
    _Tag__loadV1Tag = _Tag._loadV1Tag
    def _loadV1Tag( me, fp):
        ed3.tag.unicode = enco
        enco.on = True
        r = _Tag__loadV1Tag( me, fp)
        ed3.tag.unicode = unicode
        enco.on = False
        return r
    if 1:
        _Tag._loadV1Tag = _loadV1Tag

    #тези (+enco.encode) стигат за да работи писането в.1 _saveV1Tag
    o_getTitle  = _Tag._getTitle
    o_getArtist = _Tag._getArtist
    o_getAlbum  = _Tag._getAlbum
    def _getTitle(  me): return enco( o_getTitle( me))
    def _getArtist( me): return enco( o_getArtist( me))
    def _getAlbum(  me): return enco( o_getAlbum( me))
    _Tag._getTitle  = _getTitle
    _Tag._getArtist = _getArtist
    _Tag._getAlbum  = _getAlbum

    o_setReleaseDate= _Tag._setReleaseDate
    def _setReleaseDate( me, date):
        o_setReleaseDate( me, date)
        me._setDate( b"XDOR", date)    #if available, shadows other dates
        #me.frame_set.pop( "XDOR", 0) #doesnt work
    _Tag._setReleaseDate = _setReleaseDate
    _Tag.release_date = property( _Tag._getReleaseDate, _setReleaseDate)

    #обаче за коментарите е по-сложно..
    _CommentsAccessor = ed3.tag.CommentsAccessor
    #class CommentsAccessor( _CommentsAccessor):    #XXX там има super().. което води до тука !:
    o__iter__ = _CommentsAccessor.__iter__
    def n__iter__( me):
        for f in o__iter__( me):
            f.text = enco( f.text)
            yield f
    ed3.tag.CommentsAccessor.__iter__ = n__iter__

    #позволи едновременно в.1 и в.2
    _Tag.v12 = False
    _save = _Tag.save
    def save( me, version=None, **ka):
        version = version if version else me.version
        print( 'save', version, _Tag.v12 and '+v12' or '')
        #me.fake1 = version & ed3.ID3_V1 #allow own v1 Encoding
        r = _save( me, version=version, **ka)
        if _Tag.v12 and version[0] == ed3.ID3_V2[0]:   #allow v1 additional to v2
            print( 'extra-v1')
            #me.fake1 = True
            ka[ 'backup' ] = None     #сакън не пак
            enco.on = True
            r = _save( me, version=ed3.ID3_V1, **ka)
            enco.on = False
        #me.fake1 = False
        me.msaved = True
        return r
    _Tag.save = save

    from eyed3.plugins import classic
    class meyed3( classic.ClassicPlugin):
        NAMES = ["meyed3"]
        def __init__(me, arg_parser):
            classic.ClassicPlugin.__init__( me, arg_parser)
            op = arg_parser.add_argument_group("meyeD3 options")

            class Action1( argparse.Action):
                def __call__(me, parser, namespace, values, option_string=None):
                    enco.encoding1 = values[0]
            op.add_argument( '--encv1', dest='encv1',
                help ='str.encoding for v1 - be careful',
                action= Action1,
                type= str, nargs=1,
                )

            class Action2( argparse.Action):
                def __call__(me, parser, namespace, values, option_string=None):
                    _Tag.v12 = True
            op.add_argument( '--v12', dest='v12',
                help ='if v2, also add v1',
                action= Action2,
                nargs=0,
                )

            class Action3( argparse.Action):
                def __call__(me, parser, namespace, values, option_string=None):
                    #print( 11111, parser, namespace, values, option_string)
                    import sys

                    #tags = dict( (x.strip() for x in l.strip().split('=',1)) for l in
                    #tags = dict( (k.lower(),v) for k,v in tags.items())
                    #WTF.. multiline comments
                    tags = {}
                    k= None
                    for l in sys.stdin:
                        if not l.strip(): continue
                        kv = l.split( '=',1)
                        if len(kv) < 2 or l.startswith( ' '):
                            tags[ k ] += '\n'+l
                            continue
                        k,v = kv
                        k = k.strip().lower()
                        tags[ k ] = v.strip()

                    tx = dict( album= '', title= '', artist= 'performer', track= 'tracknumber',
                            track_total=    'tracktotal',
                            recorded_date=  'year date',
                            )

                    tags2 = {}
                    for k,tkk in tx.items():
                        tkk = [ k ] + tkk.split()   #always try k itself
                        for tk in tkk:
                            v = tags.get( tk)
                            if v:
                                tags2[ k] = v
                                break
                    print( tags2)
                    namespace.__dict__.update( tags2)

            #op.add_argument( '--fromfile', dest='fromfile',
            #    help= 'obtain tags from text file (- is stdin), as lines key=value',
            op.add_argument( '--stdin', dest='stdin',
                help= 'obtain tags from stdin, as lines key=value',
                action= Action3,
                nargs=0,
                )

        def handleFile( self, f):
            classic.ClassicPlugin.handleFile( self, f)
            if not _Tag.v12: return
            if self.audio_file.tag.version[0] == ed3.ID3_V1[0]: return
            if self.args.rename_pattern: return
            if getattr( self, 'msaved', False): return
            if self.args.remove_all or self.args.remove_v1 or self.args.remove_v2: return
            #again
            super(classic.ClassicPlugin, self).handleFile( f, tag_version= ed3.ID3_V1)
            self.printTag( self.audio_file.tag)

    #classic.ClassicPlugin = ClassicPlugin


if 0:
    IMAGE_AUTOSCALE = True
    #this was duplicating images..
    def addImage(me, type, image_file_path, desc = u""):
        image_frame = None
        if image_file_path:
            if me.IMAGE_AUTOSCALE:    #max 1Kx1K, non-progressive
                front = image_file_path+'.mp3.jpg'
                if not os.path.exists( front):
                    print( 'autoscale', front)
                    print( os.system( 'djpeg "%(image_file_path)s" | pnmscale -pixels 1050000 | cjpeg -q 75 -optimize > /tmp/meyd3tmp.jpg' % locals() ))
                    import shutil
                    #os.rename( '/tmp/meyd3tmp.jpg', front )
                    shutil.move( '/tmp/meyd3tmp.jpg', front )
                image_file_path = front
            image_frame = ed3.frames.ImageFrame.create( type, image_file_path, desc)

        image_frames = me.frames[ ed3.frames.IMAGE_FID]
        for i in image_frames:
            if i.pictureType == type:
                if image_frame: #compare
                    for a in 'description mimeType imageData'.split():  #encoding being set afterwards?
                        if getattr( i, a) != getattr( image_frame, a):
                            print( 'diff', a, image_file_path)
                            if a!='imageData': print( repr( getattr( i, a)), repr( getattr( image_frame, a)))
                            break   #diff
                    else:
                        image_frame = None
                        print( 'same', type, image_file_path)
                        continue   #same
                me.frames.remove(i)

        if image_frame:
            me.frames.addFrame( image_frame)

########### dont save if same tags
    f1 = f2 = None
    def __saveV2Tag( me, v):
        #print( 2222222221, object.__repr__(me))
        fnew = [ f.__dict__.copy() for f in me.frames ]
        if me.f2 == fnew: print( 222222222, 'same frames')
        else: _Tag.__saveV2Tag( me,v)

    def __loadV2Tag( me, f):
        if me.v12:
            me.clear()
            me.__loadV1Tag( isinstance( f, file) and f.name or f) #new fileptr plz
            me.clear()
        r = _Tag.__loadV2Tag( me, f)
        me.f2 = [ f.__dict__.copy() for f in me.frames ]
        return r

    def __saveV1Tag( me, v):
        #print( 111111111, object.__repr__(me))
        fnew = me.getv1data( enc= True)
        #print( 'old', *me.f1.items())
        #print( 'new', *fnew.items())
        if me.f1 == fnew: print( 111111111, 'same frames')
        else: _Tag.__saveV1Tag( me,v)


#??? same-tags?
def __eq__(me, o):
    if not isinstance( o, me.__class__): return False
    return me.__dict__ == o.__dict__
ed3.tag.Genre.__eq__ = __eq__
#eyed3.Frame.__eq__ = __eq__

_nums = ed3.tag.TagTemplate._nums
if isinstance( ed3.tag.TagTemplate.__dict__[ '_nums'], staticmethod):
    ed3.tag.TagTemplate._nums = staticmethod( lambda num_tuple, param, zeropad: _nums( num_tuple, param, False))
else: #old
    ed3.tag.TagTemplate._nums = lambda self, num_tuple, param, zeropad: _nums( self, num_tuple, param, False)

#ed3.tag.Tag = Tag #cached too many places before this


if 0:
    _EyeD3Driver = eyeD3_run.EyeD3Driver
    class EyeD3Driver( _EyeD3Driver):
        def handleEdits(me, tag):
            oo = (me.opts.track, me.opts.track_total)
            if '' in oo:
                tt = zip( oo, tag.getTrackNum())
                rr = [ None if o == '' else t for o,t in tt]
                tag.setTrackNum( rr, zeropad = me.opts.zeropad)

            if me.opts.remove_comments:   #because elif comments
                count = tag.removeComments()
                eyeD3_run.printWarning("Removing %d comment frames" % count)
                me.opts.remove_comments = None

            return _EyeD3Driver.handleEdits( me, tag)
    eyeD3_run.EyeD3Driver = EyeD3Driver
    eyeD3_run.main()

# vim:ts=4:sw=4:expandtab

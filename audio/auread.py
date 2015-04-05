#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

new = dict(
    sample_rate = 44100/5, #16000,
    channels =1 ,
    )
new = ()

for a in sys.argv[1:]:
    print()
    print( a)
    def aut(a):
        'py2 + py3 + cygwin'
        #http://audiotools.sourceforge.net/programming/audiotools.html#pcmreader-objects
        import audiotools
        f = audiotools.open(a)
        nchannels = f.channels()
        sample_rate = f.sample_rate()
        print( nchannels, 'x', sample_rate, f.total_frames() )
        pcm = f.to_pcm()
        if new:
            nchannels = new['channels']
            kargs = dict(
                    sample_rate = f.sample_rate(),
                    channel_mask= audiotools.ChannelMask.from_channels( nchannels),
                    #bits_per_sample= f.bits_per_sample,
                    )
            kargs.update( new)
            r = pcm
            pcm = audiotools.PCMConverter( r,
                    #channel_mask= audiotools.ChannelMask.from_channels( nchannels),
                    bits_per_sample= r.bits_per_sample,
                    **kargs)
        return nchannels, pcm
    FLOAT = 0

    def dataiter(p):
        while True:
            data = p.read( 1024*32)
            if not data: break
            if FLOAT: data = data.to_float()
            yield data

    def aut_channels( a):
        nchannels, p = aut(a)
        channels = [ [] for c in range( nchannels) ]
        for data in dataiter(p):
            for i,ch in enumerate( channels):
                c = data.channel(i)
                ch.extend( c.frame(j)[0]
                            for j in range( c.frames))
        print( len( channels),
                [ len(c) for c in channels],
                [ c[12345] for c in channels],
                )

    def aut_frames( a):
        nchannels, p = aut(a)
        fms = []
        for data in dataiter(p):
            fms.extend( tuple( data.frame(j))
                for j in range( data.frames)
                )
        #too much memory = nsamples*sizeof(tuple+2*int)
        print( len( fms), fms[12345])

    def aut_channels_raw( a):
        nchannels, p = aut(a)
        channels = [ [] for c in range( nchannels) ]
        for data in dataiter(p):
            data = list( data)
            for i,ch in enumerate( channels):
                ch.extend( data[i::nchannels] )
        print( len( channels),
                [ len(c) for c in channels],
                [ c[12345] for c in channels],
                )

    def _pcm_raw( reader, nchannels):
        import numpy, ctypes
        channels = [ [] for c in range( nchannels) ]
        for dats, sizer in reader():
            for dat,c in zip( dats, channels ):
                if sizer is None:
                    c.append( dat)
                else:
                    sz = int( sizer(dat) if callable(sizer) else sizer)
                    c.append( ctypes.string_at( dat, sz))

        #print( [[len( i) for i in c[:5]] for c in channels] )
        #print( list(z))
        #print( channels[0][0] )
        channels = [ numpy.fromstring( b''.join(c) , dtype='<i2') for c in channels ]
        if nchannels>1:
            if not len(channels[1]):
                r = channels[0].reshape( -1, nchannels)
            else:
                r = numpy.column_stack( channels)   #same as .transpose( .vstack( channels))
        else:
            r = channels[0]
        print( nchannels, r.shape, r[12345], )
        return
        for i in range( len(r)):
            if (0 not in r[i] if r.ndim>1 else r[i]):
                print( i, r[i:i+20].T)
                break


    def avpy_pcm_raw( a):
        '''FIXME:
            in avpy/version/av11.py: wrong key of avresample_* = _libraries[ 'libavcodec.so'] ; must be 'libavresample.so'
           no resample
        '''
        #https://pypi.python.org/pypi/Avpy  pip  https://bitbucket.org/sydh/avpy
        import numpy, ctypes
        import avpy
        m = avpy.Media( a)
        #print( m.info())
        #TODO: get first audio stream
        sinfo = m.info()['stream'][0]
        nchannels = sinfo['channels']
        print( nchannels, sinfo['sampleRate'], sinfo['sampleFmt'] )
        sampleFmt = str(sinfo['sampleFmt']).lower()

        pnchannels = sampleFmt.endswith('p') and nchannels or 1 #*p=planar, then LLLLL,RRRRR as tuple; else LRLRLRLRLR
        def looper():
            x = 10
            for pkt in m:
                pkt.decode()
                if x<3: print( pkt.frame.contents.nb_samples )
                x += 1
                yield pkt.frame.contents.data[:pnchannels], pkt.dataSize / pnchannels
        return _pcm_raw( looper, nchannels)

    def myff_pcm_raw( a, resample =None):
        '''FIXME:
            no py3

            in ffmpegmodule.c:
                PyModule_AddIntMacro( module, AV_CH_LAYOUT_MONO );

            in ffmpeg.py:
                from _ffmpeg import AV_CH_LAYOUT_MONO
                fix print + except DecodeError (for py3)

            rf.get_channel_layout() does not work
        '''
        # http://bitbucket.org/Svedrin/failplay/src/tip/myffmpeg  old:https://pypi.python.org/pypi/myffmpeg
        import numpy, ctypes
        import ffmpeg
        rf = ffmpeg.LowLevelDecoder( a)
        nchannels = rf.get_channels()
        input_rate  = rf.get_samplerate()
        input_fmt   = rf.get_samplefmt()
        input_layout = rf.get_channel_layout()
        if not input_layout:
            assert nchannels in (1,2),nchannels
            input_layout = ffmpeg.AV_CH_LAYOUT_MONO if nchannels ==1 else ffmpeg.AV_CH_LAYOUT_STEREO
        print( nchannels, input_rate, input_fmt, input_layout, rf.get_codec(),
                rf.get_duration(), #rf.get_bitrate(), #rf.get_metadata(), #rf.get_path()
                )

        if resample:
            org = dict(
                input_rate  = input_rate,
                output_rate = input_rate,
                input_sample_format = input_fmt,
                output_sample_format= input_fmt,    #AV_SAMPLE_FMT_S16
	            input_channel_layout= input_layout,
	            output_channel_layout=input_layout, #AV_CH_LAYOUT_STEREO AV_CH_LAYOUT_MONO
	        #   filter_length=16, log2_phase_count=10, linear=0, cutoff=1
                )
            rrate = resample.get('rate',     input_rate)
            kargs = dict( org, output_rate= rrate )
            if resample.get('s16', False):
                kargs.update( output_sample_format = ffmpeg.AV_SAMPLE_FMT_S16 )
            rnchannels  = resample.get('channels', nchannels)
            if nchannels != rnchannels:
                assert rnchannels in (1,2), rnchannels
                kargs.update( output_channel_layout = ffmpeg.AV_CH_LAYOUT_MONO if rnchannels==1 else ffmpeg.AV_CH_LAYOUT_STEREO )
                nchannels = rnchannels
            if kargs != org:
                resample = ffmpeg.Resampler( **kargs).resample
            else: resample = None

        def looper():
            x=10
            while True:
                try:
                    data = rf.read()
                except StopIteration: break
                if x<3: print( len(data[0]))
                x+=1
                if resample: data = resample( data)
                yield data, None#len
        return _pcm_raw( looper, nchannels)

    def myff_pcm_raw_resamp( a):
        return myff_pcm_raw( a, resample= dict( s16=True,
                channels=1,
                rate=44100/5,
            ))

    def av_pcm_raw( a, resample =None):
        ''' FIXME:
        py3: setup.py : def library_config(name): ..after getting raw_config
            try: unicode    #py2
            except:
                import sys
                raw_config = raw_config.decode( sys.stdout.encoding)

          but then at av.open() : UnicodeEncodeError: 'ascii' codec ...
              str isnt autoconverted to cdef bytes..
              so only works for ascii filenames+paths
        '''
        #https://github.com/mikeboers/PyAV newer than https://pypi.python.org/pypi/av/0.2.2
        import av
        import numpy, ctypes
        if resample:
            resample = av.AudioResampler(
                    format= av.AudioFormat('s16').packed,
                    layout= 'stereo',
                    rate= resample.get( 'rate') or 0,
                ).resample
            #TODO try it

        container = av.open(a)
        stream = next(s for s in container.streams if s.type == 'audio')
        print( stream.channels, stream.rate, stream.format.name, )
        nchannels = stream.channels
        def looper():
            x=10
            for packet in container.demux(stream):
                for frame in packet.decode():
                    #XXX to_bytes() rounds up data to 128. cut it back
                    data = [ p.to_bytes() #[: 2*frame.samples * (nchannels if nchannels > len(frame.planes) else 1) ]
                                for p in frame.planes ]#[:pnchannels] ]
                    if x<3: print( frame.samples, frame.format.name, frame.layout.name, 'planes', len(frame.planes), frame ,
                        [len( d) for d in data]
                        )
                    x+=1
                    #yield pi, fi, frame
                    #print( len(data))
                    yield data, None
        return _pcm_raw( looper, nchannels)

    def libsndfile( a):
        ''' no mp3. py3 doesnt work. cygwin dies half-way
         svn checkout http://pyzic.googlecode.com/svn/trunk/libsndfile-ctypes/libsndfilectypes
         libsndfilectypes.libsndfile.py:

         +  libName = 'sndfile'
         !  dllName = 'lib'+libName+'-1'    cygwin: 'cyg'+libName+'-1'

            _lib=None
            try:
                from ctypes.util import find_library
                #does the user already have lib installed?
         +      dllPath = find_library( libName) #*nix #dllName.split('-')[0].split('lib',1)[-1] )
         +      if not dllPath:
         !          dllPath = find_library(dllName)
                ...

        '''
        import numpy
        from libsndfilectypes.libsndfile import SndFile

        with SndFile( a) as sndf :
            nchannels = sndf.nbChannels
            data, succ = sndf.read( None and 4096*64, numpy.int16)
            assert succ == data.shape[0]
            print( nchannels, data.shape, data[ 12345] )

    import timeit, gc
    if 10:
        def garbager():
            gc.enable()
            gc.collect()
        for fn in [
                #libsndfile,
                myff_pcm_raw, #myff_pcm_raw_resamp,
                #av_pcm_raw,
                #avpy_pcm_raw,       #ok py3 +py2
                aut_channels_raw,
                    #aut_channels,
                    #aut_frames,    #slow,memory-hog
                  ] [:]:
            try:
                t = timeit.timeit( lambda : fn( a) , garbager, number=1 )
            except:
                t=None
                import traceback
                traceback.print_exc()
            print( '-', fn.__name__, t)
            gc.collect()


'''
speed comparison any-audio into python :

.flac:
aut_channels 36.6
aut_frames 48.0
aut_channels_raw 12.0

.flac 2 44100 s16 1344.5
- av_pcm_raw 4.1
- myff_pcm_raw 3.9
- avpy_pcm_raw 4.2
- aut_channels_raw 13.3
- aut_channels 54.2
- aut_frames 75.0

.flac.mp3 2 44100 s16p 1344.5
- av_pcm_raw 7.0
- myff_pcm_raw 6.7
- avpy_pcm_raw 7.7
- aut_channels_raw 8.8

.wav 2 44100 s16 1344.5
- av_pcm_raw 1.9
- myff_pcm_raw 1.5
- avpy_pcm_raw 2.6
- aut_channels_raw 6.9

.wav 1 16000 s16 1344.5
- av_pcm_raw 0.8
- myff_pcm_raw 0.4
- avpy_pcm_raw 0.8
- aut_channels_raw 1.1
- aut_channels 8.8
- aut_frames 22.3

.flac 2 44100 s16 5128.4
- libsndfile 7.0
- myff_pcm_raw 8.9
- av_pcm_raw 10.7
- avpy_pcm_raw 11.6

'''

# vim:ts=4:sw=4:expandtab

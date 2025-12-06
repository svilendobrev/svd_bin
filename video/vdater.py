#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
import sys,re,subprocess,tempfile
import datetime, os

import optparse
oparser = optparse.OptionParser(
    description= 'get dates of videofiles into *.dt OR set dates of videofile from *.dt',
    usage= '%s [options] f_in [f_out]'
)
def optany( name, *short, **k):
    return oparser.add_option( dest=name, *(list(short)+['--'+name.replace('_','-')] ), **k)
def optbool( name, *short, **k):
    return optany( name, action='store_true', *short, **k)
optbool( 'tz_local', help= 'use local timezone')
optbool( 'inner',   help= 'use inner creatime, instead of from-filename')
optbool( 'dateset', help= 'set date to videofile ; default is get date')
optbool( 'many',    help= 'many in-files of same kind, guess out-files')
optz,args = oparser.parse_args()

set_local_tz = optz.tz_local
use_inner_datetime = optz.inner
dt2v = optz.dateset
many = optz.many

def touch( fo, creatime):
    a_secs = creatime.split('.')[0]
    try:
        dt = datetime.datetime.strptime( a_secs, '%Y-%m-%d' 'T' '%H:%M:%S',)
    except ValueError:
        dt = datetime.datetime.strptime( a_secs, '%Y-%m-%d' 'T' '%H:%M',)

    if optz.tz_local:
        dt = dt.replace( tzinfo= datetime.timezone.utc ).astimezone()
        print( ' >>', dt)

    t = dt.timestamp()
    os.utime( fo, (t,t) )


def do( fi, fo ):
    if not fo and dt2v:
        fo = fi
        fi = os.path.splitext( fo)[0]+'.dt'

    if fi.lower().endswith('.dt'):
        fromdt = True
        try:
            creatime = open(fi).readlines()[0]
        except:
            fo0 = re.split( r'\.\.w\d+\.', fo)[0]
            if fo0 == fo: raise
            fi = os.path.splitext( fo0)[0]+'.dt'
            creatime = open(fi).readlines()[0]
        #assert fo.endswith( '.mkv') or fo.endswith('.avi'), fo
    else:
        fromdt = False
        dt_tm = re.search( r'(?P<Y>\d{4})(?P<M>\d{2})(?P<D>\d{2})_(?P<h>\d{2})(?P<m>\d{2})(?P<s>\d{2})', fi)
        dt_tm = dt_tm or re.search( r'(?P<Y>\d{4})(?P<M>\d{2})(?P<D>\d{2})(?P<h>\d{2})(?P<m>\d{2})(?P<s>\d{2})_\d{4}', fi)
        if not use_inner_datetime and dt_tm:
            creatime = '{Y}-{M}-{D}T{h}:{m}:{s}.000000Z'.format( **dt_tm.groupdict())
        else:
            creatime = subprocess.check_output( [ 'ffprobe', '-hide_banner', fi ],
                stderr= subprocess.STDOUT
                ).decode('cp1251', 'ignore')
            creatime = [ l for l in creatime.split('\n') if 'creation_time' in l ][0]
            creatime = creatime.split(': ',1)[-1]
        if not fo:
            fo = os.path.splitext( fi)[0]+'.dt'

    creatime = creatime.strip()
    print( '>>', creatime, fo)

#tz = datetime.datetime.now().astimezone().tzinfo   same as supplying None

    if fo.endswith( '.mkv'):
        with tempfile.NamedTemporaryFile( suffix='.xml', ) as fxml:
            fxml.write( f'''\
        <?xml version="1.0"?>
        <!-- <!DOCTYPE Tags SYSTEM "matroskatags.dtd"> -->
        <Tags>
          <Tag>
            <Targets />
            <Simple>
              <Name>creation_time</Name>
              <String>{creatime}</String>
            </Simple>
          </Tag>
        </Tags>
        '''.encode('ascii'))
            fxml.seek(0)

            subprocess.check_output( ['mkvpropedit', fo, '--tags', 'all:'+fxml.name ] )     #ignore/hide output
        touch( fo, creatime)

    elif fo.endswith( '.avi'):
        ffo = fo+'.avi'
        subprocess.call( 'ffmpeg -hide_banner -y -i'.split() + [ fo,
                        ] + '-acodec copy -vcodec copy -metadata'.split() + [
                            'date='+creatime, ffo] )   #date->ICRD recognized only
        touch( ffo, creatime)

    elif fo.endswith( '.mp4'):
        ffo = fo+'.mp4'
        subprocess.call( 'ffmpeg -hide_banner -y -i'.split() + [ fo,
                        ] + '-acodec copy -vcodec copy -metadata'.split() + [
                            'creation_time='+creatime, ffo] )
        touch( ffo, creatime)

    elif fromdt:
        touch( fo, creatime)

    else:
        assert fo.lower().endswith('.dt'), fo
        with open(fo,'w') as o:
            o.write( creatime )


if many:
    for fi in args:
        do( fi, None)
else:
    fi,fo = (args[:2]+[ None ])[:2]
    do( fi, fo)


# vim:ts=4:sw=4:expandtab

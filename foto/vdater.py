#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

import sys,re,subprocess,tempfile
import datetime, os

set_local_tz = False
for a in ['-tz', '--tz']:
    if a in sys.argv:
        sys.argv.remove( a)
        set_local_tz = True

use_inner_datetime = False
for a in ['-inner', '--inner']:
    if a in sys.argv:
        sys.argv.remove( a)
        use_inner_datetime = True

dt2v = False
for a in ['-dt', '--dt']:
    if a in sys.argv:
        sys.argv.remove( a)
        dt2v = True

fi,fo = (sys.argv[1:3]+[ None ])[:2]
if not fo and dt2v:
    fo = fi
    fi = os.path.splitext( fo)[0]+'.dt'

if fi.lower().endswith('.dt'):
    fromdt = True
    try:
        creatime = open(fi).readlines()[0]
    except:
        fo0 = re.split( '\.\.w\d+\.', fo)[0]
        if fo0 == fo: raise
        fi = os.path.splitext( fo0)[0]+'.dt'
        creatime = open(fi).readlines()[0]
    #assert fo.endswith( '.mkv') or fo.endswith('.avi'), fo
else:
    fromdt = False
    dt_tm = re.search( '(?P<Y>\d{4})(?P<M>\d{2})(?P<D>\d{2})_(?P<h>\d{2})(?P<m>\d{2})(?P<s>\d{2})', fi)
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

def touch( fo, creatime):
    a_secs = creatime.split('.')[0]
    try:
        dt = datetime.datetime.strptime( a_secs, '%Y-%m-%d' 'T' '%H:%M:%S',)
    except ValueError:
        dt = datetime.datetime.strptime( a_secs, '%Y-%m-%d' 'T' '%H:%M',)

    if set_local_tz:
        dt = dt.replace( tzinfo= datetime.timezone.utc ).astimezone()
        print( ' >>', dt)

    t = dt.timestamp()
    os.utime( fo, (t,t) )

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

elif fromdt:
    touch( fo, creatime)

else:
    assert fo.lower().endswith('.dt'), fo
    with open(fo,'w') as o:
        o.write( creatime )

# vim:ts=4:sw=4:expandtab

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

fi,fo = (sys.argv[1:3]+[ None ])[:2]

if fi.lower().endswith('.dt'):
    creatime = open(fi).readlines()[0]
    assert fo.endswith( '.mkv') or fo.endswith('.avi'), fo
else: #if fi.lower().endswith('.mov'):
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

else:
    assert fo.lower().endswith('.dt'), fo
    with open(fo,'w') as o:
        o.write( creatime )

# vim:ts=4:sw=4:expandtab

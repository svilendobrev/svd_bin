import sys
import datetime, calendar, time
import os.path
from svd_util import optz, datetimez
optz.text( 'year')
optz.text( 'hour')
optz.bool( 'ilocal')
optz.bool( 'olocal')
optz.bool( 'fake', '-n' )
optz,args = optz.get()

def delta( dt, what):
    v = getattr( optz, what)
    if v:
        iv = int(v)
        if v[0].isdigit():
            dt = dt.replace( **{ what: iv })
        else:
            if what == 'hour':
                what = 'seconds'
                iv = 3600*iv
            dt = dt + datetime.timedelta( **{ what: iv })
    return dt

for a in args:
    d = os.path.getmtime(a)

    dti = datetimez.timestamp2datetime( d, local= optz.ilocal)
    dt = dti
    dt = delta( dt, 'year')
    dt = delta( dt, 'hour')

    t = datetimez.datetime2timestamp( dt, local= optz.olocal)
    print dti, dt, d, t
    if not optz.fake:
        os.utime( a, (t,t))


import datetime
def days_epoch( *a):
    d = datetime.datetime( *a)
    print d
    r = d.toordinal()  - datetime.datetime( 1970,1,1).toordinal()
    return d,r #* 24*3600

def sec( *a):
    d,r = days_epoch( *a)
    hr = r*24 + d.hour
    sec = (hr*60 + d.minute)*60 + d.second
    return sec

def prn( s):
    s *= 1000   #msec
    x = '%x' % s
    y = ' '.join( [ x[-12:-8], x[-8:-4], x[-4:] ] )
    print x, ':', y

def p( *a,**k):
    return prn( sec( *a,**k))

import sys
if not sys.argv[1:]: print 'args: year month day [hour [min [sec]]]'
#else: p( *(int(x) for x in sys.argv[1:] ) )
else: p( *(map( int, sys.argv[1:] ) ))

#!/usr/bin/env python

import sys
import re
import subprocess, os

from util import optz
optz.bool(  'dryrun', '-n', )
optz.bool(  'verbose', '-v', )
optz.bool(  'autoon',  )
optz.bool(  'nomenu',  )
optz.bool(  'noscan',  )
optz.bool(  'crypto',  '-c' )
optz.text(  'iface',  default= 'wlan0' )    #ath0
optz.text(  'essid',  )
optz,args = optz.get()

o_n = optz.dryrun
o_v = optz.verbose
o_menu = not optz.nomenu
o_scan = not optz.noscan
with_crypt = optz.crypto #opt('-c', '--crypt', '--crypto')

iface = optz.iface or 'ath0'

res = dict(
    addr   = re.compile( 'Cell.*? - Address: ([0-9A-F:]+)' ),
    essid  = re.compile( 'ESSID:"([^"]*)"' ),
    quality= re.compile( 'Quality[=:](\d+)/(\d+)' ),
    crypto = re.compile( 'Encryption key:(on|off)' ),
)
'''$iwlist scan
    Cell 04 - Address: 00:80:48:37:8B:01
          ESSID:"ACH.ZeroConfig.GR"
          Mode:Master
          Frequency:2.437 GHz (Channel 6)
          Quality=17/94  Signal level=-78 dBm  Noise level=-95 dBm
          Encryption key:off
          Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s
                    12 Mb/s; 48 Mb/s
          Extra:bcn_int=100
'''
all = []
d = None
input = sys.stdin
if optz.autoon:
    # from /etc/acpi/wlan.sh
    fn = '/proc/acpi/asus/wlan'
    on = file( fn).read().strip()
    if on == '0':
        echoon = 'sudo sh -c'.split() + [ '"echo 1 > %(fn)s:"' % locals() ]
        subprocess.Popen( echoon).wait()
        import time
        time.sleep( 2)    #2

if optz.essid:
    all = [ dict( essid=optz.essid, crypto=True)]
else:
    if o_scan:
        ifc = 'sudo ifconfig'.split() + [ iface, 'up']
        subprocess.Popen( ifc).wait()
        input = subprocess.Popen( ['sudo', 'iwlist', iface, 'scan' ], stdout= subprocess.PIPE
                    ).communicate()[0].split('\n')

    for a in input:
        a = a.strip()
        for k in ['addr'] + [ q for q in res.keys() if q !='addr']:
            v = res[k]
            m = v.search( a)
            if not m: continue
            v = m.group(1)
            if k == 'addr':
                d = {}
                all.append(d)
                print '---' #k,v
            elif k == 'quality':
                v = int( int(m.group(1)) / float(m.group(2)) * 100)
            elif k == 'crypto':
                v = (v.lower() != 'off')
                if v: print 'crypto'
            elif k in 'essid'.split():
                print k,v
            d[k] = v

    if not with_crypt:
        all = [ d for d in all if not d['crypto'] ]

    all.sort( key= lambda d: (d['quality'],d['essid']) )
    all.reverse()

    def strval( k,v, both=False):
        if isinstance(v,bool): return v and k or ''
        if both: return '%s=%s' % (k,v)
        return str(v)

    def strvalues(a,keys, both=False):
        return '  '.join( strval(k,a[k],both=both) for k in keys )

    keys = 'quality crypto essid addr'.split()
    if not o_menu:
        for a in all: print strvalues(a,keys,both=True)

iface_def = '''
iface %(iface_name)s inet manual
    down dhclient -r -pf /var/run/dhclient.$IFACE.pid -lf /var/run/dhclient.$IFACE.leases $IFACE
    down ifconfig $IFACE down
%(wpa_stuff)s
    up ifconfig $IFACE up
    up dhclient -cf /etc/dhcp3/dhclient.$LOGICAL.conf -pf /var/run/dhclient.$IFACE.pid -lf /var/run/dhclient.$IFACE.leases $IFACE
    wireless-essid %(essid)s
'''

wpa_conf  = '/etc/wpa_supplicant.conf'
wpa_stuff = '''
    up wpa_supplicant -B -Dwext -i$IFACE -c %(wpa_conf)s
    up wpa_cli reassociate
''' % locals()

adict = dict( (a['essid'], a) for a in all)

if o_menu and all:
    if len(all)==1:
        essid = all[0]['essid']
    else:
        cmd = ['dialog' ] #+ sys.argv[1:]
        #if o_menu == '-checklist': cmd += ['--separate-output']
        cmd += [ '--menu', #or '--checklist',
            iface, 0, 60, 16
        ]
        for a in all:
            cmd += [ a['essid'], strvalues( a, ['quality']+['crypto']*bool(with_crypt)) ]
        cmds = [str(c) for c in cmd]
        print cmds
        essid = subprocess.Popen( cmds, stderr= subprocess.PIPE
                ).communicate()[1]  #communicate does wait
    if essid:
        print 'choice:', essid

        verbose = o_v and '--verbose' or ''

        tmp_ifaces_fn = '/tmp/iw.py.tmp'
        iface_name = 'iw'
        ifdn = 'sudo ifdown --verbose'.split() + [ iface]
        print ifdn
        if not o_n:
            r = subprocess.Popen( ifdn)
            r.wait()
            print '-------', r.returncode
        a = adict[essid]
        if a['crypto']:
            #wpa_conf = wpa_conf % locals()
            assert essid in file( wpa_conf).read(), 'no network %(essid)s in file %(wpa_conf)s; use wpa_passphrase to make it' % locals()
            wpa_stuff = wpa_stuff % locals()
            print wpa_stuff
        else: wpa_stuff = ''
        tmptext = iface_def % locals() #channel=
        if not o_n:
            tmp = file( tmp_ifaces_fn, 'w')
            tmp.write( tmptext)
            tmp.close()
            #print tmptext
        else:
            print '>', tmp_ifaces_fn, '\n', tmptext

        ifup = ('sudo ifup %(verbose)s -i %(tmp_ifaces_fn)s %(iface)s=%(iface_name)s' % locals() ).split()
        print ifup
        if not o_n: os.execvp( ifup[0], ifup)


def update_interfaces( name, essid, channel =None):
    found = done = 0
    r = []
    for l in file( '/etc/network/interfaces'):
        l = l.rstrip()
        if not done:
            ls = l.split()
            if ls[:1] == ['iface']:
                if found: done = 1
                if ls[1] == name: found+=1
            elif found:
                if ls[:1] == ['wireless-essid']:
                    l = '  ' + ls[0] +' '+ essid
                elif channel is not None and ls[:1] == ['wireless-channel']:
                    l = '  ' + ls[0] +' '+ str( channel)
        r.append( l)
        #print l
    if not found:
        r += (iface_def % locals() ).split('\n')
    return r
#r = update_interfaces( 'walk', 'bozaa')

# vim:ts=4:sw=4:expandtab

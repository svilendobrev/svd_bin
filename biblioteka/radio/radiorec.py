#!/usr/bin/python3

import datetime, subprocess, sys, time
import os.path
from svd_util import optz
optz.int( 'seconds', '-s', default= 0, help= 'this has priority over --minutes' )
optz.int( 'retry_n', default= 1 )
optz.int( 'retry_delay_seconds', default= 20 )
optz.int( 'minutes', '-m', default= 6, help= 'this only if no --seconds specified' )
optz.int( 'extra_seconds', default= 3 )
optz.str( 'stream', default= 'http://stream.bnr.bg:8003/botev.mp3')
                #'http://streaming.bnr.bg/HristoBotev'

optz.str( 'stream2', default ='')
optz.str( 'fname',   default= '', help= 'output-fname, appended -bk if stream2 and -rec if recorder')
optz.multi( 'exec',  default= [], help= 'use syntax of find(1) - outfname is {} ; can be multiple times' )
optz.str( 'logfname', )
optz.bool( 'quiet',   help= 'silent the player/recorder, eventually')
optz.str( 'recorder', help= 'run this instead of mplayer, a str{}-template with 2 given kargs: {ofname} {stream}')

from svd_util.py.wither import wither

def prn( *a,**ka):
    print( file= sys.stderr, *a,**ka)
    sys.stderr.flush()
def prndict( d, key=None, exclude =()):
    return ', '.join( k+'= '+repr(v) for k,v in sorted( d.items(), key=key) if k not in exclude)

def rec( o, *, fname, secs, mins, stream ):
    now = datetime.datetime.now().strftime( '%Y%m%d.%H.%M.%S')
    prn('#', prndict( locals(), exclude= ['o'] ))
    prn('#optz', prndict( o.__dict__))
    if not fname:
        fname = stream.split('://')[-1].replace('/','_')
    ofname = [fname, now, ]
    if o.stream2: ofname.append( 'bk')
    if o.recorder: ofname.append( 'rec')
    ofname = '-'.join( ofname
        ).replace( ' ', '_' #just in case
        ).replace( ':', ''  #mplayer codec-options separator
        ).replace( ',', ''  #also
        ) + '.wav'

    sz_seconds = (secs or mins*60)
    assert sz_seconds

    #wave.getparams()
    #(1, 2, 44100, 1474560,
    #(nchannels, sampwidth, framerate, nframes,
    #sz_bytes = 1*2*44100* sz_seconds
    #    '-endpos', str(sz_bytes)+'b',

    if o.recorder:
        cmd = [ s.format( ofname=ofname, stream=stream) for s in o.recorder.split() ]
    else:
        cmd = 'mplayer -vc null -vo null -ao'.split() + [
            'pcm:fast:file='+ ofname,
            stream,
            '-nocache',
          ]
        if o.quiet: cmd.append( '-quiet')

    timewait = sz_seconds + o.extra_seconds
    prn( '#rec', timewait, 's', ' '.join( cmd))

    with (o.logfname and open( o.logfname, 'a') or wither) as out:
        retry_n = max( o.retry_n, 1)
        returncode = 13
        while True:
            with subprocess.Popen(  #needs python3.2 at least
                cmd,
                stdin= subprocess.PIPE,
                stderr= out, #o.logfname and subprocess.STDOUT or None,
                stdout= out,
            ) as p:
                #try new TODO.. use -endpos xxx option?
                while p.poll() is None: #p.returncode
                    if timewait>0:
                        tw = min( 2, timewait)
                        time.sleep( tw)
                        #prn('#sleep', timewait)
                        timewait -= tw
                    else:
                        if not o.recorder:
                            p.communicate( input= b'q')
                        else:
                            #prn( '#stop')
                            #p.communicate( input= b'\3')
                            p.terminate()
                            #p.kill()
                        returncode = False  #OK
                        break
                else:
                    returncode = p.returncode

            if returncode or os.path.exists( ofname) or retry_n<=1:
                break

            retry_n -= 1
            prn( '#retry', retry_n)
            time.sleep( o.retry_delay_seconds)

        if o.exec:
            for exec in o.exec:
                exec = exec.replace( '{}', ofname)
                cmds = exec.split()
                with subprocess.Popen(  #needs python3.2 at least
                    cmds,
                    stderr= out,
                    stdout= out,
                ) as p:
                    p.wait()

o,args = optz.get()
if o.stream2 != o.stream: #HACK за да не се сравнява в radiorec.sh-script ..
    rec( o, fname= o.fname, secs= o.seconds, mins= o.minutes,
        stream = o.stream2 or (args[0] if args else o.stream) )

#!/usr/bin/python3

import datetime, subprocess, sys, time
import os.path
from util import optz
optz.int( 'seconds', '-s', default= 0 )
optz.int( 'retry_n', default= 1 )
optz.int( 'retry_delay_seconds', default= 20 )
optz.int( 'minutes', '-m', default= 30 )
optz.int( 'seconds_extra', default= 3 )
optz.str( 'stream', default= 'http://stream.bnr.bg:8003/botev.mp3'
                #'http://streaming.bnr.bg/HristoBotev'
            )
#optz.str( 'stream', default= 'http://streaming.bnr.bg/Horizont' )
optz.str( 'fname',  default= '' )
optz.multi( 'exec',  default= [], help= 'in syntax of find - outfname is {} ; can be multiple times' )
optz.str( 'logfname', )
optz.bool( 'quiet_mplayer', )

from util.py.wither import wither

def rec( o, *, fname, secs, mins, stream ):
    now = datetime.datetime.now().strftime( '%Y%m%d.%H.%M.%S')
    if not fname:
        fname = o.stream.split('://')[-1].replace('/','_')

    ofname = '-'.join( [fname, now, ]
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

    cmd = 'mplayer -vc null -vo null -ao'.split() + [ 'pcm:fast:file='+ ofname,
            stream,
            '-nocache',
          ]
    if o.quiet_mplayer:
        cmd.append( '-quiet')

    timewait = sz_seconds + o.seconds_extra
    print( '#rec', timewait, 's', ' '.join( cmd), file= sys.stderr)

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
                while p.poll() is None: #p.returncode
                    if timewait>0:
                        tw = min( 2, timewait)
                        #print( 1111111111, tw)
                        time.sleep( tw)
                        timewait -= tw
                    else:
                        p.communicate( input= b'q')
                        #p.terminate()
                        returncode = False  #OK
                        break
                else:
                    returncode = p.returncode
            #print( 22222222222, returncode)

            if returncode or os.path.exists( ofname) or retry_n<=1:
                break

            retry_n -= 1
            print( '#retry', retry_n)
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
rec( o, fname=o.fname, secs= o.seconds, mins= o.minutes, stream =o.stream, )

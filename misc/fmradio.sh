#!/bin/sh
#run instead of shell inheriting PID etc
exec /usr/local/bin/softfm -f 104800000 -r 44100 -W "$1" $2

#ne: rtl_fm -f 104.8e6 -M wbfm -s 400000 -r 48000 | sox -t raw -r 48000 -es -b 16 - -r 44100 -c 2 share/bbaa.flac
#da:
#git clone https://github.com/jorisvr/SoftFM
#cd SoftFM/
#nd build
#cmake ..

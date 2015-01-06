#!/bin/sh
#for a in "$@"; do echo "$a"; ffprobe -hide_banner "$a" |& grep -i audio; done
filmid.sh "$@" | grep -i '(input|audio)'
# | grep -v stereo |l


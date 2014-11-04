#!/bin/sh
#|Genre
#mplayer -vo null -ao null -frames 0 -msglevel identify=4 "$@" 2>/dev/null | grep -E '((VIDEO|AUDIO|Title|Artist|Album|Year|Comment): *[^ ]+|Playing|ID_(LENG|VIDEO_[HW])|Track|[sa]lang|subtitle|^VIDEO )'
for a in "$@"; do ffprobe -hide_banner "$a"; done 2>& 1

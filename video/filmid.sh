#!/bin/bash
#|Genre
#mplayer -vo null -ao null -frames 0 -msglevel identify=4 "$@" 2>/dev/null | grep -E '((VIDEO|AUDIO|Title|Artist|Album|Year|Comment): *[^ ]+|Playing|ID_(LENG|VIDEO_[HW])|Track|[sa]lang|subtitle|^VIDEO )'
PWD=`pwd`
for a in "$@"; do
 [[ ! "$a" =~ ^/ ]] && a="$PWD/$a"
 ffprobe -hide_banner file://"$a" 2>&1
done

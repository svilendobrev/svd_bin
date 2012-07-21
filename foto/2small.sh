#!/bin/sh
#../src/fit2print.py --cjpeg= --djpeg --size=800x600,pixels --autooutpfx=small/ "$@"
#`dirname $0`/fit2print.py --cjpeg= --djpeg --size=1024x768,pixels --exifcopy --autooutpfx=small/ "$@"
_SCALE=${SCALE:-2}

if false ; then
__SCALE=-$_SCALE
test "$_SCALE" = "1" && __SCALE=
$E `dirname $0`/fit2print.py --cjpeg= --djpeg $__SCALE --exifcopy --autooutpfx=$_SCALE/ "$@"

else

mkdir -p $_SCALE
test "$_SCALE" = "1" && __SCALE= || __SCALE="-scale 1/$_SCALE"
for a in "$@"; do
 echo ==="$a"
 djpeg $__SCALE "$a" | cjpeg -q ${Q:-90} -progressive -optimize >$_SCALE/"$a"
 jhead -te "$a" -dt $_SCALE/"$a"
 test -n "$AUTOROT" && jhead -autorot $_SCALE/"$a"
done

fi

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
 b=`echo $_SCALE/"$a" | sed -e s/jpg$/$_SCALE.jpg/`
 mkdir -p "$b"
 rmdir "$b"
 djpeg $__SCALE "$a" | cjpeg -q ${Q:-90} -progressive -optimize >"$b"
 jhead -te "$a" -dt "$b"
 test -n "$AUTOROT" && jhead -autorot "$b"
done

fi

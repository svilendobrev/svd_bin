#!/bin/sh
scale=$1
shift
#echo "$0 imagefile downscale(2,4,8) flip(-cw,-ccw,none)"
#echo "scale=$2 flip=$3"

for a in "$@"; do
 out=`echo "$a" | sed "s/\.jpg/\.$scale\.jpg/"`
 echo "$a -> $out"

#	save only exif as binary:
#jpegtopnm -exif=- $in >outfile
#	exif as text > stderr:
#jpegtopnm -exif=- -dumpexif $in >/dev/null

 djpeg -pnm -scale 1/$scale "$a" | cjpeg -quality 90 >"$out"
#pnmflip $flip |
 jhead -te "$a" -dt "$out"
done

#quality 90->95:  filesize * 1.5

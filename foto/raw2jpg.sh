#!/bin/sh
# -w : white balance from camera
# -c : stdout
# -e : get thumbnail only
# -i -v : metainfo

#dcraw -w $1	#.ppm
dcraw -c -e $1 >$1.thumb.jpg
#jhead
#maf j2j JEXT=ppm


#!/bin/bash

FILE_CRW=$1
REDUCE=$2
ICC=$3

[ -z "$REDUCE" ] && REDUCE=4
REDUCEdcr=
REDUCEpnm=
[ "$REDUCE" -ge 2 ] && REDUCEdcr=-h 
[ $REDUCE -gt 2 ] && let REDUCEpnm=$REDUCE/2 && REDUCEpnm="| pnmscale -r $REDUCEpnm"
NAME=`basename "$FILE_CRW"`
TMP_TIFF=/tmp/tmp-`basename "$FILE_CRW"`.tif
OUT=./icc2raw/


ALL_ICCs="/usr/1/foto/d60_linear_dcraw_profiles/*.icm /usr/1/foto/*.icc"
[ -z "$ICC" ] && ICC="$ALL_ICCs"

echo "raw2tiff $FILE_CRW /$REDUCE > $OUT | $ICC*"

#FLIP=(-cw,-ccw,none)"
FLIPpnm=
[ -n "$FLIP" ] && FLIPpnm="| pnmflip $FLIP"
#pnmflip $FLIP
#how to get it from EXIF?
 
#brightness: dcraw -b coef
#gamma correction?

#echo "$REDUCEdcr $REDUCEpnm"
#exit -1
mkdir -p $OUT
pipe="dcraw -4 -w $REDUCEdcr -c $FILE_CRW \
$REDUCEpnm \
$FLIPpnm \
| ppmnorm -bpercent 0.1 -wpercent 0.1 -brightmax \
| pnmtotiff -truecolor -color > $TMP_TIFF"
eval "$pipe"

for a in $ICC ; do 
	echo -ne " tiff2icc $a \r"
	tifficc -i "$a" "$TMP_TIFF" "$OUT/$NAME-`basename \"$a\"`.$REDUCE.tif"
done
crwinfo -t $OUT/$NAME-ikona.jpg $FILE_CRW 
echo "done          "

#sharpen (edge-enhance) : pnmnlfilt 0.4 0.8

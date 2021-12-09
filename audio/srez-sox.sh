#!/bin/sh
#-x
IN="$1" && shift
set -x
sox "$IN" "$IN".wav trim $@
#fname="$1"
#shift
#sox "$fname" "$fname".wav trim `python3 -c "import sys; print( *(a if a[0] in '=-+' else '='+a for a in sys.argv[1:]))" $@`
# play $1 trim =$2-4 4 =$3-4 4


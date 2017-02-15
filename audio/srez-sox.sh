#!/bin/sh -x
sox "$1" "$1".wav trim $2 $3
#fname="$1"
#shift
#sox "$fname" "$fname".wav trim `python3 -c "import sys; print( *(a if a[0] in '=-+' else '='+a for a in sys.argv[1:]))" $@`
# play $1 trim =$2-4 4 =$3-4 4


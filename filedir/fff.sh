#!/bin/sh -f
#oooh
#if no dbl quotes, a* is expanded on the find's line
#if dbl quotes added (as \"), a* is passed as "a*" WITH the quotes
#so use -f (or set -f, then +f) to avoid pathname expansion

_f="-name $1" ; shift
for a in "$@"; do _f="$_f -o -name $a"; done
#echo "$_f"
find . -follow \( -type f -o -type d \) \( $_f \)

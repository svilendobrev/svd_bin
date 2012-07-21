#!/bin/sh
for a in "$@"; do
 echo "$a"
 jpegtran -optimize -progressive -copy all "$a" >"$a".x
 mv -f "$a".x "$a"
done


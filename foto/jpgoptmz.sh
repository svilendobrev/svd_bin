#!/bin/sh
for a in "$@"; do
 echo "$a"
 jpegtran -optimize -progressive -copy all "$a" >"$a".x && rm -f "$a" && mv -f "$a".x "$a"
done


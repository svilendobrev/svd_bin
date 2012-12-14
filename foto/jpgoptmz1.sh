#!/bin/sh
a="$1"
if jhead "$a" | grep -qi progressive ; then echo ok "$a"
else
 echo "$a"
 jpegtran -optimize -progressive -copy all "$a" >"$a".x && rm -f "$a" && mv -f "$a".x "$a"
fi

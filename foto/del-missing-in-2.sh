#!/bin/sh
mkdir -p del
for a in "$@"; do [ -f 2/"$a" ] || $E mv -v "$a" del/; done
#for a in *.jpg; do [ -f 2/`basename "$a" .jpg`.2.jpg ] || $E rm -v  "$a"; done

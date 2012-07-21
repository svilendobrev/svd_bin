#!/bin/sh
chall.pl 's,^/\* *\d* *\*/ ,,;s,\n/\* *\d* *\*/ ,\n,g' "$@"

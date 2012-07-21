#!/bin/sh
if test -z "$__INSID" ; then
	export __INSID=1
	find "$@" -name \*jpg -exec $0 {} \;
else
	jhead "$1" | grep -q -i progressive || echo "$1"
fi

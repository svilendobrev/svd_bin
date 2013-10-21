#!/bin/sh
mkdir -p rot
for a in "$@"; do
 x=`jhead $a | grep Orientation`
 [ -n "$x" ] && jpegtran -rotate `echo $x | sed s/.*tate//` $a >rot/$a
done

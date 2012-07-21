#!/bin/sh
mkdir rot
for a in "$@"; do
 x=`jhead $a | g Orientation`
 [ -n "$x" ] && jpegtran -rotate `echo $x | sed s/.*tate//` $a >rot/$a
done

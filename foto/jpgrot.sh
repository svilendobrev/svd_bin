#!/bin/sh
for a in "$@"; do
 mkdir -p rot/"$a"
 rmdir rot/"$a"
 x=`jhead $a | grep Orientation`
 [ -n "$x" ] && jpegtran -rotate `echo $x | sed s/.*tate//` $a >rot/$a
done

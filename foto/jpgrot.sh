#!/bin/sh
ROT=$1
shift
for a in "$@"; do
 mkdir -p rot/"$a"
 rmdir rot/"$a"
# jpegtran -rotate $ROT "$a" >rot/"$a"
 jpegtran -rotate $ROT -optimize -progressive -copy all -outfile "rot/$a" "$a"
 echo $ROT == "rot/$a"
done

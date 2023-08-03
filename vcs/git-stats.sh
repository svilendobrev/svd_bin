#!/bin/sh
mkdir -p _stats
for a in [a-z]*/; do
 ./gitstats "$@" $a _stats/$a
 # -c start_date=value
 ( cd $a ;  ../git-commits-by-user.sh > ../_stats/$a/commits.txt )
done


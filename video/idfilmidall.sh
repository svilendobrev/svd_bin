#!/bin/sh
X="$@"
test -n "$X" || X=.
find $X -regextype posix-egrep \(    \
           -iregex ".*\.(avi|mkv|wmv|mov|ts|mpg|mp4|mpeg)" \
        -o -iregex ".*[^0-9]\.m2ts" \
        \)  \
        -exec $E idfilmid.sh "{}" \;

#        -o -iname \*.mkv \
#        -o -iname \*.wmv \
#        -o -iname \*.mov \
#        -o -iname \*.ts \

# vim:ts=4:sw=4:expandtab

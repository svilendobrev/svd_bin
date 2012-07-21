#!/bin/sh
#$Id: gconf-localepurge.sh,v 1.1 2006-10-05 15:59:36 sdobrev Exp $

test -z "$LANGok" && LANGok='C bg' # en en_GB
# add spaces at both ends!
export LANGok=" $LANGok "

#E=echo

DIR_USUAL=/etc/gconf/gconf.xml.defaults/
DIR=${1-$DIR_USUAL}

echo purging $DIR
cd $DIR

######### %gconf-tree-<LANG>.xml files
$E rm -f `perl -e '@f= grep( m/-(\w+)\.xml/ && $ENV{"LANGok"}!~/ $1 /, @ARGV); print join(" ",@f)' %gconf-tree-*.xml`

#for a in %gconf-tree-*.xml; do
#    for l in $LANGok; do
#        if test $a = %gconf-tree-$l.xml ; then
#            echo ok $a
#            continue 2
#        fi
#    done
#    $E rm $a
#done

############## schemas/*.xml files

#this may always match but will write only if there are changes
chall.pl 's!(<local_schema locale="(\S+)"[\s\S]*?/local_schema>\s*)!$p=$1,(($ENV{"LANGok"}=~/ $2 /) ? $p :"")!eg' `find schemas/ -type f`

chall.pl 's!(<locale name="(\S+)"[\s\S]*?/locale>\s*)!$p=$1,(($ENV{"LANGok"}=~/ $2 /) ? $p :"")!eg' *.schema

#    perl -ne 's!(<local_schema locale="(\S+)".*?>\n)!$p=$1,(($ENV{"LANGok"}=~/ $2 /) ? $p :"")!e; print' $a
# <local_schema locale="uk" short_desc=...

# vim:ts=4:sw=4:expandtab

#!/bin/sh
#$Id: gconf-localepurge.sh,v 1.1 2006-10-05 15:59:36 sdobrev Exp $

test -z "$LANGok" && LANGok='C bg' # en en_GB
# add spaces at both ends!
export LANGok=" $LANGok "

chall.pl 's!(<locale name="(\S+)"[\s\S]*?/locale>\s*)!$p=$1,(($ENV{"LANGok"}=~/ $2 /) ? $p :"")!eg' $@

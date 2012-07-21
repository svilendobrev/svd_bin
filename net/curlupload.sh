#!/bin/sh
#slowly 1-by-1
A1=$1
A2=$2
shift 2
if [ "$1" = "--1" ]; then
	shift
	X="curl --ftp-create-dirs -T $A1 $@ ftp://$A2/$A1"
	[ -f $A1.ok ] || (echo $X; $X && touch $A1.ok)
else
	echo "use: $0 $what ftp://usr:psw@where.to/go [-other -curl -options -here]"
	echo "     srvr.my/here is in homedir, srvr.my//here is root"
	Y="find $A1 -name *.ok -prune -o -type f -a -exec $0 {} $A2 --1 $@ ;"
	echo $Y
	$Y
fi

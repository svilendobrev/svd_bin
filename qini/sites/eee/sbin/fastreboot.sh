#!/bin/sh

if [ "$1" = "--ask" ]
then
	zenity --question && sudo $0
	exit $?
fi

[ `id -u` = "0" ] || echo "Must be root."

/usr/bin/killall --wait usbstorageapplet
/bin/umount /media/sdb1

/bin/kill -USR1 1

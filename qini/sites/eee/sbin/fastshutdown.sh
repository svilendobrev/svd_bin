#!/bin/sh

if [ "$1" = "--askNONONO" ]
then
	zenity --question && sudo $0
	exit $?
fi

[ `id -u` = "0" ] || echo "Must be root."

/usr/bin/killall --wait usbstorageapplet
/bin/umount /media/sdb1

/bin/kill -USR2 1

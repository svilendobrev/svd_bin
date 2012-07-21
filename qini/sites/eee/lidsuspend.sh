#!/bin/sh
#off: lidsuspend 0
#on : lidsuspend
if test $# == 0 -o -n "$1" -a "$1" != "0" ; then
	sudo chmod +x /etc/acpi/lidbtn.sh
else
	sudo chmod -x /etc/acpi/lidbtn.sh
fi

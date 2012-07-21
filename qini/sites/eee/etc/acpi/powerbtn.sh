#!/bin/sh
# /etc/acpi/powerbtn.sh
# Initiates a shutdown when the power putton has been
# pressed.

if ps -Af | grep -q '[k]desktop' && test -f /usr/bin/dcop
then
    dcop --all-sessions --all-users ksmserver ksmserver logout 1 2 2 && exit 0
elif ps -Af | grep -q 'AsusLauncher'
then
    if [ ! -f /home/user/.doingLogin ]
    then
      DISPLAY=:0 su -c /opt/xandros/bin/shutdown_dialog user &
    fi
else
	/bin/sync
	/usr/bin/killall --wait usbstorageapplet
    /bin/kill -SIGUSR2 1
fi

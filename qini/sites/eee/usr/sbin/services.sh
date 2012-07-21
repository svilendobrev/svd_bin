#!/bin/sh
PATH="/lib/init:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin"
# On this system X takes 1 second to start
sleep 1

rm -fr /dev/disks/Removable/* /dev/cdroms/* /media/sd*

#start networking first
if [ -e /proc/sys/net/ipv4/conf/all/rp_filter ] ; then
	for f in /proc/sys/net/ipv4/conf/*/rp_filter; do
		echo 1 > $f
	done
fi

# We do not want the connection system dialog at startup
touch /tmp/xandrosncs_no_status_dialog

echo "">/proc/sys/kernel/hotplug
/sbin/udevd --daemon
#debug udev
#. /root/05udev

# Loop over every line in /etc/modules.
grep '^[^#]' /etc/modules | \
while read module args; do
	[ "$module" ] || continue
	modprobe $module $args > /dev/null 2>&1 || true
done

modprobe usbhid
modprobe uhci-hcd
modprobe ehci-hcd
mount -t usbfs usbfs /proc/bus/usb

/sbin/start-stop-daemon --start --quiet --exec /usr/sbin/acpid -- -c /etc/acpi/events -s /var/run/acpid.socket -l /dev/null

modprobe atl2

modprobe pciehp pciehp_force=1
sleep 1	#XXX 2
/usr/sbin/wlan_on_boot.sh
#XXX> /tmp/wlan_on_boot.log 2>&1

alsactl restore
aplay /usr/share/sounds/silence.wav

sleep 1	#XXX 2
modprobe usb-storage

# XXX this equivalent to /etc/init.d/cupsys start - moved to /etc/fastservices
#chown root:lpadmin /usr/share/cups/model 2>/dev/null || true
#chmod 3775 /usr/share/cups/model 2>/dev/null || true
#mkdir -p /var/run/cups
#start-stop-daemon --start --quiet --oknodo --pidfile /var/run/cups/cupsd.pid --exec /usr/sbin/cupsd

#XXX moved below
# if [ -f /etc/fastservices ]; then
# 	for i in `cat /etc/fastservices`; do
# 		/usr/sbin/invoke-rc.d $i start
# 	done
# fi

#XXX disabled
# if [ `cat /sys/block/sdb/device/vendor` = "ATA" ]; then
# 	if [ ! -d "/home/user/My Documents 2" ]; then
# 		mkdir -p "/home/user/My Documents 2"
# 	fi
# 	mount /dev/sdb1 "/home/user/My Documents 2"
# 	chown user:user "/home/user/My Documents 2"
# fi

modprobe p4_clockmod
modprobe cpufreq_ondemand
#echo "ondemand" > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
#/sbin/cpuspeed

# XXX this equivalent to /etc/init.d/portmap start - moved to /etc/fastservices
#start-stop-daemon --start --quiet --oknodo --exec /sbin/portmap

# Store samba run state in /tmp, as it gets written to frequently
mkdir -p /tmp/.samba
#XXX moved to /etc/fastservices
#/usr/sbin/invoke-rc.d samba start

if [ -f /etc/fastservices ]; then
	#let comment line start with '#'
	for i in `grep -v "^#" /etc/fastservices`; do
		/usr/sbin/invoke-rc.d $i start
	done
fi

/sbin/memd
#wake on lan = magic packet
/usr/sbin/ethtool -s eth0 wol g

# Clean up the file that disables connection status window
rm -f /tmp/xandrosncs_no_status_dialog

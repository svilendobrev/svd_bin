#!/bin/sh
V=`cat /sys/class/backlight/acpi_video0/brightness`
X=${1:-5}
test $X = 1 && V=$((V+1))
test $X = 0 && V=$((V-1))
sudo sh -c "echo $V > /sys/class/backlight/acpi_video0/brightness"

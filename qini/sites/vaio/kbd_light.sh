#!/bin/sh
V=${1:-1}
sudo sh -c "echo $V > /sys/devices/platform/sony-laptop/kbd_backlight"


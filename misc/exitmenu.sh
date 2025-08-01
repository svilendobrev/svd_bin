#!/bin/sh

#LOG=/tmp/exi.`date +%Y%m%d-%H%M`.$$
#exec &>>$LOG-b

scelta=$( Xdialog --stdout --title " exit?" --shadow --menu "?" 17 35 35 \
      "q" "poweroff"  \
      "x" "xrestart"  \
      "r" "reboot"    \
      2>/dev/null );

case $scelta in
#x) killall nodm ;;
x) pkexec /usr/local/bin/xrestart ;;
q) systemctl poweroff ;;
r) systemctl reboot ;;
#h) systemctl hibernate ;;
#s) systemctl suspend   ;;
*) echo "invalid result ($scelta) "; exit;;
esac

# vim:ts=4:sw=4:expandtab

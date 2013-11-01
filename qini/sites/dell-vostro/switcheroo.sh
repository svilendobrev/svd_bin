#!/bin/sh
#https://help.ubun`tu.com/community/HybridGraphics
echo vgaswitcheroo >/home/tmp/vgaswitcheroo
vgaswitcheroo=/sys/kernel/debug/vgaswitcheroo/switch

test -z "$1" && WHICH=IGD || WHICH=DIS

cat $vgaswitcheroo

echo ON 	> $vgaswitcheroo
echo $WHICH > $vgaswitcheroo
echo OFF 	> $vgaswitcheroo

cat $vgaswitcheroo

#use integrated:
#echo IGD > /sys/kernel/debug/vgaswitcheroo/switch

#use discrete:
#echo DIS > /sys/kernel/debug/vgaswitcheroo/switch

#on/off the unused:
#echo ON > /sys/kernel/debug/vgaswitcheroo/switch
#echo OFF > /sys/kernel/debug/vgaswitcheroo/switch

#Queues a switch to integrated graphics to occur when the X server is next restarted.
#echo DIGD > /sys/kernel/debug/vgaswitcheroo/switch
#echo DDIS > /sys/kernel/debug/vgaswitcheroo/switch

#!/bin/sh
#usr/bin/xdotool  nnnno
##xdotool . = next  , = prev
#getactivewindow
#set_window --name kuk
#search --name mplayer
#windowactivate
#type --clearmodifiers $1
#sleep 0.5
#search --name kuk
#windowactivate
#search --name kuk
#set_window --name pp

X=`xdotool getactivewindow`
xdotool search --name mplayer windowactivate sleep 0.3 type " $1"
xdotool sleep 0.35 windowactivate $X


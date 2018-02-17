#!/bin/bash
#setxkbmap -rules xfree86 -model pc105 -layout "en_US,bg" -variant ",phonetic_enhanced" -option "grp:alt_shift_toggle" -print | xkbcomp - $DISPLAY

#echo XXXXXXXXXXXXXXXXXX >/tmp/xxxxxxx

# xkbcomp uses cur dir, then /usr/X11R6/lib/X11/xkb
# remove xkb/pc/us
# ln -s xkb/us	xkb/pc/us
#the bg outside pc/ dir doesn't seem to work, so no enhanced...
grep -q 'Module kbd: vendor' /var/log/Xorg.0.log && RUL=xorg || RUL=evdev
#for RUL in evdev xorg; do	#xorg xfree86
  #try one of these
  echo $RUL
  #-v 5

  if test -e /usr/share/X11/xkb/symbols/bg_ltgt ; then
    setxkbmap -rules $RUL -model pc105 -layout "en_US,bg_ltgt" -variant ",phonetic_ltgt" -option "grp:alt_shift_toggle,grp_led:scroll,grp:sclk_toggle"
  elif test -e /home/qini/x/symbols/bg_ltgt ; then
    setxkbmap -rules $RUL -model pc105 -layout "en_US,bg_ltgt" -variant ",phonetic_ltgt" -option "grp:alt_shift_toggle,grp_led:scroll,grp:sclk_toggle" -print | xkbcomp -w 3 -I/home/qini/x/ - $DISPLAY
  else
    setxkbmap -rules $RUL -model pc105 -layout "en_US,bg" -variant ",phonetic" -option "grp:alt_shift_toggle,grp_led:scroll,grp:sclk_toggle"
  fi
  	##&& break
		#also caps_toggle menu_toggle ... /usr/share/X11/xkb/rules/base.lst
	#-print | xkbcomp - $DISPLAY
#done
#date > /tmp/`basename $0`

#same as scrollock sclk_toggle above
xmodmap -e "keysym Pause = ISO_Next_Group"
#xmodmap -e "keysym Break = ISO_Next_Group"

xset r rate 200 30

xmodmap -pk | grep -q Alt_R || xmodmap -e 'keycode 108 = Alt_R'
#xmodmap -e "add mod1 = Alt_L Alt_R"

echo clear lock | xmodmap -
echo keysym Caps_Lock = Shift_L | xmodmap - >& /dev/null #Caps_Lock

if uname -a | grep -q eee ; then ##eeepc:
 echo eeepc
  echo keycode 135 = Control_R    | xmodmap - #Menu
  echo add control = Control_R    | xmodmap -
else
 xmodmap -e "keycode 133 = underscore"	#winLeft =_
 xmodmap -e "keycode 134 = underscore"	#winRight=_
fi


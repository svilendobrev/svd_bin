#!/bin/bash -x
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
  OPTION="grp_led:scroll,grp:sclk_toggle,grp:lctrl_lwin_toggle"
  #maybe also: grp:alt_shift_toggle    grp:alt_space_toggle    grp:win_space_toggle
  # grp:lwin_toggle =doesnotwork
  # error=  grp:rctrl_rshift_toggle   grp:ctrl_shift_toggle   grp:ctrl_space_toggle
  grep -q 'Logitech Wireless Keyboard PID:4023' /var/log/Xorg.0.log && OPTION=$OPTION,grp_led:caps
  grep -q 'Kingston HyperX Alloy Core RGB Keyboard' /var/log/Xorg.0.log && OPTION=$OPTION,grp_led:caps
  echo $OPTION
  #US=en_US
  US=us
  if test -e /usr/share/X11/xkb/symbols/bg_ltgt ; then
    setxkbmap -rules $RUL -model pc105 -layout "$US,bg_ltgt" -variant ",phonetic_ltgt" -option $OPTION
  elif test -e /home/qini/x/symbols/bg_ltgt ; then	#does not work well.. copy the symbols/bg_ltgt into above
    setxkbmap -rules $RUL -model pc105 -layout "$US,bg_ltgt" -variant ",phonetic_ltgt" -option $OPTION -print | xkbcomp -w 3 -I/home/qini/x/ - $DISPLAY
  else
    setxkbmap -rules $RUL -model pc105 -layout "$US,bg" -variant ",phonetic" -option $OPTION
  fi
  	##&& break
		#also caps_toggle menu_toggle ... /usr/share/X11/xkb/rules/base.lst
	#-print | xkbcomp - $DISPLAY
#done
#date > /tmp/`basename $0`

#same as scrollock sclk_toggle above
#xmodmap -e "keysym Pause = ISO_Next_Group"
#xmodmap -e "keysym Break = ISO_Next_Group"

xset r rate 200 30
#xset r rate 250 30	#fujitsu kbd..

xmodmap -pk | grep -q Alt_R || xmodmap -e 'keycode 108 = Alt_R'
#xmodmap -e "add mod1 = Alt_L Alt_R"

echo clear lock | xmodmap -
#echo keysym Caps_Lock = Shift_L | xmodmap - >& /dev/null #Caps_Lock
echo keysym Caps_Lock = Control_L | xmodmap - >& /dev/null #Caps_Lock
echo add Control = Control_L | xmodmap -

if uname -a | grep -q eee ; then ##eeepc:
 echo eeepc
  echo keycode 135 = Control_R    | xmodmap - #Menu
  echo add control = Control_R    | xmodmap -
else	#133=winLeft 134=winRight 135=Menu
 xmodmap -e "keysym Menu = underscore"
 #xmodmap -e "keycode 135 = underscore"
 #xmodmap -e "keycode 133 = underscore"	#winLeft =_
 #xmodmap -e "keycode 134 = underscore"	#winRight=_
fi

#xmodmap -e "keysym Super_L = Escape"

#!/bin/bash
#-x
#setxkbmap -rules xfree86 -model pc105 -layout "en_US,bg" -variant ",phonetic_enhanced" -option "grp:alt_shift_toggle" -print | xkbcomp - $DISPLAY

# xkbcomp uses cur dir, then /usr/X11R6/lib/X11/xkb
# remove xkb/pc/us
# ln -s xkb/us	xkb/pc/us
#the bg outside pc/ dir doesn't seem to work, so no enhanced...
grep -q 'Module kbd: vendor' /var/log/Xorg.0.log && RUL=xorg || RUL=evdev

#XXX setxkbmap -option is additive
  echo $RUL
  #-v 5

#  TOGGLE2=lctrl_lwin_toggle
#  uname -a | grep -q x220 && TOGGLE2=alt_shift_toggle
#  OPTION="grp_led:scroll,grp:sclk_toggle,grp:$TOGGLE2"
#=======
  OPTION="grp_led:scroll,grp:sclk_toggle,grp:lctrl_lwin_toggle,grp:win_space_toggle"

  #maybe also: grp:alt_shift_toggle    grp:alt_space_toggle    grp:win_space_toggle
  # grp:lwin_toggle =doesnotwork
  # error=  grp:rctrl_rshift_toggle   grp:ctrl_shift_toggle   grp:ctrl_space_toggle
  grep -q 'Logitech Wireless Keyboard PID:4023' /var/log/Xorg.0.log && OPTION=$OPTION,grp_led:caps
  grep -q 'Kingston HyperX Alloy Core RGB Keyboard' /var/log/Xorg.0.log && OPTION=$OPTION,grp_led:caps
  uname -a | grep -q eeepc  && OPTION="grp_led:scroll,grp:sclk_toggle,grp:alt_shift_toggle" && NOBGLTGT=1
  echo $OPTION
  #US=en_US
  US=us
  if test -e $NOBGLTGT/usr/share/X11/xkb/symbols/bg_ltgt ; then
    setxkbmap -rules $RUL -model pc105 -layout "$US,bg_ltgt" -variant ",phonetic_ltgt" -option $OPTION
  elif test -e $NOBGLTGT/home/qini/x/symbols/bg_ltgt ; then	#does not work well.. copy the symbols/bg_ltgt into above
    setxkbmap -rules $RUL -model pc105 -layout "$US,bg_ltgt" -variant ",phonetic_ltgt" -option $OPTION -print | xkbcomp -w 3 -I/home/qini/x/ - $DISPLAY
  else
    setxkbmap -rules $RUL -model pc105 -layout "$US,bg" -variant ",phonetic" -option $OPTION
  fi
		#also caps_toggle menu_toggle ... /usr/share/X11/xkb/rules/base.lst
	#-print | xkbcomp - $DISPLAY

#same as scrollock sclk_toggle above
#xmodmap -e "keysym Pause = ISO_Next_Group"
#xmodmap -e "keysym Break = ISO_Next_Group"

xset r rate 200 30
#xset r rate 250 30	#fujitsu kbd..

xmodmap -pk | grep -q Alt_R || xmodmap -e 'keycode 108 = Alt_R'
#xmodmap -e "add mod1 = Alt_L Alt_R"

#capslock... caps=ctrl-on-hold|esc-on-tap
#github.com/alols/xcape
if which xcape >& /dev/null ; then
 pgrep xcape >/dev/null || (
  sleep 2
  setxkbmap -option caps:ctrl_modifier
  xcape  -e 'Caps_Lock=Escape'
 )
else
 echo clear lock | xmodmap -
 echo keysym Caps_Lock = Control_L | xmodmap - >& /dev/null #Caps_Lock=control
fi

#also check https://unix.stackexchange.com/a/730891 - via udev, regardless of X or what
# https://www.codejam.info/2022/04/xmodmaprc-wayland.html
# /usr/share/X11/xkb/symbols/ctrl
# /usr/share/X11/xkb/symbols/capslock
# /usr/share/X11/xkb/rules/evdev
# ? .config/xkb/symbols/someth
# ? + entry in .config/xkb/rules/evdev aotu someth:..

echo add Control = Control_L | xmodmap -

if uname -a | grep -q eee ; then ##eeepc:
 echo eeepc
 #this stopped working
 # echo keycode 135 = Control_R    | xmodmap - #Menu
 # echo add control = Control_R    | xmodmap -
 #so use this instead:
 xmodmap -e "keysym Menu = underscore"
 #pause == scrollock ; no break
 xmodmap -e "keysym Pause = ISO_Next_Group"
else	#133=winLeft 134=winRight 135=Menu
 xmodmap -e "keysym Menu = underscore"
 #xmodmap -e "keycode 135 = underscore"
 #xmodmap -e "keycode 133 = underscore"	#winLeft =_
 #xmodmap -e "keycode 134 = underscore"	#winRight=_
fi

if uname -a | grep -q hepi ; then #hp640
 echo hEpI.. PrintScr=Insert
  xmodmap -e "keysym Print = KP_Insert"
 #xmodmap -e "keycode 107 = KP_Insert Print KP_Insert Print"	#instead of print+sysreq
 #fn+F10 = insert
 #fn+S = sysRq ~= printscr -> insert
 #fn+C = scrollLock -> ISO_Next_Group
 #fn+R = Break
fi


#xmodmap -e "keysym Super_L = Escape"

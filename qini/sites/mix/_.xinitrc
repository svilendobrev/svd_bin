LD_LIBRARY_PATH=/usr/openwin/lib:/usr/lib
export LD_LIBRARY_PATH
OPENWINHOME=/usr/openwin;	export OPENWINHOME
xrdb -load $HOME/.Xdefaults 
#xsetroot -solid cadetblue4 

# xclock -geometry -0+0 &
#
#xterm -n adl7 -geometry 80x46+0-4 -fn fixed -ls &
#xterm -n adl7 -geometry 82x40-0-4 -ls &
#xterm -n adl7 -name ROOT -geometry 80x41+0+0 -fn fixed -ls &
#
#/usr/local/bin/xmailbox++ -file nsmail/Inbox -update 30 -geometry -0+40 &

. $HOME/sys/_xtermstart

# Startup netscape after 3 seconds so we dont delay the login process
# sh -c "sleep 2; /usr/local/bin/netscape_47.sh -iconic" &

#/usr/local/bin/start_mwm_12
#echo "$0 : $PATH" >pathme
#/usr/local/bin/start_kwm > kde-errors 2>&1
/usr/local/bin/start_kwm > /dev/null 2>&1 

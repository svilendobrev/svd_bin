#!/bin/sh
export VS=`echo $VS$0.$1|grep vs`
export VIO=`echo $VIO$0.$1|grep vio`
for a in ${@:-./*}; do
 test -d "$a" || continue
 test "$a" = "./__pycache__" && continue
 if test ! -L "$a" -o -n "$LINKSuall" -o `basename "$0"` = "luall.sh" -o -f .LINKSuall -o -f _uall-links; then
  cd "$a"
  if test -f ignore-uall -o -f _uall-ignore ; then echo '** ignored' `pwd`
  else
    BWD=$a
    test -n "$UWD" && BWD=$UWD/${a#./}
    H="$UPFX >>> $BWD -----------"
    #`pwd`'---'
    if test -n "$VS" ; then
        CMD="v s"
        test -x ./vs && CMD=./vs
        echo -e "$H"
        UWD=$BWD $E $CMD
    elif test -n "$VIO" ; then
        CMD="v io"
        test -x ./vio && CMD=./vio
        echo -e "$H"
        UWD=$BWD $E $CMD
    else
      CMD="v u"
      test -x ./u && CMD=./u
      if test -z $UPARAL ; then
        echo -e "$H"
        UWD=$BWD $E $CMD
      else
        #UWD=$BWD $E $CMD 2>&1 | nl -s "$BWD	" - | cut -c1-5,7- &
        UWD=$BWD $E $CMD 2>&1 | perl -ne "s,^,$BWD  ,;print "  &
      fi
    fi
  fi
  cd ..
 fi
done
# vim:ts=4:sw=4:expandtab

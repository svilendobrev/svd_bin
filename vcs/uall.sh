#!/bin/sh
export VS=`echo $VS$0.$1|grep vs`
for a in ${@:-./*}; do
 test -d $a || continue
 if test ! -L "$a" -o -n "$LINKSuall" -o `basename "$0"` = "luall.sh" -o -f .LINKSuall; then
  cd "$a"
  if test -f ignore-uall ; then echo '** ignored' `pwd`
  else
    BWD=$a
    test -n "$UWD" && BWD=$UWD/${a#./}
    H=" >>> $BWD"
    #`pwd`'---'
    if test -n "$VS" ; then
        echo "$H"
        test -x ./vs && CMD=./vs || test -x ./u && CMD=./u || CMD="v s"
        UWD=$BWD $E $CMD
    else
      test -x ./u && CMD=./u || CMD="v u"
      if test -z $UPARAL ; then
        echo "$H"
        UWD=$BWD $E $CMD
      else
        UWD=$BWD $E $CMD |& nl -s "$BWD	" - | cut -c1-5,7- &
      fi
    fi
  fi
  cd ..
 fi
done
# vim:ts=4:sw=4:expandtab

#!/bin/sh
export VS=`echo $VS$0.$1|grep vs`
for a in ${@:-*}; do
 test -d $a || continue
 if test ! -L $a -o -n "$LINKSuall" -o `basename "$0"` = "luall.sh"; then
  cd $a 
  if test -f ignore-uall ; then echo ' ** ignored' `pwd` 
  else 
    H=">>> $a"
    #`pwd`'---'
    if test -n "$VS" ; then 
        echo "$H"
        test -x ./vs && CMD=./vs || test -x ./u && CMD=./u || CMD="v s"
        $E $CMD
    else
      test -x ./u && CMD=./u || CMD="v u"
      if test -z $UPARAL ; then
        echo "$H"
        $E $CMD 
      else 
        $E $CMD | nl -s "$a	" - | cut -c7- &
      fi
    fi
  fi
  cd ..
 fi
done
# vim:ts=4:sw=4:expandtab

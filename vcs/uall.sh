#!/bin/sh
for a in ${@:-*}; do
 test -d $a || continue
 if test ! -L $a -o -n "$LINKSuall" -o `basename "$0"` = "luall.sh"; then
  cd $a 
  if test -f ignore-uall ; then echo ' ** ignored' `pwd` 
  else 
    echo '---' `pwd` '---'
    if echo $0 | grep -q vs ; then $E v s
    else
      if test -x ./u ; then $E ./u 
      else $E v u 
      fi
    fi
  fi
  cd ..
 fi
done
# vim:ts=4:sw=4:expandtab

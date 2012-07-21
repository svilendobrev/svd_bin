#!/bin/bash

#set -x
#errtrace
#set -E
trap "killall lftp; kill -SIGHUP -$$" SIGQUIT

echo ps:$$
IO=${IO:-./}
#IO=/tmp/proba
TODO=$IO/todo
LOG=${LOG:-$IO/log}
STOP=${STOP:-$IO/stop}

NPARALEL=${NPARALEL:-2}

FIN=${FIN:-./fin}

exec > >( tee -a $LOG ) 2>&1
#exec 2>&1 | tee -a $LOG
#exec >> $LOG 2>&1
echo started $0 $TODO

mkdir -p $TODO $FIN
chmod a+rw $TODO $FIN
touch $TODO/ignore


WGET='wget -r -c --no-parent'
WGET="$WGET --restrict-file-names=nocontrol --content-disposition"
#WGET="$WGET --no-verbose"
WGET="$WGET --progress=dot:mega"
WGET="$WGET -R.part -X\*[Ss]ample"
mywget() { $WGET -i "$a"; }

NICE="empty -f"
NICE=nice
NICE=unbuffer

anypart() {
# mOPTS="--verbose=3"
 lftp -c "mirror -c -I *.part --dry-run \"$1\" ./" | grep -q "^get.*part"
}

mylftp() { #arg1: urllistfile
 OPTS="mirror -c"
# OPTS="$OPTS --ignore-time"
# OPTS="mirror -n"
 OPTS="$OPTS --parallel=$NPARALEL"
# OPTS="$OPTS --use-pget-n=2"
 OPTS="$OPTS --verbose=3"
 OPTS="$OPTS -X *.part"
 OPTS="$OPTS -x '.*[sS]ample.*'"
 cat "$1" | while read x; do
  test -f $STOP && echo stopped1 $0 && exit 1
  test -z "$x" && continue
  anypart "$x" && echo "$x" >> $IO/_todo
   #&& continue

  _OPTS="$OPTS \"$x\" ./"
  #mirror does not work on single files hence get1, the only *get* with working -c contiue
  echo "$x" | grep -q '/$' || _OPTS="get1 -c \"$x\" || $_OPTS"
  echo "$_OPTS"
  echo "<< $x"
  $NICE lftp -c "set xfer:rate-period 5" -c "$_OPTS" || continue
  test -f $STOP && echo stopped2 $0 && exit 1
  echo ">> $x"
  echo "$x" >>$FIN/ok
 done
}

myget=mylftp
echo go


while true; do
 for a in $TODO/*; do
    test -f $STOP && echo stopped $0 && exit
    sleep 1
    test -f "$a" || continue
    test -s "$a" || continue
    echo :"$a"
    O=$FIN/`date +%s`
    $myget "$a" && mv -f "$a" $FIN/
    # $O && mkdir -p $O && mv "$a" $O && cp $LOG $O && echo >$LOG
 done
 test -s $IO/_todo && mv -f $IO/_todo  $TODO/
 find $IO -name log -size +50k | grep $LOG && cp $LOG $FIN/`date +%s`.log && echo >$LOG
 sleep 15
 #echo again
done
echo neverquited $0

# vim:ts=4:sw=4:expandtab

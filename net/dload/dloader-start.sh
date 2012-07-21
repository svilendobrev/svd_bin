#!/bin/sh

# PROVIDE: dloader
# REQUIRE: mystart

ROOT=/mnt/a/novo/
DIR=wget
cd $ROOT && mkdir -p $DIR && chmod a+rw $DIR && cd $DIR

export IO=/tmp/proba
export STOP=$IO/stop

#allow replace ./dloader.sh on-the-fly
#create a file ./stop to avoid/stop ./dloader.sh and re-start it once removed

stopper() { # seems that any executed cmd/func is forked, so kill all of them
 while true; do
  sleep 3
  test -f $STOP || continue
  echo selfstop lftp dloader.sh
  killall lftp dloader.sh
  break
 done
}

stopper &

while true; do
 test -f $STOP || su opa ./dloader.sh
 sleep 5
done

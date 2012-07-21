#!/bin/sh
SLEEP=${1:-3}
shift
sleep $SLEEP
devilspie "$@" &
sleep 19
killall devilspie

#!/bin/sh
ARGS='-r '
for a in $@; do
 case $a in
 	-1.2*) ARGS="$ARGS --min 1.2ghz" ;;
 	-1.6*) ARGS="$ARGS --min 1.6ghz" ;;
 	-2*) ARGS="$ARGS --min 2.1ghz" ;;

 	+1.2*) ARGS="$ARGS --max 1.2ghz" ;;
 	+1.6*) ARGS="$ARGS --max 1.6ghz" ;;
 	+2*) ARGS="$ARGS --max 2.1ghz" ;;

# 	+[0-9]*) ARGS="$ARGS --max $a" ;;
 	[a-z]*) ARGS="$ARGS -g $a" ;;
 esac
done
echo cpufreq-set $ARGS
sudo cpufreq-set $ARGS -c 0

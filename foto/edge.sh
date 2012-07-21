#!/bin/sh
[ -z "$EDGE" ] && EDGE=0.4
[ -z "$RADIUS" ] && RADIUS=0.8
OUT=$1.edge.$EDGE.ppm
#echo $EDGE $RADIUS
pnmnlfilt -$EDGE $RADIUS <$1 >$OUT


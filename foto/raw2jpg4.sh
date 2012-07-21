#!/bin/sh
dcraw -w -h -c $1 | pnmscale -r 2 | cjpeg -q 90 >$1.4.jpg

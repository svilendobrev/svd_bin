#!/bin/sh
dcraw -w -h -c $1 | pnmscale -r 4 | cjpeg -q 90 >$1.8.jpg

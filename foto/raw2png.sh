#!/bin/sh
dcraw -c "$@" | pnmtopng >$1.png

#!/bin/sh
mplayer -vo null -ao null -frames 0 -msglevel identify=4 "$@" 2>/dev/null

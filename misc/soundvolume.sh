#!/bin/sh
amixer set Master playback ${2:-2}db${1:-+}
#e.g. soundvol - 5

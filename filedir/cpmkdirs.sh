#!/bin/sh
CPopts="$3"
test ! -e "$2/$1" && mkdir -p "$2/$1" && rmdir "$2/$1"
cp "$CPopts" "$1" "$2/$1"

# vim:ts=4:sw=4:expandtab

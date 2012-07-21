#!/bin/sh
mkdir -p reindex
for a in "$@"; do mencoder "$a" -o reindex/"$a" -ovc copy -oac copy; done

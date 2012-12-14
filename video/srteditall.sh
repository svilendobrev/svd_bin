#!/bin/sh
echo subtitledit `find . -name \*srt | sed -s 's/^/"/;s/$/"/'` | sh

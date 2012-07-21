#!/bin/sh
find $1 -type d -print | perl -ne 'chop ;$f=$_; s{^/}[]; s{[^/]+/}[|___]g; print +(-d $f) ? "$_/\n" : "$_\n"'

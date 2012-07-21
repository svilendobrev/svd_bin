#!/bin/sh
ROOT=`cat CVS/Repository`
cvs stat $@ | perl -ne "print if (s!Repository revision:\s*(\d+\.\d+)\.\d+\.\d+\s*.*?$ROOT/([^,]+).*!cvd -r \1 \2! )"

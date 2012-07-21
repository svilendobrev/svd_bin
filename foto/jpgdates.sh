#!/bin/sh
find . -name \*jpg -exec jhead {} \; | grep -E '(ile name|Date)'

#!/bin/sh
find ${1:-.} -name \*jpg | sort | parallel jhead {} \; | grep -E '(ile name|Date)'

#!/bin/sh
git log --pretty=format:%an | awk '{ ++c[$0]; } END { for(cc in c) printf "%5d %s\n",c[cc],cc; }'| sort -r

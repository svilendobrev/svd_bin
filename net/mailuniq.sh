#!/bin/sh
#for a in *; do ln $a ../`perl -ne 'if (s/Message-Id: <(.*)>/\1/i) {print; exit;}' $a `; done
for b in */cur; do 
 echo $b
 cd $b
 for a in *; do ln $a ../`perl -ne 'if (s/Message-Id: <(.*)>/\1/i) {print; exit;}' $a `; done 
 cd -
done

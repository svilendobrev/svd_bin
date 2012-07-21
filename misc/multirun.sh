#!/bin/sh

if [ $# -lt 2 ]; then echo "multi_cmd command-in-quotes file-list-in-quotes [-q[q]]"
else

for a in $2
do
 echo $a
 case x$3 in
  x|x-qq*) ;;
  x-q*) echo "------- [$a] -------";;
  x*)   echo "------- run [$1] on [$a] -------";; 
 esac
 $1 $a
done
echo "=== eof ==="
fi


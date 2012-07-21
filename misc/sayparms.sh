#!/bin/sh
#if u want to see how some program is being (hiddenly) invoked,
#copy/link this, named as the target program,
#and make sure it's called instead of original (in path or else)

echo "$# parameters"
echo ":: $@ ::"
for a in "$@"; do  echo :"$a"; done

#!/bin/tcsh
#while ($#argv > 0)
# echo "$argv[1]"
# shift
#end


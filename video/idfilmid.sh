#!/bin/sh
for i in "$@"; do
	x="$i".id
	test -e "$x" && grep -q ID_LENGTH "$x" && exit
	echo "$i"
	filmid.sh "$i" > "$x"
done

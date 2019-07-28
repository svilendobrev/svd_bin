#!/bin/sh

echo "<html>"
test -n "$HEAD$TITLE" && echo "<head>"
test -n "$TITLE" && echo "<title>$TITLE</title>"
test -n "$HEAD$TITLE" && echo "$HEAD</head>"
test -n "$AUTOSIZE" && echo " <head> <style> img { max-width: 95% ; max-height: 95% } </style> </head> "
echo "<body><center>"
echo "$TITLE"
echo "<hr>"
test -z "$NOBR" && BR="<BR>"
test -z "$NOHR" && HR="<hr>"
for a in "$@"; do
	test "$a" = "$O" && continue
	test -z "$NONAME" && name="<BR>$a"
	if [ -d "$a" ]; then
		echo '<a href="'$a'">' $name "</a> $BR $HR"
	else
	    endname=
		test -n "$HREF" && endname="</a>" && echo -n '<a href="'$HREF/$a'">'
		echo '<img src="'$a'"'"$ATTRS"' >' $name$endname "$BR $HR $BR"
	fi
done
echo "</html>"


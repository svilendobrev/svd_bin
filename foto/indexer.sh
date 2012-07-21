#!/bin/sh

echo "<html>"
test -n "$TITLE" && echo "<title>$TITLE</title>"
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
		echo '<img src="'$a'">' $name$endname "$BR $HR $BR"
	fi
done
echo "</html>"


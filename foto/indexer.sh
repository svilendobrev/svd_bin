#!/bin/bash

echo "<html>"
test -n "$HEAD$TITLE" && echo "<head>"
test -n "$TITLE" && echo "<title>$TITLE</title>"
test -n "$HEAD$TITLE" && echo "$HEAD</head>"
#opera: pagedown=82.5vh
#ffox:  pagedown=91.2vh
test -n "$AUTOSIZE" && echo " <head> <style> img { max-width: 98.5vw ; max-height: 87.5vh } body { margin: 1px } </style> </head> "

echo "<body><center>"
echo "$TITLE"
echo "<hr>"
test -z "$NOBR" && BR="<BR>"
test -z "$NOHR" && HR="<hr>"
for a in "$@"; do
	test "$a" = "$O" && continue
	#perl -e ' exit !($ARGV[0] =~ m,/del/,)' "$a" && continue
	[[ "x$a" =~ /del/ ]] && continue
	if [ -d "$a" -o -n "$NOPATHS" -a `basename "$a" .html` != "$a" ]; then
		echo '<a href="'$a'">' "$a" "</a> $BR $HR"
	else
		test -z "$NONAME" && name="<BR>$a"
		test -z "$JHEAD" && name="$name "`jhead "$a" | perl -ne 'print if s/^(Aperture.*:|Exposure.time.*:.*s|ISO.*:)//'`
	    endname=
		test -n "$HREF" && endname="</a>" && echo -n '<a href="'$HREF/$a'">'
		echo '<img src="'$a'"'"$ATTRS"' >' $name$endname "$BR $HR $BR"
	fi
done
echo "</html>"


#!/usr/bin/perl -n
print if s/^.*(<img[^>]+src=|imgf\( *)[\"\'](.+?)[\"\'].*/\2/ || s/^ *!([\w.]+)($|\s.*)/\1.jpg/

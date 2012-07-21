#$Id: doscyr.py,v 1.1 2006-01-10 12:15:22 sdobrev Exp $

dos2win = ''
for c in range(0x80): dos2win += chr(c)
for c in range(0x80,0x80+0x40): dos2win += chr(c+0x40)
for c in range(0x80,0x80+0x40): dos2win += chr(c)

import re
doscyr = re.compile( '[\x80-\xBF]' )

# vim:ts=4:sw=4:expandtab

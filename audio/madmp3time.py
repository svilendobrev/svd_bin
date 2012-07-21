#!/usr/bin/env python
import sys
import mad
mf = mad.MadFile( sys.argv[1])
track_length_in_milliseconds = mf.total_time()
s = track_length_in_milliseconds//1000
print s, s//60,':', s-60*(s//60)

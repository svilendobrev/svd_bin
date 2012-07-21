#$Id$
# -*- coding: utf-8 -*-
#маха начални-крайни нови редове вътре в полетата
import csv,sys
reader = csv.reader( open( sys.argv[1], "rb"))

rows = list( reader)
fixrows = [ [ x.strip() for x in l ] for l in rows ]

fo = file( sys.argv[1]+'.fix', "wb")
writer = csv.writer( fo)
writer.writerows( fixrows)
fo.close()

# vim:ts=4:sw=4:expandtab

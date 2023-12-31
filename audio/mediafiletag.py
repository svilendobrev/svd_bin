#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mediafile, sys
for a in sys.argv[1:]:
    mf = mediafile.MediaFile( a, id3v23= True)
    print( a, dict( (k,v) for k,v in mf.as_dict().items() if v))

    if 0:
        #oa = ..
        omf= mediafile.MediaFile( oa, id3v23= True)
        omf.update( mf.as_dict()
        omf.save()

# vim:ts=4:sw=4:expandtab

#!/usr/bin/env python

#
# simple.py - non threaded use of pyinotify

help = '''
usage: ./simple.py path[s]-to-watch] [-r] [-m=hexmask -r -m=mask1,mask2]
    -r  - recursive
    -m  - mask to use
'''

from process import PExample

# please read src/examples/README
try:
    # import local build
    import autopath
    from src.pyinotify.pyinotify import SimpleINotify, EventsCodes
except ImportError:
    # import global (installed) pyinotify
    from pyinotify import SimpleINotify, EventsCodes


if __name__ == '__main__':
    #
    # - Personalized monitoring: watch for selected events and
    #   do processing with PExample()
    # - The watched path is '/tmp' (by default) or the first
    #   command line argument if given.
    # - No additional thread is instancied and dedicated to the
    #   monitoring, instead of that this thread is in charge of
    #   all the job and block until the monitoring stop, type
    #   c^c to stop it.
    # - You can read the threaded version of this example in
    #   threaded_example.py
    #
    import sys

    class cfg:
        mask = ''
        rec = False
    path = []
    for a in sys.argv[1:]:
        if a =='-r': cfg.rec = True
        elif a.startswith('-m='): cfg.mask = a[3:]
        else:
            path.append(a)
    if not path:
        raise SystemExit, help

    def_mask = dict( IN_MODIFY =1, IN_DELETE =1,
                    IN_OPEN =1, IN_ATTRIB =1, IN_CREATE =1
                ).keys()

    masks = def_mask
    mask=0
    if cfg.mask:
        try:
            mask = int( cfg.mask,16)
        except TypeError: pass
        if mask:
            masks = ''
        else:
            masks = cfg.mask.split(',')
    for m in masks:
        mask |= getattr( EventsCodes, m)

    # class instance and init
    ino = SimpleINotify()

    print 'start monitoring %r %s with mask %d/%s' % (path, cfg.rec and 'recursive' or '', mask,'|'.join(masks))

    added_flag = False
    # read and process events
    while True:
        try:
            if not added_flag:
                # on first iteration, add a watch on path:
                # watch path for events handled by mask and give an
                # instance of PExample as processing function.
                for p in path:
                    ino.add_watch( p, mask, PExample(), rec=cfg.rec)
                added_flag = True
            ino.process_events()
            if ino.event_check():
                ino.read_events()
        except KeyboardInterrupt:
            # ...until c^c signal
            print 'stop monitoring...'
            # close inotify's instance
            ino.close()
            break
        except Exception, err:
            # otherwise keep on watching
            print err


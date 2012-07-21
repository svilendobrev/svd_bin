#!/usr/bin/env python
#$Id: ftpsrv.py,v 1.1 2004-08-23 17:01:51 sdobrev Exp $
from medusa.ftp_server import ftp_server, dummy_authorizer, asyncore

class any_authorizer(dummy_authorizer):
    def authorize (self, channel, username, password):
        r = dummy_authorizer.authorize( self, channel, username, password)
        channel.read_only = 0
        return r

import sys
if not sys.argv[1:]:
    print 'ftps host port root'
else:
    fs = ftp_server(
                any_authorizer( sys.argv[3] ),
                ip=sys.argv[1],
                port=int( sys.argv[2]),
            )
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        fs.log_info('FTP server shutting down. (received SIGINT)', 'warning')
        # close everything down on SIGINT.
        # of course this should be a cleaner shutdown.
        asyncore.close_all()

# vim:ts=4:sw=4:expandtab

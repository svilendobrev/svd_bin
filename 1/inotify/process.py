# -*- coding: utf-8 -*-
#
# process.py - example of ProcessEvent subclassing
# Copyright (C) 2006  Sйbastien Martini <sebastien.martini@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.


# please read src/examples/README
try:
    # import local build
    import autopath
    from src.pyinotify.pyinotify import ProcessEvent
except ImportError:
    # import global (installed) pyinotify
    from pyinotify import ProcessEvent


class PExample(ProcessEvent):
    """
    PExample class: introduces how to subclass ProcessEvent.
    """

    def process_default(self, event_k, event):
        """
        new default processing method
        """
        print 'PExample::process_default'
        super(PExample, self).process_default(event_k, event)

    # The followings events are individually handled

    def process_IN_MODIFY(self, event_k):
        """
        process 'IN_MODIFY' events
        """
        print 'PExample::process_IN_MODIFY'
        super(PExample, self).process_default(event_k, 'IN_MODIFY')

    def process_IN_OPEN(self, event_k):
        """
        process 'IN_OPEN' events
        """
        print 'PExample::process_IN_OPEN'
        super(PExample, self).process_default(event_k, 'IN_OPEN')


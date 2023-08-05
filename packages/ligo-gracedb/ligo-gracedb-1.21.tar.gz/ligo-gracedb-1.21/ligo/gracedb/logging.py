# -*- coding: utf-8 -*-
# Copyright (C) Leo Singer, Brian Moe, Branson Stephens (2015)
#
# This file is part of gracedb
#
# gracedb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gracedb.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

"""
Some convenience logging classes courtesy of Leo Singer, provided as is.

Usage:
import logging
import ligo.gracedb.rest
import ligo.gracedb.logging
 
logging.basicConfig()
log = logging.getLogger('testing')
 
gracedb = ligo.gracedb.rest.GraceDb()
graceid = 'T62829'
 
log.addHandler(ligo.gracedb.logging.GraceDbLogHandler(gracedb, graceid))

# The following will create a log entry on the gracedb server
# (if the log level permits)
#
log.warn("this is a warning")
"""

import logging
from six.moves.queue import Queue
from threading import Thread
__all__ = ('GraceDbLogHandler',)


_END_OF_STREAM = object()


class _GraceDbLogStream(object):

    def __init__(self, gracedb, graceid):
        self._gracedb = gracedb
        self._graceid = graceid
        self._queue = Queue()
        self._thread = Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def _run(self):
        while True:
            text = self._queue.get()
            if text is _END_OF_STREAM:
                self._queue.task_done()
                return
            self._gracedb.writeLog(self._graceid, text)
            self._queue.task_done()

    def write(self, text):
        self._queue.put(text)

    def close(self):
        if self._thread.is_alive():
            self._queue.put(_END_OF_STREAM)
            self._queue.join()
            self._thread.join()

    def __del__(self):
        self.close()


class _GraceDbLogFormatter(logging.Formatter):

    def __init__(self):
        logging.Formatter.__init__(self, logging.BASIC_FORMAT)

    def format(self, record):
        s = logging.Formatter.format(self, record)
        return '<div style="white-space:pre-wrap">' + s.strip("\n") + '</div>'


class GraceDbLogHandler(logging.StreamHandler):

    def __init__(self, gracedb, graceid):
        stream = _GraceDbLogStream(gracedb, graceid)
        super(GraceDbLogHandler, self).__init__(stream)
        self.formatter = _GraceDbLogFormatter()

    def close(self):
        super(GraceDbLogHandler, self).close()
        self.stream.close()

#!/usr/bin/env python
#
# Copyright 2017 QuantRocket - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging, logging.handlers
import socket
import six
import sys
import os
from six.moves import queue, urllib
from .exceptions import ImproperlyConfigured

FLIGHTLOG_PATH = "/flightlog/handler"

LOG_RECORD_TYPE_BOUNDARY = "||||q5%XfK4#||||"

class ImpatientHttpHandler(logging.handlers.HTTPHandler):
    """
    An HttpHandler that sets a short timeout (instead of the default no
    timeout), as well as serializing the record attribute types so they can
    be reconstituted.
    """

    def mapLogRecord(self, record):
        dict_with_types = {}
        for k, v in record.__dict__.items():
            type_name = type(v).__name__
            dict_with_types[k] = "{0}{1}{2}".format(
                type_name, LOG_RECORD_TYPE_BOUNDARY, v)
        return dict_with_types

    def emit(self, record):
        orig_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(3)
        super(ImpatientHttpHandler, self).emit(record)
        socket.setdefaulttimeout(orig_timeout)

def FlightlogHandler(background=None):
    """
    Returns a log handler that logs to flightlog. If background = True,
    configures a queue-based handler which sends messages to flightlog in a
    background thread. Otherwise, returns an http handler that runs
    synchronously.

    Modified from https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block
    """
    base_url = os.environ.get("HOUSTON_BASE_URL", None)
    if not base_url:
        raise ImproperlyConfigured("HOUSTON_BASE_URL is not set")
    parsed = urllib.parse.urlparse(base_url)
    secure = parsed.scheme == "https"
    if "HOUSTON_USERNAME" in os.environ and "HOUSTON_PASSWORD" in os.environ:
        credentials = (os.environ["HOUSTON_USERNAME"], os.environ["HOUSTON_PASSWORD"])
    else:
        credentials = None

    if six.PY2:
        if secure:
            raise NotImplementedError("Logging to Flightlog over HTTPS requires Python 3")
        if credentials:
            raise NotImplementedError("Logging to Flightlog using Basic Auth requires Python 3")

    if six.PY2:
        http_handler = ImpatientHttpHandler(
            parsed.netloc, FLIGHTLOG_PATH, method="POST")
    else:
        http_handler = ImpatientHttpHandler(
            parsed.netloc, FLIGHTLOG_PATH, method="POST", secure=secure, credentials=credentials)

    if six.PY2 or sys.version_info.minor < 2:
        if background:
            import warnings
            warnings.warn('Background logging requires Python 3.2 or higher. Logging in foreground...')
        background = False
    elif background is None:
        background = True

    if background:
        log_queue = queue.Queue(-1)  # no limit on size
        queue_handler = logging.handlers.QueueHandler(log_queue)
        listener = logging.handlers.QueueListener(log_queue, http_handler)
        listener.start()
        return queue_handler
    else:
        return http_handler

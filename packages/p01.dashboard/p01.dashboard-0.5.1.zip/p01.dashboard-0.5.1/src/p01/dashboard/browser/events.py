##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""
$Id: events.py 4554 2017-01-07 11:51:20Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import datetime
import logging

import gevent
import gevent.queue

import zope.interface
import zope.publisher.interfaces.http

import p01.dashboard.processor


LOGGER = logging.getLogger(__name__)


@zope.interface.implementer(zope.publisher.interfaces.http.IResult)
class SSEResult(object):
    """Server sent event stream result

    This will also work with single requests used by IE polyfill.
    """

    def __init__(self, streamer, channel, port):
        self.streamer = streamer
        self.channel = channel
        self.port = port
        self.client = streamer.getClient(self.port, self.channel)

    def __iter__(self):
        """Iterable server event stream"""
        while self.client.isStreaming:
            try:
                part = self.client.queue.get(timeout=0.5)
                if part is not None:
                    # mark client as seen and send stream
                    self.client.seen = datetime.datetime.now()
                    LOGGER.debug("Send stream for client %s:%s" %(self.port,
                        self.channel))
                    yield part
                else:
                    # None get as messag from queue means we need to abort
                    LOGGER.debug("Stop stream for client %s:%s" %(self.port,
                        self.channel))
                    raise StopIteration
            except gevent.queue.Empty:
                # empty queue, wait for next stream
                LOGGER.debug("Empty stream for client %s:%s" %(self.port,
                    self.channel))
                gevent.sleep(0.5)
        # processor stopped, close stream
        LOGGER.debug("Processor stopped for client %s:%s" %(self.port,
            self.channel))
        raise StopIteration

    def close(self):
        # add close marker to client
        self.streamer.delClient(self.client.port, self.client.channel)


class Events(object):
    """Server sent event stream

    This class sends a SSE data stream to the connected port
    """

    channel = None

    def __call__(self):
        # setup headers, no caching and buffering by nginx
        response = self.request.response
        response.setHeader('Cache-Control','no-cache')
        # response.setHeader("Connection", "keep-alive")
        response.setHeader('X-Accel-Buffering','no')
        response.setHeader('Content-Type', 'text/event-stream;charset=utf-8')
        port = self.request.get('REMOTE_PORT')
        LOGGER.debug("Start stream for channel %s and port %s" %(port,
            self.channel))
        streamer = p01.dashboard.processor.streamer
        return SSEResult(streamer, self.channel, port)

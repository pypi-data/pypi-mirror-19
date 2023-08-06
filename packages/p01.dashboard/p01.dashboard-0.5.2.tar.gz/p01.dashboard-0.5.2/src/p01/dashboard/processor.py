##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""Processor queue
$Id: processor.py 4555 2017-01-07 12:12:46Z roger.ineichen $
"""
__docformat__ = 'restructuredtext'

import json
import time
import datetime
import logging
import threading

import gevent
import gevent.queue


# clients
CLOSE_EMPTY_STREAMS_AFTER_SECONDS = 5 * 60
MAX_STREAMS_PER_CLIENT = 100

# mark as started
STREAMING = True


LOGGER = logging.getLogger(__name__)


##############################################################################
#
# client

class Client(object):
    """Client with port and channel holding the data queue"""

    seen = None

    def __init__(self, streamer, port, channel,
        timeout=CLOSE_EMPTY_STREAMS_AFTER_SECONDS,
        maxStreams=MAX_STREAMS_PER_CLIENT):
        self.streamer = streamer
        self.timeout = datetime.timedelta(seconds=timeout)
        self.maxStreams = maxStreams
        self.port = port
        self.channel = channel
        self.queue = gevent.queue.Queue(self.maxStreams)
        self.created = datetime.datetime.now()
        self.updated = None
        self.seen = datetime.datetime.now()
        # set client remove marker
        self.alive = True

    @property
    def isStreaming(self):
        if not self.alive:
            return False
        elif not isStreaming():
            return False
        else:
            if self.seen <= datetime.datetime.now() - self.timeout:
                return False
            else:
                return True

    def addStream(self, msg, now=None):
        """Add stream for this client and widget"""
        try:
            # add message to queue
            self.queue.put(msg)
            # mark a s updated if queue is not full
            if now is None:
                now = datetime.datetime.now()
            self.updated = now
        except gevent.queue.Full:
            LOGGER.debug("Adding stream to full queue for client %s:%s" % (
                self.port, self.channel))


##############################################################################
#
# streamer

class Streamer(object):
    """Streamer processor"""

    def __init__(self, timeout=CLOSE_EMPTY_STREAMS_AFTER_SECONDS,
        maxStreams=MAX_STREAMS_PER_CLIENT):
        self.timeout = timeout
        self.maxStreams = maxStreams
        self.lock = threading.RLock()
        # initial streams
        self.streams = {}
        # global clients
        self.clients = {}

    def getClient(self, port, channel=None):
        """Retruns a client for given port and channel"""
        try:
            client = self.clients[(port, channel)]
        except KeyError:
            # client didnt exist, create one
            LOGGER.info("Create client %s:%s" % (port, channel))
            client = Client(self, port, channel, self.timeout, self.maxStreams)
            with self.lock:
                self.clients[(port, channel)] = client
            # add initial stream
            streams = self.streams.get(channel)
            for id, msg in streams.items():
                client.addStream(msg)
        return client

    def delClient(self, port, channel):
        """Remove the given client"""
        LOGGER.info("Remove client %s:%s" % (port, channel))
        key = port, channel
        with self.lock:
            if key in self.clients:
                # if client still exists remove them now
                del self.clients[key]

    def addStream(self, channel, id, data):
        """Add widget stream to all clients queues"""
        global STREAMS
        now = datetime.datetime.now()
        if data is not None:
            data['id'] = id
            data['updated'] = int(time.time())
            msg = 'data: %s\n\n' % json.dumps(data)
            # add global stream for delivery as initial data on connecting
            with self.lock:
                streams = self.streams.setdefault(channel, {})
                streams[id] = msg
            # add client streams
            for client in tuple(self.clients.values()):
                if not client.isStreaming:
                    # remove client
                    LOGGER.info("Remove client %s:%s" % (client.port,
                        client.channel))
                    key = client.port, client.channel
                    with self.lock:
                        del self.clients[key]
                elif ((client.channel is None and channel is None) or
                    (client.channel == channel)):
                    # add stream message
                    client.addStream(msg, now)

    # management api methods
    def getClients(self):
        for client in self.clients.values():
            yield ({
                'port': client.port,
                'channel': client.channel,
                'updated': client.updated,
                'created': client.created,
                'seen': client.seen,
                })

    def purge(self, seconds=0, port=None, channel=None):
        """Purge clients for channel, port or all streams"""
        keys = []
        now = datetime.datetime.now()
        expired = now - datetime.timedelta(seconds=seconds)
        for key, client in self.clients.items():
            prt, cName = key
            if ((port is None or port == prt) and \
                (channel is None or channel == cName) and \
                (client.seen is None or client.seen <= expired)):
                LOGGER.info("Purge client %s:%s" % (port, channel))
                # force to stop sending streams
                keys.append((port, channel))
                client.alive = False
        # remove clients
        counter = len(keys)
        if counter:
            for port, channel in keys:
                self.delClient(port, channel)
        return counter


streamer = Streamer(CLOSE_EMPTY_STREAMS_AFTER_SECONDS, MAX_STREAMS_PER_CLIENT)


def isStreaming():
    """Knows if the server is streaming"""
    global STREAMING
    return STREAMING


def stopStreams():
    """Mark as stopped and force to ignore sending streams"""
    global STREAMING
    STREAMING = False
    # purge streams
    global streamer
    return streamer.purge()


def startStreams():
    """Mark as streaming and force to send streams"""
    global STREAMING
    STREAMING = True


##############################################################################
#
# scheduler

class Scheduler(object):
    """Gevent based function scheduler"""

    def __init__(self, interval, function, *args, **kwargs):
        self.greenlet = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.stopped = False
        self.start()

    def worker(self):
        while True:
            if self.stopped:
                break
            gevent.spawn(self.function, *self.args, **self.kwargs)
            gevent.sleep(self.interval)

    def start(self):
        self.greenlet = gevent.spawn(self.worker)

    def stop(self):
        self.stopped = True
        gevent.sleep(self.interval + 1)
        self.greenlet.kill()

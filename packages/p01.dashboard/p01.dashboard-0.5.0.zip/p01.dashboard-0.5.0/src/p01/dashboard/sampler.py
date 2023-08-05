##############################################################################
#
# Copyright (c) 2013 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""Dashboard data sampler
$Id: sampler.py 4549 2017-01-05 15:08:07Z roger.ineichen $
"""
__docformat__ = 'restructuredtext'

import zope.component

import p01.dashboard.processor
import p01.dashboard.interfaces


def startSamplers():
    for (name, sampler) in zope.component.getUtilitiesFor(
        p01.dashboard.interfaces.ISampler):
        sampler.start()


def stopSamplers():
    for (name, sampler) in zope.component.getUtilitiesFor(
        p01.dashboard.interfaces.ISampler):
        sampler.stop()


@zope.interface.implementer(p01.dashboard.interfaces.ISampler)
class SamplerBase(object):
    """Sampler base class"""

    def __init__(self, interval=5, streamer=None):
        self.interval = interval
        if streamer is None:
            streamer = p01.dashboard.processor.streamer
        self.streamer = streamer
        self._scheduler = None

    def start(self):
        self._scheduler = p01.dashboard.processor.Scheduler(self.interval,
            self._enqueue)

    def stop(self):
        self._scheduler.stop()

    @property
    def channel(self):
        """Defines the streaming channel (None is used as as default)"""
        return None

    @property
    def name(self):
        """Defines the sampler name used as widget.id"""
        raise NotImplementedError("Subclass must implement name property")

    @property
    def data(self):
        """Get sampler data"""
        raise NotImplementedError("Subclass must implement data property")

    def _enqueue(self):
        """Put widget data into queue"""
        self.streamer.addStream(self.channel, self.name, self.data)

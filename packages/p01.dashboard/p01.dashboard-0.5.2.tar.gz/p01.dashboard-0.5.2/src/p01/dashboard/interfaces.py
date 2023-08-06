##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""
"""
__docformat__ = "reStructuredText"

import zope.interface
import zope.publisher.interfaces.http


class ISSEResult(zope.publisher.interfaces.http.IResult):
    """Server sent event result"""

    def close(self):
        """Mark the connnection as closed and force to cleanup sampler"""


class ISampler(zope.interface.Interface):
    """Sampler component (utility) base interface

    Note: the start method must add one or more streams. A scheduler must make
    sure that this streams periodicaly get added to the streamer.

    Something like:

        import p01.dashboard.processor

        @zope.interface.implementer(ISampler)
        class MinimalSampler(object):

            def __init__(self):
                self.streamer = p01.dashboard.processor.streamer
                self.interval = 60
                self._scheduler = None

            def start(self):
                self._scheduler = p01.dashboard.processor.Scheduler(
                    self.interval, self.tick)

            def stop(self):
                if self._scheduler is not None:
                    self._scheduler.stop()

            def tick(self):
                self.streamer.addStream(channel, name, data)

    """

    def start():
        """Start sampler"""

    def stop():
        """Stop sampler"""


class ISimpleSampler(ISampler):
    """Simple sampler offering built-in widget data and stream adding"""

    name = zope.schema.TextLine(
        title=u'Sampler name',
        description=u'Sampler name',
        required=True,
        )

    channel = zope.schema.TextLine(
        title=u'Sampler channel name',
        description=u'Sampler channel name',
        default=None,
        required=False,
        )

    data = zope.schema.Field(
        title=u'Sampler data stream',
        description=u'Sampler data stream',
        required=True,
        )


class IDashboardAware(zope.interface.Interface):
    """Dashboard aware object"""

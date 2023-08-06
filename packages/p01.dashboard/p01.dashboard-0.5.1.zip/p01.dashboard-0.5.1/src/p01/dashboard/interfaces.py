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
    """Sampler component (utility)"""

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

    def start():
        """Start sampler"""

    def stop():
        """Stop sampler"""

    def _enqueue():
        """Put widget data into queue"""


class IDashboardAware(zope.interface.Interface):
    """Dashboard aware object"""

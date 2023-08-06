##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""
$Id: __init__.py 4549 2017-01-05 15:08:07Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import p01.dashboard.sampler
import p01.dashboard.processor


class WSGIServerMixin(object):
    """Sampler and processor start/stop mixin used for gevent WSGIServer"""

    def start(self):
        # start samplers
        p01.dashboard.sampler.startSamplers()
        # start streaming
        p01.dashboard.processor.startStreams()
        # sart wsgi server
        super(WSGIServerMixin, self).start()

    def stop(self, timeout=None):
        """Stop server and sampler scheduler"""
        # stop streaming
        p01.dashboard.processor.stopStreams()
        # stop samplers
        p01.dashboard.sampler.stopSamplers()
        # stop wsgi server
        super(WSGIServerMixin, self).stop(timeout)

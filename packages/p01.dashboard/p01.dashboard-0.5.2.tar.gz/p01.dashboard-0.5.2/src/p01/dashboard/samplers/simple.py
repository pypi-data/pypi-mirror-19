        ##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""Simple sampler usning a name and callable
$Id: simple.py 4549 2017-01-05 15:08:07Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import zope.interface

import p01.dashboard.sampler
import p01.dashboard.interfaces


@zope.interface.implementer(p01.dashboard.interfaces.ISampler)
class SimpleSampler(p01.dashboard.sampler.SamplerBase):
    """Simple sampler using a name and callable method"""

    name = None
    func = None

    def __init__(self, name=None, channel=None, func=None, interval=60):
        super(SimpleSampler, self).__init__(interval)
        self.name = name
        self.channel = channel
        self.func = func

    @property
    def data(self):
        """Returns the data for the relevant dashboard widget

        Note: each widget requires a custom data format. See the documentation
        for more information. Or write your own widget and use your own data.
        """
        return self.func()

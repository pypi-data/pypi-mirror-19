        ##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""XError server status widget
$Id: xerror.py 4549 2017-01-05 15:08:07Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import urllib
import urlparse

import zope.interface

import p01.json.proxy
import p01.json.transport

import p01.dashboard.sampler
import p01.dashboard.interfaces


def getJSONPRCProxy(url):
    """Returns a jsonrpc proxy for the given url"""
    parsed = urlparse.urlparse(url)
    if parsed.username is not None and parsed.password is not None:
        # first remove user, password from netloc
        netloc = urllib.splituser(parsed.netloc)[1]
        url = '%s://%s%s' % (parsed.scheme, netloc, parsed.path)
        if parsed.scheme == 'https':
            transport = p01.json.transport.SafeBasicAuthTransport(
                username=parsed.username, password=parsed.password)
        else:
            transport = p01.json.transport.BasicAuthTransport(
                username=parsed.username, password=parsed.password)
    else:
        if parsed.scheme == 'https':
            transport = p01.json.transport.SafeTransport()
        else:
            transport = p01.json.transport.Transport()
    return p01.json.proxy.JSONRPCProxy(url, transport=transport)


@zope.interface.implementer(p01.dashboard.interfaces.ISampler)
class XErrorSampler(p01.dashboard.sampler.SamplerBase):
    """XError sampler"""

    url = None
    channel = None
    username = None
    password = None

    def __init__(self, url, channel=None, interval=60):
        super(XErrorSampler, self).__init__(interval)
        self.url = url
        self.channel = channel

    @property
    def name(self):
        return 'xerror'

    @property
    def data(self):
        items = []
        proxy = getJSONPRCProxy(self.url)
        for data in proxy.getSummary():
            errors = data.get('errors')
            users = data.get('users')
            value = '%s (%s)' % (errors, users)
            if errors:
                css = 'errors'
            else:
                css = 'success'
            items.append({
                'label': data.get('title'),
                'value': value,
                'errors': errors,
                'users': users,
                'css': css,
            })
        return {'items':items}


################################################################################
#
# setup your custom XError sampler with something like:
#
# XERROR = 'https://username:password@error.domain.tld'
#
# sampler = BuildbotSampler(XERROR, interval=60)

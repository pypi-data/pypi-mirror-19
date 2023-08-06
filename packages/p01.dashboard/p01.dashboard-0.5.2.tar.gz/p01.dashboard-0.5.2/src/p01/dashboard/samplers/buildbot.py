##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""Buildbot status widget
$Id: buildbot.py 4549 2017-01-05 15:08:07Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import json

import requests

import zope.interface

import p01.dashboard.sampler
import p01.dashboard.interfaces


# URL template for fetching JSON data about builds.
URL = ('%(url)s/json/builders/%(name)s/builds/%(build)s?as_text=1&filter=0')
LATEST = -1

# Status codes that can be returned by the getBuildStatus method
# From buildbot.status.builder.
# See: http://docs.buildbot.net/current/developer/results.html
SUCCESS, WARNINGS, FAILURE, SKIPPED, EXCEPTION, RETRY, TRYPENDING = range(7)
OK = (SUCCESS, WARNINGS)  # These indicate build is complete.
FAILED = (FAILURE, EXCEPTION, SKIPPED)  # These indicate build failure.
PENDING = (RETRY, TRYPENDING)  # These indicate in progress or in pending queue.


STATI = {
    SUCCESS: 'success',
    WARNINGS: 'warning',
    FAILURE: 'failure',
    SKIPPED: 'skipped',
    EXCEPTION: 'exception',
    RETRY: 'retry',
    TRYPENDING: 'pending',
}


def _getBuildData(url):
    """Fetches JSON data for the all the builds from the try server.
    Args:
    url: A try server URL to fetch builds information.
    Returns:
    A dictionary with information of all build on the try server.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
    except Exception, e:
        pass
    return {}


def getBuildStatus(url, name, build=LATEST):
    """Gets build status from the buildbot status page for a given build number.
    Args:
    build: A build number on try server to determine its status.
    name: Name of the bot where the build information is scanned.
    url: URL of the buildbot.
    Returns:
    The buildbot status number, see
    http://docs.buildbot.net/current/developer/results.html for more info
    """
    # Get the URL for requesting JSON data with status information.
    url = URL % {
        'url': url,
        'name': name,
        'build': build,
    }
    data = _getBuildData(url)
    checked = False
    success = True
    status = None
    if data.get('results') in FAILED:
        status = data.get('results')
    elif data.get('steps'):
        for item in data.get('steps'):
            status = item.get('results')[0]
            # The 'results' attribute of each step consists of two elements,
            # results[0]: This represents the status of build step.
            # See: http://docs.buildbot.net/current/developer/results.html
            # results[1]: List of items, contains text if step fails, otherwise
            # empty.
            if not (item.get('isFinished') and item.get('results')[0] in OK):
                # not finished or failed status
                break
    return STATI.get(status)


@zope.interface.implementer(p01.dashboard.interfaces.ISampler)
class BuildbotSampler(p01.dashboard.sampler.SamplerBase):
    """Buildbot sampler"""

    url = None
    projects = None
    channel = None

    def __init__(self, url, projects, channel=None, interval=60):
        super(BuildbotSampler, self).__init__(interval)
        self.url = url
        self.projects = projects
        self.channel = channel

    @property
    def name(self):
        return 'buildbot'

    @property
    def data(self):
        items = []
        for name in sorted(self.projects):
            status = getBuildStatus(self.url, name)
            if status is not None:
                items.append({
                    'label': name,
                    'value': status,
                    'css': status,
                })
            else:
                items.append({
                    'label': name,
                    'value': 'unavailable',
                    'css': 'exception',
                })
        return {'items':items}


################################################################################
#
# setup your custom buildbot sampler with something like:
#
# BUILDBOT = 'https://username:password@buildbot.domain.tld'
#
# PROJECTS = ['demo', 'demo.release']
#
# sampler = BuildbotSampler(BUILDBOT, PROJECTS, interval=60)

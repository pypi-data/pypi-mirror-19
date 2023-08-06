##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""Graphite image rendering proxy
$Id: graphite.py 4549 2017-01-05 15:08:07Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import requests


class GraphiteRenderView(object):
    """Graphite render view (proxy to graphite)

    Configure a GraphiteRenderView as graphite-render view and define your
    graphite url in the view:

      <page
          name="graphite-render"
          for="p01.dashboard.interfaces.IDashboardAware"
          class=".graphite.GraphiteRenderView"
          layer="xdashboard.layer.IBaseLayer"
          permission="p01:dashboard:View"
          />

    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def url(self):
        raise NotImplementedError("Subclass must implement url property")

    def __call__(self):
        data = self.request.get('wsgi.input')
        if data:
            data = data.read()
        data = data and data or None
        response = requests.request(self.request.method, self.url, data=data)
        return response.text

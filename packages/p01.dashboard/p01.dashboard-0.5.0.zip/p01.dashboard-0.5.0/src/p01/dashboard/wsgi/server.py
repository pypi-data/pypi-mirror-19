##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""
$Id: server.py 4549 2017-01-05 15:08:07Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import gevent.pywsgi

import p01.dashboard.wsgi


class WSGIServer(p01.dashboard.wsgi.WSGIServerMixin, gevent.pywsgi.WSGIServer):
    """Gevent server serving dashboard sampler data"""


def server_factory(global_conf, host, port):
    """Paste server factory using gevent

    NOTE: use circus and chausette server factory for production use
    This is only used for development.
    """

    port = int(port)

    def serve(app):
        print 'WSGIServer serving at http://%s:%s' % (host, port)
        # server = WSGIServer((host, port), app, handler_class=WebSocketHandler)
        server = WSGIServer((host, port), app)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print 'Exiting with KeyboardInterrupt'
            server.stop()
    return serve

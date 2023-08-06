##############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""pywsgi servre factory
$Id: circus.py 4549 2017-01-05 15:08:07Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import sys
import os
import socket
import argparse

import gevent.pywsgi
import paste.deploy

import p01.dashboard.wsgi


_ADDRESS_FAMILY = {
    'AF_INET': socket.AF_INET,
    'AF_INET6': socket.AF_INET6
}

try:
    _ADDRESS_FAMILY['AF_UNIX'] = socket.AF_UNIX
    AF_UNIX = socket.AF_UNIX
except AttributeError:
    # windows doesn't support AF_UNIX
    AF_UNIX = object()

_SOCKET_TYPE = {
    'SOCK_STREAM': socket.SOCK_STREAM,
    'SOCK_DGRAM': socket.SOCK_DGRAM,
    'SOCK_RAW': socket.SOCK_RAW,
    'SOCK_RDM': socket.SOCK_RDM,
    'SOCK_SEQPACKET': socket.SOCK_SEQPACKET
}


def create_socket(host, port=0, family=socket.AF_INET, type=socket.SOCK_STREAM,
    backlog=2048, blocking=True):
    try:
        if not host.startswith('unix:') and family == socket.AF_UNIX:
            raise ValueError('Your host needs to have the unix:/path form')
        if host.startswith('unix:') and family != socket.AF_UNIX:
            # forcing to unix socket family
            family = socket.AF_UNIX
    except AttributeError:
        # windows doen't have AF_UNIX
        if host.startswith('unix:'):
            raise ValueError('No unix no unix:socket')

    if host.startswith('fd://'):
        # just recreate the socket
        fd = int(host.split('://')[1])
        sock = socket.fromfd(fd, family, type)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    else:
        sock = socket.socket(family, type)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if host.startswith('unix:'):
            filename = host[len('unix:'):]
            try:
                os.remove(filename)
            except OSError:
                pass
            sock.bind(filename)
        else:
            sock.bind((host, port))
        sock.listen(backlog)

    if blocking:
        sock.setblocking(1)
    else:
        sock.setblocking(0)
    return sock


class WSGIHandler(gevent.pywsgi.WSGIHandler):
    """WSGI request handler supporting socket"""

    def __init__(self, sock, address, server, rfile=None):
        try:
            if server.socket_type == socket.AF_UNIX:
                address = ['0.0.0.0']
        except AttributeError:
            # windows
            pass
        super(WSGIHandler, self).__init__(sock, address, server, rfile)



class WSGIServer(p01.dashboard.wsgi.WSGIServerMixin, gevent.pywsgi.WSGIServer):
    """Gevent server serving dashboard sampler data"""

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    handler_class = WSGIHandler

    def __init__(self, listener, application=None, backlog=2048,
        spawn='default', environ=None,
        socket_type=socket.SOCK_STREAM, address_family=socket.AF_INET,
        **ssl_args):
        # create socket
        self.address_family = address_family
        self.socket_type = socket_type
        host, port = listener
        self.socket = create_socket(host, port, self.address_family,
            self.socket_type, backlog=backlog)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = self.socket.getsockname()
        # init
        super(WSGIServer, self).__init__(self.socket, application=application,
            backlog=None, spawn=spawn, environ=environ, **ssl_args)


def main():
    """Setup and start a WSGI server

    NOTE: this method is registered as a console circus script and is only used
    for run the WSGI server from a circus daemon.

    The circus watcher config looks like:

    [watcher:...]
    working_dir = /...
    cmd = /.../bin/circus --fd $(circus.sockets....) paste:.../paste.ini

    """
    sys.path.append(os.curdir)
    parser = argparse.ArgumentParser(description='Run some watchers.')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--address-family', type=str, default='AF_INET',
                        choices=sorted(_ADDRESS_FAMILY.keys()))
    parser.add_argument('--socket-type', type=str, default='SOCK_STREAM',
                        choices=sorted(_SOCKET_TYPE.keys()))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--host', default='localhost')
    group.add_argument('--fd', type=int, default=-1)

    group.add_argument('--backlog', type=int, default=2048)
    parser.add_argument('--spawn', type=int, default=None,
                        help="Spawn type")
    parser.add_argument('application', nargs='?')
    args = parser.parse_args()

    application = args.application

    path = application.split(':')[-1]
    app = paste.deploy.loadapp('config:%s' % os.path.abspath(path))

    if args.fd != -1:
        host = 'fd://%d' % args.fd
    else:
        host = args.host

    address_family = _ADDRESS_FAMILY[args.address_family]
    socket_type = _SOCKET_TYPE[args.socket_type]
    skws = {
        'backlog': args.backlog,
        'address_family': address_family,
        'socket_type': socket_type,
    }
    if args.spawn is not None:
        skws['spawn'] = args.spawn

    if host.startswith('fd://') or host.startswith('unix:'):
        print 'WSGIServer serving on %s' % host
    else:
        print 'WSGIServer serving on %s:%s' % (host, args.port)
    server = WSGIServer((host, args.port), app, **skws)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    main()

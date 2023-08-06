'''Asynchronous application for serving requests
on sockets. This is the base class of :class:`.WSGIServer`.
All is needed by a :class:`.SocketServer` application is a callable
which build a :class:`.ProtocolConsumer` for each new client request
received.
This is an example of a script for an Echo server::

    import pulsar
    from pulsar.apps.socket import SocketServer

    class EchoServerProtocol(pulsar.ProtocolConsumer):
        ...

    if __name__ == '__main__':
        SocketServer(EchoServerProtocol).start()

Check the :ref:`echo server example <tutorials-writing-clients>` for detailed
implementation of the ``EchoServerProtocol`` class.

.. _socket-server-settings:

Socket Server Settings
==============================
All standard :ref:`application settings <settings>` can be applied to a
:class:`SocketServer`. In addition, the following are
specific to sockets and can be used to fine tune your application:

bind
------
To specify the address to bind the server to::

    python script.py --bind 127.0.0.1:8070

This will accept connection from the 127.0.0.1 network interface and port 8070.
This means pulsar will be able to accept connections only from clients
running into the same computer it is running.

On the other hand, it is possible to listen for connections from all
the network interfaces available on the server by specifying ``:<port>``.
For example, this will listen for both ipv4 and ipv6 sockets **on all hosts**
on port 8080::

    python script.py --bind :8080

**Use this notation when running pulsar inside Docker or any other container**.

You can bind to a random available port by specifying 0 as the port number::

    python script.py --bind :0

useful during testing.


backlog
---------
To specify the maximum number of queued connections you can use the
:ref:`backlog <setting-backlog>` settings. For example::

    python script.py --backlog 1000

rarely used.

keep_alive
---------------
To control how long a server :class:`.Connection` is kept alive after the
last read from the remote client, one can use the
:ref:`keep-alive <setting-keep_alive>` setting::

    python script.py --keep-alive 10

will close client connections which have been idle for 10 seconds.

.. _socket-server-ssl:

TLS/SSL support
------------------------
Transport Layer Security (often known as Secure Sockets Layer) is handled by
the :ref:`cert-file <setting-cert_file>` and :ref:`key-file <setting-key_file>`
settings::

    python script.py --cert-file server.crt --key-file server.key


.. _socket-server-concurrency:

Concurrency
==================

When running a :class:`SocketServer` in multi-process mode (default),
the application, create a listening socket in the parent (Arbiter) process
and then spawn several process-based actors which listen on the
same shared socket.
This is how pre-forking servers operate.

When running a :class:`SocketServer` in threading mode::

    python script.py --concurrency thread

the number of :class:`.Actor` serving the application is set
to ``0`` so that the application is actually served by the
arbiter event-loop (we refer this to a single process server).
This configuration is used when debugging, testing, benchmarking or on small
load servers.

In addition, a :class:`SocketServer` in multi-process mode is only available
for:

* Posix systems.
* Windows running python 3.2 or above (python 2 on windows does not support
  the creation of sockets from file descriptors).

Check the :meth:`SocketServer.monitor_start` method for implementation details.
'''
import os
import socket
from math import log
from random import lognormvariate
from functools import partial
try:
    import ssl
except ImportError:     # pragma    nocover
    ssl = None

import pulsar
from pulsar import TcpServer, DatagramServer, Connection, ImproperlyConfigured
from pulsar import as_coroutine
from pulsar.utils.internet import parse_address
from pulsar.utils.config import pass_through


class SocketSetting(pulsar.Setting):
    virtual = True
    app = 'socket'
    section = "Socket Servers"


class Bind(SocketSetting):
    name = "bind"
    flags = ["-b", "--bind"]
    meta = "ADDRESS"
    default = "127.0.0.1:{0}".format(pulsar.DEFAULT_PORT)
    desc = """\
        The socket to bind.

        A string of the form: ``HOST``, ``HOST:PORT``, ``unix:PATH``.
        An IP is a valid HOST. Specify ``:PORT`` to listen for connections
        from all the network interfaces available on the server.
        """


class KeepAlive(SocketSetting):
    name = "keep_alive"
    flags = ["--keep-alive"]
    validator = pulsar.validate_pos_int
    type = int
    default = 15
    desc = """\
        The number of seconds to keep an idle client connection
        open."""


class Backlog(SocketSetting):
    name = "backlog"
    flags = ["--backlog"]
    validator = pulsar.validate_pos_int
    type = int
    default = 2048
    desc = """\
        The maximum number of queued connections in a socket.

        This refers to the number of clients that can be waiting to be served.
        Exceeding this number results in the client getting an error when
        attempting to connect. It should only affect servers under significant
        load.
        Must be a positive integer. Generally set in the 64-2048 range.
        """


class KeyFile(SocketSetting):
    name = "key_file"
    flags = ["--key-file"]
    meta = "FILE"
    default = None
    desc = """\
    SSL key file
    """


class CertFile(SocketSetting):
    name = "cert_file"
    flags = ["--cert-file"]
    meta = "FILE"
    default = None
    desc = """\
    SSL certificate file
    """


class SocketServer(pulsar.Application):
    '''A :class:`.Application` which serve application on a socket.

    It bind a socket to a given address and listen for requests. The request
    handler is constructed from the callable passed during initialisation.

    .. attribute:: address

        The socket address, available once the application has started.
    '''
    name = 'socket'
    cfg = pulsar.Config(apps=['socket'])

    def protocol_factory(self):
        '''Factory of :class:`.ProtocolConsumer` used by the server.

        By default it returns the :meth:`.Application.callable`.
        '''
        return partial(Connection, self.cfg.callable)

    async def monitor_start(self, monitor):
        '''Create the socket listening to the ``bind`` address.

        If the platform does not support multiprocessing sockets set the
        number of workers to 0.
        '''
        cfg = self.cfg
        if (not pulsar.platform.has_multiProcessSocket or
                cfg.concurrency == 'thread'):
            cfg.set('workers', 0)
        if not cfg.address:
            raise ImproperlyConfigured('Could not open a socket. '
                                       'No address to bind to')
        address = parse_address(self.cfg.address)
        if cfg.cert_file or cfg.key_file:
            if not ssl:
                raise RuntimeError('No support for ssl')
            if cfg.cert_file and not os.path.exists(cfg.cert_file):
                raise ImproperlyConfigured('cert_file "%s" does not exist' %
                                           cfg.cert_file)
            if cfg.key_file and not os.path.exists(cfg.key_file):
                raise ImproperlyConfigured('key_file "%s" does not exist' %
                                           cfg.key_file)
        # First create the sockets
        try:
            server = await self.create_server(monitor, address)
        except socket.error as e:
            raise ImproperlyConfigured(e) from None
        else:
            monitor.servers[self.name] = server
            self.cfg.addresses = server.addresses

    def actorparams(self, monitor, params):
        params['sockets'] = monitor.servers[self.name].sockets

    async def worker_start(self, worker, exc=None):
        '''Start the worker by invoking the :meth:`create_server` method.
        '''
        if not exc and self.name not in worker.servers:
            server = await self.create_server(worker)
            server.bind_event('stop', lambda _, **kw: worker.stop())
            worker.servers[self.name] = server

    async def worker_stopping(self, worker, exc=None):
        server = worker.servers.get(self.name)
        if server:
            await server.close()
        close = getattr(self.cfg.callable, 'close', None)
        if hasattr(close, '__call__'):
            try:
                await as_coroutine(close())
            except Exception:
                pass

    def worker_info(self, worker, info):
        server = worker.servers.get(self.name)
        if server:
            info['%sserver' % self.name] = server.info()
        return info

    def server_factory(self, *args, **kw):
        '''Create a :class:`.TcpServer`.
        '''
        return TcpServer(*args, **kw)

    #   INTERNALS
    async def create_server(self, worker, address=None):
        '''Create the Server which will listen for requests.

        :return: a :class:`.TcpServer`.
        '''
        sockets = worker.sockets if not address else None
        cfg = self.cfg
        max_requests = cfg.max_requests
        if max_requests:
            max_requests = int(lognormvariate(log(max_requests), 0.2))
        server = self.server_factory(
            self.protocol_factory(),
            worker._loop,
            sockets=sockets,
            address=address,
            max_requests=max_requests,
            keep_alive=cfg.keep_alive,
            name=self.name,
            logger=self.logger
        )
        for event in ('connection_made', 'pre_request', 'post_request',
                      'connection_lost'):
            callback = getattr(cfg, event)
            if callback != pass_through:
                server.bind_event(event, callback)
        await server.start_serving(cfg.backlog, sslcontext=self.sslcontext())
        return server

    def sslcontext(self):
        cfg = self.cfg
        if cfg.cert_file and cfg.key_file:
            ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ctx.load_cert_chain(certfile=cfg.cert_file, keyfile=cfg.key_file)
            return ctx


class UdpSocketServer(SocketServer):
    '''A :class:`.SocketServer` which serves application on a UDP sockets.

    It binds a socket to a given address and listen for requests. The request
    handler is constructed from the callable passed during initialisation.

    .. attribute:: address

        The socket address, available once the application has started.
    '''
    name = 'udpsocket'
    cfg = pulsar.Config(apps=['socket'])

    def protocol_factory(self):
        '''Return the :class:`.DatagramProtocol` factory.
        '''
        return self.cfg.callable

    async def monitor_start(self, monitor):
        '''Create the socket listening to the ``bind`` address.

        If the platform does not support multiprocessing sockets set the
        number of workers to 0.
        '''
        cfg = self.cfg
        if (not pulsar.platform.has_multiProcessSocket or
                cfg.concurrency == 'thread'):
            cfg.set('workers', 0)
        if not cfg.address:
            raise pulsar.ImproperlyConfigured('Could not open a socket. '
                                              'No address to bind to')
        address = parse_address(self.cfg.address)
        server = await self.create_server(monitor, address)
        monitor.servers[self.name] = server
        self.cfg.addresses = server.addresses

    def server_factory(self, *args, **kw):
        '''By default returns a new :class:`.DatagramServer`.
        '''
        return DatagramServer(*args, **kw)

    #   INTERNALS
    async def create_server(self, worker, address=None):
        '''Create the Server which will listen for requests.

        :return: the server obtained from :meth:`server_factory`.
        '''
        sockets = worker.sockets if not address else None
        cfg = self.cfg
        max_requests = cfg.max_requests
        if max_requests:
            max_requests = int(lognormvariate(log(max_requests), 0.2))
        server = self.server_factory(self.protocol_factory(),
                                     worker._loop,
                                     sockets=sockets,
                                     address=address,
                                     max_requests=max_requests,
                                     name=self.name,
                                     logger=self.logger)
        server.bind_event('stop', lambda _, **kw: worker.stop())
        for event in ('pre_request', 'post_request'):
            callback = getattr(cfg, event)
            if callback != pass_through:
                server.bind_event(event, callback)
        await server.create_endpoint()
        return server

.. image:: https://pulsar.fluidily.com/assets/images/pulsar-banner-600.svg
   :alt: Pulsar
   :width: 300

|
|

:Badges: |license|  |pyversions| |status| |pypiversion|
:Master CI: |master-build|_ |coverage-master| |appveyor|
:Documentation: http://quantmind.github.io/pulsar/
:Downloads: http://pypi.python.org/pypi/pulsar
:Source: https://github.com/quantmind/pulsar
:Stack overflow: questions tagged python-pulsar_
:Mailing list: `google user group`_
:Design by: `Quantmind`_ and `Luca Sbardella`_
:Platforms: Linux, OSX, Windows. Python 3.5 and above
:Keywords: client, server, asynchronous, concurrency, actor, thread, process,
    socket, wsgi, websocket, redis, json-rpc

.. |pypiversion| image:: https://badge.fury.io/py/pulsar.svg
    :target: https://pypi.python.org/pypi/pulsar
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/pulsar.svg
  :target: https://pypi.python.org/pypi/pulsar
.. |license| image:: https://img.shields.io/pypi/l/pulsar.svg
  :target: https://pypi.python.org/pypi/pulsar
.. |status| image:: https://img.shields.io/pypi/status/pulsar.svg
  :target: https://pypi.python.org/pypi/pulsar
.. |downloads| image:: https://img.shields.io/pypi/dd/pulsar.svg
  :target: https://pypi.python.org/pypi/pulsar
.. |master-build| image:: https://travis-ci.org/quantmind/pulsar.svg?branch=master
.. _master-build: http://travis-ci.org/quantmind/pulsar
.. |dev-build| image:: https://travis-ci.org/quantmind/pulsar.svg?branch=dev
.. _dev-build: http://travis-ci.org/quantmind/pulsar
.. |coverage-master| image:: https://coveralls.io/repos/github/quantmind/pulsar/badge.svg?branch=master
  :target: https://coveralls.io/github/quantmind/pulsar?branch=master
.. |coverage-dev| image:: https://coveralls.io/repos/github/quantmind/pulsar/badge.svg?branch=dev
  :target: https://coveralls.io/github/quantmind/pulsar?branch=dev
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/w2ip01j07qm161ei?svg=true
    :target: https://ci.appveyor.com/project/lsbardel/pulsar


An example of a web server written with ``pulsar`` which responds with
"Hello World!" for every request:

.. code:: python

    from pulsar.apps import wsgi

    def hello(environ, start_response):
        data = b'Hello World!\n'
        response_headers = [
            ('Content-type','text/plain'),
            ('Content-Length', str(len(data)))
        ]
        start_response('200 OK', response_headers)
        return [data]


    if __name__ == '__main__':
        wsgi.WSGIServer(callable=hello).start()


Pulsar's goal is to provide an easy way to build scalable network programs.
In the ``Hello world!`` web server example above, many client
connections can be handled concurrently.
Pulsar tells the operating system (through epoll or select) that it should be
notified when a new connection is made, and then it goes to sleep.

Pulsar uses the asyncio_ module from the standard python
library and it can be configured to run in multi-processing mode.

Another example of pulsar framework is the asynchronous HttpClient_:

.. code:: python

    from pulsar.apps import http

    async with http.HttpClient() as session:
        response1 = await session.get('https://github.com/timeline.json')
        response2 = await session.get('https://api.github.com/emojis.json')


The http client maintains connections alive (by default 15 seconds) and therefore
any requests that you make within a session will automatically reuse the
appropriate connection. All connections are released once the session exits the
asynchronous ``with`` block.

Installing
============

Pulsar has no hard dependencies, install via pip::

    pip install pulsar

or download the tarball from pypi_.


Applications
==============
Pulsar design allows for a host of different asynchronous applications
to be implemented in an elegant and efficient way.
Out of the box it is shipped with the the following:

* Socket servers
* `Asynchronous WSGI server`_
* HttpClient_
* JSON-RPC_
* `Web Sockets`_
* `Asynchronous Test suite`_
* `Data stores`_ (with async Redis client)
* `Task queue consumers`_
* `Asynchronous botocore`_
* `django integration`_

.. _examples:

Examples
=============
Check out the ``examples`` directory for various working applications.
It includes:

* Hello world! wsgi example
* An Httpbin WSGI application
* An HTTP Proxy server
* A JSON-RPC Calculator server
* Websocket random graph.
* Websocket chat room.
* The `dining philosophers problem <http://en.wikipedia.org/wiki/Dining_philosophers_problem>`_.
* `Twitter streaming <https://github.com/quantmind/pulsar-twitter>`_


Design
=============
Pulsar internals are based on `actors primitive`_. ``Actors`` are the *atoms*
of pulsar's concurrent computation, they do not share state between them,
communication is achieved via asynchronous inter-process message passing,
implemented using the standard python socket library.

Two special classes of actors are the ``Arbiter``, used as a singleton_,
and the ``Monitor``, a manager of several actors performing similar functions.
The Arbiter runs the main eventloop and it controls the life of all actors.
Monitors manage group of actors performing similar functions, You can think
of them as a pool of actors.

.. image:: https://pulsar.fluidily.com/assets/images/actors.png
   :alt: Pulsar Actors

More information about design and philosophy in the documentation.


Add-ons
=========
Pulsar checks if some additional libraries are available at runtime, and
uses them to add additional functionalities or improve performance:

* greenlet_: required by the `pulsar.apps.greenio`_ module and useful for
  developing implicit asynchronous applications
* uvloop_: if available it is possible to use it as the default event loop
  for actors by passing ``--io uv`` in the command line (or ``event_loop="uv"``
  in the config file)
* http-parser_: if available, the default HttpParser for both client and server
  is replaced by the C implementation in this package (about three times faster
  than pulsar python version)
* setproctitle_: if installed, pulsar can use it to change the processes names
  of the running application
* psutil_: if installed, a ``system`` key is available in the dictionary
  returned by Actor info method
* python-certifi_: The HttpClient_ will attempt to use certificates from
  certifi if it is present on the system
* ujson_: if installed it is used instead of the native ``json`` module
* unidecode_: to enhance the ``slugify`` function


Running Tests
==================
Pulsar test suite uses the pulsar test application. To run tests::

    python setup.py test

For options and help type::

    python setup.py test --help

flake8_ check (requires flake8 package)::

    flake8


.. _contributing:

Contributing
=================
Development of pulsar_ happens at Github. We very much welcome your contribution
of course. To do so, simply follow these guidelines:

* Fork pulsar_ on github
* Create a topic branch ``git checkout -b my_branch``
* Push to your branch ``git push origin my_branch``
* Create an issue at https://github.com/quantmind/pulsar/issues with
  pull request for the **dev branch**.
* Alternatively, if you need to report a bug or an unexpected behaviour, make sure
  to include a mcve_ in your issue.

A good ``pull`` request should:

* Cover one bug fix or new feature only
* Include tests to cover the new code (inside the ``tests`` directory)
* Preferably have one commit only (you can use rebase_ to combine several
  commits into one)
* Make sure ``flake8`` tests pass

.. _license:

License
=============
This software is licensed under the BSD_ 3-clause License. See the LICENSE
file in the top distribution directory for the full license text.

.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _multiprocessing: http://docs.python.org/library/multiprocessing.html
.. _`actors primitive`: http://en.wikipedia.org/wiki/Actor_model
.. _setproctitle: http://code.google.com/p/py-setproctitle/
.. _psutil: https://github.com/giampaolo/psutil
.. _pypi: http://pypi.python.org/pypi/pulsar
.. _BSD: http://opensource.org/licenses/BSD-3-Clause
.. _pulsar: https://github.com/quantmind/pulsar
.. _singleton: http://en.wikipedia.org/wiki/Singleton_pattern
.. _cython: http://cython.org/
.. _`google user group`: https://groups.google.com/forum/?fromgroups#!forum/python-pulsar
.. _flake8: https://pypi.python.org/pypi/flake8
.. _ujson: https://pypi.python.org/pypi/ujson
.. _rebase: https://help.github.com/articles/about-git-rebase
.. _unidecode: https://pypi.python.org/pypi/Unidecode
.. _`Luca Sbardella`: http://lucasbardella.com
.. _`Quantmind`: http://quantmind.com
.. _JSON-RPC: http://www.jsonrpc.org/
.. _mcve: http://stackoverflow.com/help/mcve
.. _python-certifi: https://certifi.io
.. _greenlet: http://greenlet.readthedocs.io/
.. _`pulsar.apps.greenio`: https://github.com/quantmind/pulsar/tree/master/pulsar/apps/greenio
.. _`pulsar.apps.pulse`: https://github.com/quantmind/pulsar/tree/master/pulsar/apps/pulse
.. _HttpClient: http://quantmind.github.io/pulsar/apps/http.html
.. _`Data stores`: http://quantmind.github.io/pulsar/apps/data/index.html
.. _`Task queue consumers`: https://github.com/quantmind/pulsar-queue
.. _`Asynchronous botocore`: https://github.com/quantmind/pulsar-cloud
.. _`django integration`: https://github.com/quantmind/pulsar-django
.. _`python-pulsar`: http://stackoverflow.com/questions/tagged/python-pulsar
.. _`Web Sockets`: http://quantmind.github.io/pulsar/apps/websockets.html
.. _uvloop: https://github.com/MagicStack/uvloop
.. _http-parser: https://github.com/benoitc/http-parser
.. _`Asynchronous WSGI server`: http://quantmind.github.io/pulsar/apps/wsgi/index.html
.. _`Asynchronous Test suite`: http://quantmind.github.io/pulsar/apps/test.html

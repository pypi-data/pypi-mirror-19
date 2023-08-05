Tutorial
========

Let's immediately clarify where Degu is *not* a good fit:

.. warning::

    Degu is absolutely *not* suitable for serving public websites!

    The Degu server isn't built for high concurrency, and it lacks many features
    expected by typical web browsers.

If the Degu server isn't a good fit for your problem, please check out
`gunicorn`_ and `modwsgi`_.

**So where is Degu a good fit?**

Degu is a *fantastic* fit if you're implementing REST APIs for device-to-device
communication on the local network.

In a nutshell, this is the typical Degu pattern:

    1.  Application starts a :class:`degu.server.SSLServer` on a random,
        unprivileged port

    2.  Application advertises this server to peers on the local network using
        `Avahi`_ or similar

    3.  Peers use a :class:`degu.client.SSLClient` to make requests to this
        server for structured data sync, file transfer, or whatever else the
        application REST API might expose

Some noteworthy Degu features:

    *   Degu fully exposes HTTP "chunked" transfer-encoding semantics, including
        the optional per-chunk *extension*

    *   Degu fully exposes IPv6 address semantics, including the *scopeid*
        needed for IPv6 link-local addresses

    *   Degu transparently supports ``AF_INET``, ``AF_INET6``, and ``AF_UNIX``,
        all via a single *address* argument used uniformly by the server and
        client

    *   Degu provides a safe and opinionated API for using TLSv1.2, with a
        particular focus on using client certificates to authenticate incoming
        TCP connections



Example: SSL reverse-proxy
--------------------------

Here's a minimal Degu server application, implemented according to the
:doc:`rgi`:

>>> def example_app(session, request, api):
...     return (200, 'OK', {'x-msg': 'hello, world'}, None)
...

Although not particularly useful, it's still a working example in only 2 lines
of code.

It's fun and easy to create a throw-away :class:`degu.misc.TempServer` on which
to run our ``example_app``.  We'll create a server that only accepts connections
from the IPv4 looback device:

>>> from degu.misc import TempServer
>>> server = TempServer(('127.0.0.1', 0), example_app)

That just spun-up a :class:`degu.server.Server` in a new
`multiprocessing.Process`_ (which will be automatically terminated when the
:class:`degu.misc.TempServer` instance is garbage collected).

Now we'll create a :class:`degu.client.Client` using the
:attr:`degu.server.Server.address` attribute from our above ``server``, which
will include the random, unprivileged *port* assigned by the kernel:

>>> from degu.client import Client
>>> client = Client(server.address)

A :class:`degu.client.Client` is stateless and thread-safe, does not itself
reference any socket resources.  It merely specifies *where* a server is and
*how* to make connections to it.

In order to make requests, we'll need to create a
:class:`degu.client.Connection` by calling :meth:`degu.client.Client.connect()`:

>>> conn = client.connect()

In contrast, a :class:`degu.client.Connection` is stateful and is *not*
thread-safe.

Now we can use :meth:`degu.client.Connection.put()` to make a ``PUT`` request,
which will return a :class:`degu.client.Response` namedtuple:

>>> conn.put('/foo', {}, None)
Response(status=200, reason='OK', headers={'x-msg': 'hello, world'}, body=None)

As both the Degu client and server are built for HTTP/1.1 only, connection
reuse is assumed, so we can make another request to our ``server`` using the
same connection.

This time we'll use :meth:`degu.client.Connection.post()` to make a ``POST``
request:

>>> conn.post('/bar', {}, None)
Response(status=200, reason='OK', headers={'x-msg': 'hello, world'}, body=None)

After you're done using a connection, it's a good idea to explicitly close it,
although note that a connection is also automatically closed when garbage
collected.

Close a connection using :meth:`degu.client.Connection.close()`:

>>> conn.close()

Notice that the :class:`degu.client.Response` namedtuple returned above is the
exact same tuple returned by our ``example_app``.  The Degu client API and the
RGI application API have been carefully designed to complement each other.

For example, here's an RGI application that implements a `reverse-proxy`_:

>>> class ProxyApp:
...     def __init__(self, client):
...         self.client = client
... 
...     def __call__(self, session, request, api):
...         conn = session.store.get('conn')
...         if conn is None:
...             conn = self.client.connect()
...             session.store['conn'] = conn
...         return conn.request(
...             request.method,
...             request.uri,
...             request.headers,
...             request.body
...         )
... 

The important thing to note above is that a Degu reverse-proxy application can
(more-or-less) directly use the incoming HTTP request as its forwarded HTTP
client request, and can *directly* return the *entire* HTTP response from the
upstream HTTP server without transformation.

Also note that our ``ProxyApp`` uses the generic
:meth:`degu.client.Connection.request()` method, which allows you to specify any
supported HTTP request via its four arguments.

In contrast, our previous ``PUT`` and ``POST`` requests were made using the
corresponding shortcut methods, one of which exists for each supported HTTP
request *method*:

    *   :meth:`degu.client.Connection.put()`
    *   :meth:`degu.client.Connection.post()`
    *   :meth:`degu.client.Connection.get()`
    *   :meth:`degu.client.Connection.head()`
    *   :meth:`degu.client.Connection.delete()`

It's likewise fun and easy to create throw-away SSL certificate chains using
:class:`degu.misc.TempPKI`, and to create a throw-away
:class:`degu.misc.TempSSLServer` on which to run our ``ProxyApp``.   We'll
create a server that accepts connections on any IPv6 address (but only from
clients with a client certificate signed by the correct client certificate
authority):

>>> from degu.misc import TempPKI, TempSSLServer
>>> pki = TempPKI()
>>> proxy_app = ProxyApp(client)
>>> proxy_server = TempSSLServer(pki.server_sslconfig, ('::', 0, 0, 0), proxy_app)

That just spun-up a :class:`degu.server.SSLServer` in a new
`multiprocessing.Process`_ (which will be automatically terminated when the
:class:`degu.misc.TempSSLServer` is garbage collected).

We'll need a :class:`degu.client.SSLClient` so we can make connections to our
``proxy_server``:

>>> from degu.client import SSLClient
>>> proxy_client = SSLClient(pki.client_sslconfig, proxy_server.address)
>>> proxy_conn = proxy_client.connect()

And now we can use this connection to make the same ``PUT`` and ``POST``
requests to our ``example_app``, but this time through our ``ProxyApp``
reverse-proxy:

>>> proxy_conn.put('/foo', {}, None)
Response(status=200, reason='OK', headers={'x-msg': 'hello, world'}, body=None)
>>> proxy_conn.post('/bar', {}, None)
Response(status=200, reason='OK', headers={'x-msg': 'hello, world'}, body=None)

To round things out, here's how to make the same two requests using
:meth:`degu.client.Connection.request()`:

>>> proxy_conn.request('PUT', '/foo', {}, None)
Response(status=200, reason='OK', headers={'x-msg': 'hello, world'}, body=None)
>>> proxy_conn.request('POST', '/bar', {}, None)
Response(status=200, reason='OK', headers={'x-msg': 'hello, world'}, body=None)

Finally, we'll *shut it down*:

>>> proxy_conn.close()
>>> proxy_server.terminate()
>>> server.terminate()

This example is based on real-world Degu usage.  This is almost exactly how
`Dmedia`_ uses Degu as an SSL front-end for `CouchDB`_.



Example: HTTP over AF_UNIX
--------------------------

A highly differentiating feature of Degu is that both its server and client can
*transparently* do HTTP over ``AF_UNIX``.

When creating a server or client, the *address* argument itself conveys
everything needed in order to do HTTP over ``AF_INET``, ``AF_INET6``, or
``AF_UNIX``.  This way 3rd-party application software can pass around the single
*address* argument, all while remaining gleefully unaware of what the underlying
socket family will be.

For example, when creating a server, if your *address* is an ``str``, then it
must be the absolute, normalized path of a socket file that does *not* yet
exist:

>>> import tempfile
>>> from os import path
>>> tmpdir = tempfile.mkdtemp()
>>> address = path.join(tmpdir, 'my.socket')

We'll then spin-up a throw-away :class:`degu.server.Server` by creating a :class:`degu.misc.TempServer`:

>>> from degu.misc import TempServer
>>> server = TempServer(address, example_app)

Even though in this case the *address* we provide when creating a client will
match the *address* we provided when creating a server, note that this wont
always be true, depending on the exact *address* type and value.  You should
always create a client using the resulting :attr:`degu.server.Server.address`
attribute.

So as in our previous example, we'll create a :class:`degu.client.Client` like
this:

>>> from degu.client import Client
>>> client = Client(server.address)

And as in our previous example, we'll create a :class:`degu.client.Connection`,
and then make a few HTTP requests like this:

>>> conn = client.connect()
>>> conn.request('GET', '/', {}, None)
Response(status=200, reason='OK', headers={'x-msg': 'hello, world'}, body=None)
>>> conn.request('PUT', '/foo/bar', {'content-type': 'silly'}, None)
Response(status=200, reason='OK', headers={'x-msg': 'hello, world'}, body=None)

Finally, we'll *shut it down*:

>>> conn.close()
>>> server.terminate()
>>> import shutil
>>> shutil.rmtree(tmpdir)

The important point is that both the Degu server and client keep 3rd-party
applications highly abstracted from what the underlying socket family will be
for a given *address*, thereby backing up our claim that Degu can
*transparently* do HTTP over ``AF_UNIX``.

This is especially critical for `Novacut`_, which is built as a set of
network-transparent services, most of which will usually all be running on the
local host, but any of which could likewise be running on a remote host.


RGI Primer
----------

The :doc:`rgi` (RGI) is very much in the spirit of `WSGI`_ but does not attempt
to be compatible with `CGI`_, nor necessarily to be compatible with any existing
HTTP servers.

However, a central goal of the RGI specification is be server agnostic so that
one can write RGI server applications that can transparently run under both Degu
and future Python HTTP servers that might conform with the RGI specification.

An RGI request handler (aka an "RGI server application") must be a callable
object taking three arguments, for example:

>>> def app(session, request, api):
...     if request.method != 'GET':
...         return (405, 'Method Not Allowed', {}, None)
...     if request.path != ['example']:
...         return (404, 'Not Found', {}, None)
...     return (200, 'OK', {}, b'hello, world')
...

RGI request handlers must return a 4-tuple to convey their HTTP response::

    (status, reason, headers, body)

The RGI *session* argument contains per-connection information.  The same
*session* instance is passed to your RGI request handler for all requests
handled through a given connection.  Under Degu, the *session* argument will
always be an :class:`degu.server.Session` instance.

The RGI *request* argument contains per-request information.  A unique *request*
instance is passed to your RGI request handler for each request (regardless
whether the request was made through the same connection).  Under Degu, the
*request* argument will always be a :class:`degu.server.Request` instance.

The RGI *api* argument exposes the standard RGI application API.  In particular,
it exposes the standard RGI :ref:`io-abstractions`, a set of classes used to
construct HTTP request and response bodies.  The same *api* argument is passed
to your RGI request handler for all requests handled through all connections.
Under Degu, the *api* argument will always be the :data:`degu.base.api`
constant.

As RGI request handlers will deal most with the *request* argument, it will
be detailed here.

For example, say your received this HTTP request::

    GET /foo/bar HTTP/1.1\r\n
    Accept: application/json\r\n
    \r\n

Then the *request* argument will have the following attributes with the
following values::

    request.method  --> 'GET'
    request.uri     --> '/foo/bar'
    request.headers --> {'accept': 'application/json'}
    request.body    --> None
    request.mount   --> []
    request.path    --> ['foo', 'bar']
    request.query   --> None

Or for a second example, say your received this HTTP request::

    POST /foo?bar=baz HTTP/1.1\r\n
    Content-Length: 18\r\n
    Content-Type: application/json\r\n
    \r\n
    {"hello": "world"}

Then the *request* argument will have the following attributes with the
following values::

    request.method  --> 'POST'
    request.uri     --> '/foo?bar=baz'
    request.headers --> {'content-length': 18, 'content-type': 'application/json'}
    request.body    --> Body(<rfile>, 18)
    request.mount   --> []
    request.path    --> ['foo']
    request.query   --> 'bar=baz'

In which case the RGI request handler can read the incoming HTTP request body
like this::

    request.body.read() --> b'{"hello": "world"}'

A few things are worth noting about the *request* argument:

    1.  The ``request.uri`` attribute is a ``str`` containing the full,
        unparsed request URI.

    2.  The header names in the ``request.headers`` attribute are
        case-normalized to lowercase.

    3.  The ``request.body`` attribute will be ``None`` when the request does
        not contain an HTTP request body, it will be a
        :class:`degu.base.Body` instance when the request contains a
        ``'content-length'`` header, or it will be a
        :class:`degu.base.ChunkedBody` instance when the request contains a
        ``'transfer-encoding'`` header.

    4.  The ``request.mount`` attribute is a ``list`` that is semantically
        equivalent to the `WSGI`_ ``environ['SCRIPT_NAME']`` item; it contains
        the already handled portions of the request URI; in Degu, it will
        always be an empty list ``[]`` when your RGI root application receives
        a new request, as Degu only supports mounting the root application at
        ``'/'``.

    5.  The ``request.path`` attribute is a ``list`` that is semantically
        equivalent to the `WSGI`_ ``environ['PATH_INFO']`` item; it contains
        the yet-to-be handled portions of the request URI; as a request is
        routed through RGI middleware, components should be shifted from
        ``request.path`` to ``request.mount`` using the ``request.shift_path()``
        method (in Degu, the :meth:`degu.server.Request.shift_path()` method).

    6.  The ``request.query`` attribute will be ``None`` when the request URI
        does not contain a ``'?'``, or otherwise will be a ``str`` contain the
        query portion of of the request URI, which can be an empty ``''`` if
        the final character of the URI is ``'?'``.


For more information on the RGI request arguments, see the documentation for:

    *   :class:`degu.server.Session`

    *   :class:`degu.server.Request`

    *   :class:`degu.base.API`

    *   :data:`degu.base.api`



.. _io-abstractions:

IO abstractions
---------------

On both the server and client ends, Degu uses the same set of shared IO
abstractions to represent HTTP request and response bodies.

As the IO *directions* of the request and response are flipped depending on
whether you're looking at things from a server vs client perspective, it's
helpful to think in terms of HTTP *input* bodies and HTTP *output* bodies.

An **HTTP input body** will always be one of three types:

    * ``None`` --- meaning no HTTP input body

    * :class:`degu.base.Body` --- an HTTP input body with a content-length

    * :class:`degu.base.ChunkedBody` --- an HTTP input body that uses chunked
      transfer-encoding

From the server perspective, our input is the HTTP request body received from
the client, exposed via :attr:`degu.server.Request.body`.

From the client perspective, our input is the HTTP response body received from
the server, exposed via :attr:`degu.client.Response.body`.

When the HTTP input body is not ``None``, the receiving endpoint is responsible
for reading the entire input body, which must be completed before the another
request/response sequence can be initiated using that same connection.

An **HTTP output body** can be:

    ==================================  ========  ================
    Type                                Encoding  Source object
    ==================================  ========  ================
    ``None``                            *n/a*     *n/a*
    ``bytes``                           Length    *n/a*
    :class:`degu.base.Body`             Length    File-like object
    :class:`degu.base.BodyIter`         Length    An iterable
    :class:`degu.base.ChunkedBody`      Chunked   File-like object
    :class:`degu.base.ChunkedBodyIter`  Chunked   An iterable
    ==================================  ========  ================

From the server perspective, our output is the HTTP response body sent to the
client, specified via the fourth item in the response 4-tuple::

    (status, reason, headers, body)

From the client perspective, our output is the HTTP request body sent to the
server, specified via the fourth argument when calling
:meth:`degu.client.Connection.request()`:

>>> response = conn.request(method, uri, headers, body)  #doctest: +SKIP

Or specified via the third argument when calling
:meth:`degu.client.Connection.put()` or :meth:`degu.client.Connection.post()`:

>>> response = conn.put(uri, headers, body)  #doctest: +SKIP
>>> response = conn.post(uri, headers, body)  #doctest: +SKIP

The sending endpoint doesn't directly write the output, but instead only
*specifies* the output to be written, after which the Degu backend internally
handles the writing.



.. _eg-routing:

Example: RGI routing
--------------------

As a request is routed through RGI middleware to the RGI leaf application that
will generate the response, components should be shifted from
:attr:`degu.server.Request.path` to :attr:`degu.server.Request.mount`.

The :func:`degu.server.Request.shift_path()` method is the recommended way to do
this.

For example, say we have these two RGI leaf applications:

>>> def foo_app(session, request, api):
...     assert request.mount == ['foo']
...     if request.path != []:
...         return (404, 'Not Found Foo', {}, None)
...     return (200, 'OK', {}, b'FOO this')
... 
>>> def bar_app(session, request, api):
...     assert request.mount == ['bar']
...     if request.path != []:
...         return (404, 'Not Found Bar', {}, None)
...     return (200, 'OK', {}, b'BAR that')
... 

And this RGI middleware, which will be our root application:

>>> def root_app(session, request, api):
...     if request.method != 'GET':
...         return (405, 'Method Not Allowed', {}, None)
...     if request.path == []:
...         return (200, 'OK', {}, b'ROOT here')
...     next = request.shift_path()
...     if next == 'foo':
...         return foo_app(session, request, api)
...     if next == 'bar':
...         return bar_app(session, request, api)
...     return (404, 'Not Found', {}, None)
... 

As before, we'll run our application in a :class:`degu.misc.TempServer`:

>>> from degu.misc import TempServer
>>> server = TempServer(('127.0.0.1', 0), root_app)

And create a :class:`degu.client.Client` for making connections to the above
server:

>>> from degu.client import Client
>>> client = Client(server.address)

Now we'll create a :class:`degu.client.Connection`:

>>> conn = client.connect()

And use it to make some requests so we can see the RGI routing in action:

>>> conn.get('/', {}).body.read()
b'ROOT here'
>>> conn.get('/foo', {}).body.read()
b'FOO this'
>>> conn.get('/bar', {}).body.read()
b'BAR that'

But if we request a resource the server doesn't have:

>>> conn.get('/baz', {})
Response(status=404, reason='Not Found', headers={}, body=None)
>>> conn.get('/bar/baz', {})
Response(status=404, reason='Not Found Bar', headers={}, body=None)

(Make sure you understand why that final request also returned a ``404`` error.)

Finally, we'll *shut it down*:

>>> conn.close()
>>> server.terminate()



.. _eg-range-requests:

Example: range requests
-----------------------

When the Degu server receives a request with an HTTP Range header, its value is
exposed as a :class:`degu.base.Range` instance:

>>> from degu.misc import parse_headers
>>> parse_headers(b'Range: bytes=3-8')
{'range': Range(3, 9)}

This is similar to how the value of a Content-Length header is exposed as an
``int`` rather than a ``str``:

>>> parse_headers(b'Content-Length: 6')
{'content-length': 6}

:meth:`degu.client.Connection.get_range()` is the best way to make a Range
request as it will automatically add the ``'range'`` header for you.  But for
illustration, your client code could also manually set a ``'range'`` header
whose value is a :class:`degu.base.Range` instance:

>>> from degu.base import Range
>>> my_range = Range(3, 9)
>>> my_request_headers = {'range': my_range}

When an outgoing header value isn't already a ``str`` instance, its
``__str__()`` method is called to get the string representation that should be
used in the outgoing HTTP preamble.

For example, this is done to convert an outgoing Content-Length value from an
``int`` to a ``str``.

But :meth:`degu.base.Range.__str__()` has a bit more magic to it:

>>> repr(my_range)
'Range(3, 9)'
>>> str(my_range)
'bytes=3-8'

Note that :meth:`degu.base.Range.__str__()` automatically converts between
standard Python slice semantics and the rather odd semantics of the HTTP
Range header, which uses ``(stop - 1)`` to specify the "end" of a range:

>>> str(Range(0, 1))
'bytes=0-0'

When a Range header is parsed, the reverse conversion is done:

>>> parse_headers(b'Range: bytes=0-0')
{'range': Range(0, 1)}

When responding to a valid Range request, a server should include a
Content-Range in its response headers.

:class:`degu.base.ContentRange` provides the complement for the response
headers:

>>> from degu.base import ContentRange
>>> my_content_range = ContentRange(3, 9, 12)
>>> my_response_headers = {'content-range': my_content_range}

:meth:`degu.base.ContentRange.__str__()` likewise has a bit of magic:

>>> repr(my_content_range)
'ContentRange(3, 9, 12)'
>>> str(my_content_range)
'bytes 3-8/12'

As you might expect, when the Degu client receives a response with an HTTP
Content-Range header, its value is exposed as a :class:`degu.base.ContentRange`
instance:

>>> parse_headers(b'Content-Range: bytes 3-8/12', isresponse=True)
{'content-range': ContentRange(3, 9, 12)}

**Note on portability**

The goal of the RGI specification is to allow RGI server and client components
to transparently run under multiple RGI compatible implementations.

To be portable between implementations, RGI consumers should not directly import
:class:`degu.base.Range` or :class:`degu.base.ContentRange` from the
:mod:`degu.base` module.

Instead, RGI server applications should use the ``ContentRange`` attribute
exposed on the RGI *api* argument, for example::

    def my_app(session, request, api):
        my_content_range = api.ContentRange(3, 9, 12)

And RGI client applications should use the ``Range`` attribute exposed via :attr:`degu.client.Connection.api`, for example::

    conn = client.connect()
    my_range = conn.api.Range(3, 9)

Or ideally RGI client applications should use the
:meth:`degu.client.Connection.get_range()` method as there's really no reason to
use ``api.Range`` directly in production code.

**Live example!**

Let's put all this together in a live example.  First we'll define our server
application:

>>> def range_app(session, request, api):
...     if request.path != ['example']:
...         return (404, 'Not Found', {}, None)
...     if request.method not in {'GET', 'HEAD'}:
...         return (405, 'Method Not Allowed', {}, None)
...     body = b'hello, world'
...     if request.method == 'HEAD':
...         return (200, 'OK', {'content-length': len(body)}, None)
...     r = request.headers.get('range')
...     if r is None:
...         return (200, 'OK', {}, body)
...     if r.stop > len(body):
...         return (416, 'Requested Range Not Satisfiable', {}, None)
...     cr = api.ContentRange(r.start, r.stop, len(body))
...     return (206, 'Partial Content', {'content-range': cr}, body[r.start:r.stop])
...

Then we'll spin-up a throw-away server instance:

>>> from degu.misc import TempServer
>>> server = TempServer(('127.0.0.1', 0), range_app)

And create a client for making connections to the above server:

>>> from degu.client import Client
>>> client = Client(server.address)

Now we'll create a connection and make a Range request for the resource slice
``[3:9]`` with :meth:`degu.client.Connection.get_range()`:

>>> conn = client.connect()
>>> response = conn.get_range('/example', {}, 3, 9)

Note the response status and reason:

>>> response.status
206
>>> response.reason
'Partial Content'

And the response headers:

>>> sorted(response.headers)
['content-length', 'content-range']
>>> response.headers['content-length']
6
>>> response.headers['content-range']
ContentRange(3, 9, 12)

Let's read the response body, and compare it with a standard Python slice:

>>> response.body.read()
b'lo, wo'
>>> b'hello, world'[3:9]
b'lo, wo'

Of course, we can also request the entire resource with
:meth:`degu.client.Connection.get()`:

>>> conn.get('/example', {}).body.read()
b'hello, world'

Or make a ``HEAD`` request with :meth:`degu.client.Connection.head()`:

>>> conn.head('/example', {})
Response(status=200, reason='OK', headers={'content-length': 12}, body=None)

For a few more Range request examples, let's also request the first 5 bytes:

>>> conn.get_range('/example', {}, 0, 5).body.read()
b'hello'

And request the final 5 bytes:

>>> conn.get_range('/example', {}, 7, 12).body.read()
b'world'

But if we use a *stop* value that's greater than the total size of the resource:

>>> conn.get_range('/example', {}, 7, 13)
Response(status=416, reason='Requested Range Not Satisfiable', headers={}, body=None)

Finally, we'll *shut it down*:

>>> conn.close()
>>> server.terminate()



Example: chunked encoding
-------------------------

For our final example, we'll show how chunked transfer-encoding semantics are
fully exposed in Degu.

For good measure, we'll also toss in HTTP bodies with a content-length, just to
compare and contrast.

We'll also demonstrate how to use the :class:`degu.base.BodyIter` and
:class:`degu.base.ChunkedBodyIter` wrappers to generate your HTTP output body
piecewise and on-the-fly, both for the client-side request body and the
server-side response body.

First, we'll define two silly Python generator functions that generate the
server-side response body, one for chunked transfer-encoding and another for 
content-length encoding:

>>> def chunked_response_body(echo):
...     yield (None,                      echo)
...     yield (None,                      b' ')
...     yield (None,                      b'are')
...     yield (('key', 'value'),          b' ')
...     yield (None,                      b'belong')
...     yield (('chunk', 'extensions'),   b' ')
...     yield (None,                      b'to')
...     yield (('are', 'neat'),           b' ' )
...     yield (None,                      b'us')
...     yield (None,                      b'')
...
>>> def response_body(echo):
...     yield echo
...     yield b' '
...     yield b'are'
...     yield b' '
...     yield b'belong'
...     yield b' '
...     yield b'to'
...     yield b' '
...     yield b'us'
... 
>>> len(b''.join(response_body(b''))) == 17  # 17 used below
True

Second, we'll define an RGI server application that will return a response body using
chunked transfer encoding if we ``POST /chunked``, and that will return a body
with a content-length if we ``POST /length``:

>>> def rgi_io_app(session, request, api):
...     if request.path not in (['length'], ['chunked']):
...         return (404, 'Not Found', {}, None)
...     if request.method != 'POST':
...         return (405, 'Method Not Allowed', {}, None)
...     if request.body is None:
...         return (400, 'Bad Request', {}, None)
...     echo = request.body.read()  # Body/ChunkedBody agnostic
...     if request.path[0] == 'chunked':
...         body = api.ChunkedBodyIter(chunked_response_body(echo))
...     else:
...         body = api.BodyIter(response_body(echo), len(echo) + 17)
...     return (200, 'OK', {}, body)
... 

As usual, we'll start a throw-away server and create a client:

>>> server = TempServer(('127.0.0.1', 0), rgi_io_app)
>>> client = Client(server.address)

For now we'll just use a simple ``bytes`` instance for the client-side request
body.  For example, if we ``POST /chunked``:

>>> conn = client.connect()
>>> response = conn.request('POST', '/chunked', {}, b'All your base')

Notice that a :class:`degu.base.ChunkedBody` is returned:

>>> response.body.chunked
True
>>> response.body
ChunkedBody(<reader>)
>>> response.headers
{'transfer-encoding': 'chunked'}

We can easily iterate through the ``(extension, data)`` tuples for each chunk
in the response body like this:

>>> for (extension, data) in response.body:
...     print((extension, data))
...
(None, b'All your base')
(None, b' ')
(None, b'are')
(('key', 'value'), b' ')
(None, b'belong')
(('chunk', 'extensions'), b' ')
(None, b'to')
(('are', 'neat'), b' ')
(None, b'us')
(None, b'')

(Note that :meth:`degu.base.ChunkedBody.readchunk()` can also be used to
manually step through the chunks.)

:meth:`degu.base.ChunkedBody.read()` can be used to accumulate all the chunk
data into a single ``bytes`` instance, at the expense of loosing the exact chunk
data boundaries and any chunk extensions:

>>> response = conn.request('POST', '/chunked', {}, b'All your base')
>>> response.body.read()
b'All your base are belong to us'

API-wise, ``body.read()`` can always be used without worrying about the
transfer-encoding, but in real applications you should be very cautions about
this due to the possibility of unbounded memory usage with chunked
transfer-encoding.

But at least for illustration, note that :meth:`degu.base.ChunkedBody.read()`
is basically equivalent to :meth:`degu.base.Body.read()`.

For example, if we ``POST /length``:

>>> response = conn.request('POST', '/length', {}, b'All your base')

Notice that the response body is a :class:`degu.base.Body` instance:

>>> response.body.chunked
False
>>> response.body
Body(<reader>, 30)
>>> response.headers
{'content-length': 30}

And that we get the expected result from ``body.read()``:

>>> response.body.read()
b'All your base are belong to us'

For one last bit of fancy, you can likewise use an arbitrary iterable to
generate your client-side request body.

So let's define a third silly Python generator function to generate the 
client-side request body using chunked trasfer-encoding:

>>> def chunked_request_body():
...     yield (None,                     b'All')
...     yield (None,                     b' ')
...     yield (None,                     b'your')
...     yield (None,                     b' ')
...     yield (None,                     b'*something')
...     yield (('key', 'value'),         b' ')
...     yield (('chunk', 'extensions'),  b'else*')
...     yield (('are', 'neat'),          b'')
...

To use this generator as our request body, we need to wrap it in a
:class:`degu.base.ChunkedBodyIter`, like this:

>>> body = conn.api.ChunkedBodyIter(chunked_request_body())

And then if we ``POST /chunked``:

>>> response = conn.request('POST', '/chunked', {}, body)
>>> response.body.read()
b'All your *something else* are belong to us'

Or if we ``POST /length``:

>>> body = conn.api.ChunkedBodyIter(chunked_request_body())
>>> response = conn.request('POST', '/length', {}, body)
>>> response.body.read()
b'All your *something else* are belong to us'

Well, that's all the time we have today for fancy!

>>> conn.close()
>>> server.terminate()


.. _http-subset:

HTTP/1.1 subset
---------------

For simplicity, performance, and especially security, the Degu server and client
support only a rather idealized subset of `HTTP/1.1`_ features.

Although the Degu server and client *generally* operate in an HTTP/1.1
compliant fashion themselves, they do *not* support all valid HTTP/1.1 features
and permutations from the other endpoint.  However, the unsupported features are
seldom used by other modern HTTP/1.1 servers and clients, so these restrictions
don't particularly limit the servers and clients with which Degu can interact.

Also, remember that Degu is primarily aimed at highly specialized P2P usage
where Degu clients will only be talking to the Degu servers running on other
devices on the same local network.  Degu is also aimed at using HTTP as a
network-transparent RPC mechanism, including when communicating with servers
running on the same host using HTTP over ``AF_UNIX``.

In particular, Degu is restrictive when it comes to:

**HTTP protocol version:**

    * Degu currently only supports HTTP/1.1 clients and servers; although in the
      future Degu may support, say, the finalized HTTP/2.0 protocol, there is no
      plan for Degu ever to support HTTP/1.0 (or older) clients and servers

**HTTP headers:**

    * Although allowed by HTTP/1.1, Degu doesn't support multiple occurrences of
      the same header

    * Although allowed by HTTP/1.1, Degu doesn't support headers whose value
      spans multiple lines in the request or response preamble

    * Although allowed by HTTP/1.1, Degu doesn't allow both a Content-Length and
      a Transfer-Encoding header to be present in the same request or response
      preamble

    * Degu is less forgiving when it comes to white-space in the Header lines,
      which must always have the form::

        'Name: Value\r\n'

    * Although Degu accepts mixed case header names from the other endpoint, the
      Degu server and client always case-fold (lowercase) the header names prior
      to passing control to 3rd-party RGI server application software

    * Degu :doc:`rgi` server applications must only include case-folded header
      names in their response tuple, and likewise, 3rd-party application
      software must only include case-folded header names when calling
      :meth:`degu.client.Connection.request()`

    * The Degu server includes *zero* headers by default, although :doc:`rgi`
      server applications are free to include whatever headers they see fit in
      their response; of particular note, the Degu server doesn't by default
      include a ``'date'`` header

    * The Degu client includes *zero* headers by default, although 3rd-party
      applications are free to include whatever headers they see fit in their
      request; of particular note, the Degu client doesn't by default include a
      ``'host'`` header

    * A strait-forward way to minimize the overhead of the HTTP protocol is to
      simply send fewer request and response headers; both the Degu server and
      client aggressively peruse this optimization route, even at the expense of
      of operating in a strictly HTTP/1.1 compliant fashion (again, 3rd-party
      applications are free to include additional headers as needed)

**HTTP request method:**

    * Currently the Degu server and client only allow the request method to be
      ``'GET'``, ``'HEAD'``, ``'DELETE``, ``'PUT'``, or ``'POST'``; in
      particular this restriction is in place out of security consideration when
      the Degu is used as a reverse proxy to something like `CouchDB`_; if this
      is too restrictive for your application, please `file a bug`_ and we'll
      consider relaxing this somewhat

**HTTP request body:**

    * A request body is only allowed when the request method is ``'PUT'`` or
      ``'POST'``

    * A request body is *not* allowed when the request method is ``'GET'``,
      ``'HEAD'``, or ``'DELETE'``, and as such, neither a Content-Length nor a
      Transfer-Encoding header should be preset in such requests



.. _`gunicorn`: http://gunicorn.org/
.. _`modwsgi`: https://github.com/GrahamDumpleton/mod_wsgi
.. _`WSGI`: https://www.python.org/dev/peps/pep-3333/
.. _`CGI`: https://en.wikipedia.org/wiki/Common_Gateway_Interface
.. _`Python3`: https://docs.python.org/3/
.. _`Avahi`: http://avahi.org/
.. _`multiprocessing.Process`: https://docs.python.org/3/library/multiprocessing.html#the-process-class
.. _`http.client`: https://docs.python.org/3/library/http.client.html
.. _`Dmedia`: https://launchpad.net/dmedia
.. _`CouchDB`: https://couchdb.apache.org/
.. _`Apache 2.4`: https://httpd.apache.org/docs/2.4/
.. _`reverse-proxy`: https://en.wikipedia.org/wiki/Reverse_proxy
.. _`ssl.SSLContext`: https://docs.python.org/3/library/ssl.html#ssl-contexts
.. _`link-local addresses`: https://en.wikipedia.org/wiki/Link-local_address#IPv6
.. _`HTTP/1.1`: https://www.ietf.org/rfc/rfc2616.txt
.. _`file a bug`: https://bugs.launchpad.net/degu
.. _`Novacut`: https://launchpad.net/novacut


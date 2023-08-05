# Copyright (c) 2016 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from tornado import gen
import tornado.web
import tornado.httpserver
import tornado.netutil

from yarpc.errors import BadRequestError, UnexpectedError, ProcedureFailedError
from yarpc.transport import Inbound, Request
from yarpc.transport.validator import _Validator
from yarpc._future import fail_to, maybe_async
from . import headers


class HTTPInbound(Inbound):

    def __init__(self, port=None, reuse_port=False, handlers=None):
        self.port = port or 0
        self._reuse_port = reuse_port
        self._server = None
        self._handlers = handlers or []

    def start(self, handler):
        self._handlers.append(
            ('.*$', _TornadoHandler, dict(handler=handler)),
        )
        app = tornado.web.Application(handlers=self._handlers)
        self._server = tornado.httpserver.HTTPServer(app)

        # the following does the same as http_server.listen(self.port),
        # except with fine grain control over the sockopts
        sockets = tornado.netutil.bind_sockets(
            port=self.port,
            reuse_port=self._reuse_port,
        )
        self.port = sockets[0].getsockname()[1]
        self._server.add_sockets(sockets)

    def stop(self):
        if self._server is not None:
            self._server.stop()
            self._server = None

    @property
    def hostport(self):
        # TODO get pub ip???
        return 'localhost:%s' % self.port


class _TornadoHandler(tornado.web.RequestHandler):

    def initialize(self, handler):
        self._handler = handler

    def post(self):
        request = _to_request(self.request)

        if not self._validate(request):
            return

        answer = gen.Future()

        @fail_to(answer)
        def on_dispatch(future):
            if not future.exception():
                response = future.result()
                if response.headers:
                    hs = headers.to_http_headers(response.headers)
                    for k, v in hs.iteritems():
                        self.set_header(k, v)
                if response.body is not None:
                    self.write(response.body)
            else:
                self._handle_request_exception(future.exception(), request)

            answer.set_result(None)

        maybe_async(
            self._handler.handle, request
        ).add_done_callback(on_dispatch)

        return answer

    def _validate(self, request):
        v = _Validator(request)
        if request.ttl:
            v.parse_ttl(request.ttl)
        try:
            v.validate()
        except BadRequestError as e:
            m = 'BadRequest: %s\n' % str(e)
            self.write(m)
            self.set_status(400)
            return False
        return True

    def _handle_request_exception(self, e, request):
        if isinstance(e, BadRequestError):
            m = 'BadRequest: %s\n' % str(e)
            self.write(m)
            self.set_status(400)
            return

        if not isinstance(e, UnexpectedError):
            e = ProcedureFailedError(
                exception=e,
                service=request.service,
                procedure=request.procedure,
            )

        m = 'UnexpectedError: %s\n' % str(e)
        self.write(m)
        self.set_status(500)


def _to_request(http_request):
    http_headers = http_request.headers
    procedure = http_headers.pop(headers.PROCEDURE, None)
    caller = http_headers.pop(headers.CALLER, None)
    service = http_headers.pop(headers.SERVICE, None)
    ttl = http_headers.pop(headers.TTL, None)
    encoding = http_headers.pop(headers.ENCODING, None)  # optional

    request = Request(
        caller=caller,
        service=service,
        encoding=encoding,
        ttl=ttl,
        procedure=procedure,
        headers=headers.from_http_headers(http_headers),
        body=http_request.body,
    )

    return request

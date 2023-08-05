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
from tchannel import TChannel, Response
from tchannel.errors import (
    BadRequestError as TChBadRequestError,
    UnexpectedError as TChUnexpectedError,
)
from tchannel.sync import TChannel as TChannelSync

from yarpc.errors import (
    BadRequestError,
    UnexpectedError,
    ServerEncodingError,
    ProcedureFailedError,
)
from yarpc.transport import Inbound, Request
from yarpc.transport.validator import _Validator
from yarpc._future import fail_to, maybe_async
from . import headers


class TChannelInbound(Inbound):

    def __init__(self, tchannel):
        if isinstance(tchannel, TChannelSync):
            raise ValueError(
                "TChannelInbound must use a regular TChannel,"
                "do not use a TChannelSync"
            )
        self._tchannel = tchannel

    def start(self, handler):
        self._tchannel.register(TChannel.FALLBACK)(_TChannelHandler(handler))
        if not self._tchannel.is_listening():
            self._tchannel.listen()

    def stop(self):
        self._tchannel.close()

    @property
    def hostport(self):
        return self._tchannel.hostport

    @property
    def port(self):
        return int(self.hostport.rsplit(':', 1)[1])


class _TChannelHandler(object):

    def __init__(self, handler):
        self.handler = handler

    def __call__(self, tchan_request):
        request = _to_request(tchan_request)

        v = _Validator(request)
        try:
            v.validate()
        except BadRequestError as e:
            raise TChBadRequestError(
                'BadRequest: %s\n' % str(e)
            )

        answer = gen.Future()

        @fail_to(answer)
        def on_dispatch(future):
            if not future.exception():
                response = future.result()
                tchan_response = Response(
                    body=response.body,
                    headers=headers.encode(
                        request.encoding, response.headers),
                    transport=None,  # TODO transport?
                )
                answer.set_result(tchan_response)
                return

            _handle_request_exception(future.exception(), request)

        maybe_async(
            self.handler.handle, request
        ).add_done_callback(on_dispatch)

        return answer


def _handle_request_exception(e, request):
    if isinstance(e, BadRequestError):
        raise TChBadRequestError(
            'BadRequest: %s\n' % str(e)
        )

    if isinstance(e, ServerEncodingError):
        raise e

    if not isinstance(e, UnexpectedError):
        e = ProcedureFailedError(
            exception=e,
            service=request.service,
            procedure=request.procedure,
        )

    m = 'UnexpectedError: %s\n' % str(e)

    raise TChUnexpectedError(m)


def _to_request(tchan_request):
    scheme = tchan_request.transport.scheme

    request = Request(
        caller=tchan_request.transport.caller_name,
        service=tchan_request.service,
        encoding=scheme,
        ttl=tchan_request.timeout,  # in seconds
        procedure=tchan_request.endpoint,
        headers=headers.decode(scheme, tchan_request.headers),
        body=tchan_request.body,
    )

    return request

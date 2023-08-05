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

import socket
import time

from tchannel import TChannel
from tornado import gen

from yarpc import Response, Request
from yarpc.encoding import json
from yarpc.transport import Channel
from yarpc.transport.http import HTTPOutbound
from yarpc.transport.tchannel import TChannelOutbound

hostname = socket.gethostname()


@json.procedure('phone')
@gen.coroutine
def phone(request):
    start = time.time()

    # enforce request shape
    if (
        not request.body.get('transport') or
        not request.body.get('service') or
        not request.body.get('procedure')
    ):
        raise ValueError(
            'transport, service, and procedure are '
            'required request params'
        )

    # create outbound dynamically based on request
    t = request.body['transport']
    if 'http' in t:
        http = t['http']
        outbound = HTTPOutbound(
            url='http://%s:%d' % (http['host'], http['port']),
        )
    elif 'tchannel' in request.body['transport']:
        tch = t['tchannel']
        outbound = TChannelOutbound(
            tchannel=TChannel('yarpc-test'),
            hostport='%s:%d' % (tch['host'], tch['port']),
        )
    else:
        raise ValueError(
            "no transport available for: %s" %
            request.body['transport']
        )

    # create a client with a custom channel
    # based on the previously created outbound
    # TODO support arbitrary bytes and encodings
    client = json.JSONClient(Channel(
        caller='yarpc-test',
        service=request.body['service'],
        outbound=outbound,
    ))
    answer = yield client.call(Request(
        procedure=request.body['procedure'],
        body=request.body,
        ttl=10000,
    ))

    # respond with answer from downstream service
    response = Response(body={
        'service': request.body['service'],
        'procedure': request.body['procedure'],
        'hostname': hostname,
        'elapsedms': to_millis(time.time() - start),
        'body': answer.body,
    })

    raise gen.Return(response)


def to_millis(time):
    return int(round(time * 1000))

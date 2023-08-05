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

from os import path

from tornado import gen

import crossdock
from crossdock import rand, transport as tr
from yarpc import RPC, Request
from yarpc.encoding.thrift import load, ThriftClient

idl = path.join(path.dirname(crossdock.__file__), 'Echo.thrift')
service = load(idl)


@gen.coroutine
def thrift(respw, server, transport, **kwargs):
    rpc = RPC(
        service='client',
        outbounds={
            'yarpc-test': tr.factory(server, transport),
        },
    )

    expected = rand.string(7)

    request = Request(
        body=service.Echo.echo(service.Ping(beep=expected)),
        ttl=10000,
    )
    client = ThriftClient(rpc.channel('yarpc-test'))
    response = yield client.call(request)

    if response.body.boop == expected:
        respw.success("Server said: %s" % response.body.boop)
    else:
        respw.fail("expected %s, got %s" % (expected, response.body))

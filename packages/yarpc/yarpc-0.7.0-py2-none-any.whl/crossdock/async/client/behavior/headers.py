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
from yarpc.encoding.raw import RawClient
from yarpc.encoding.json import JSONClient
from yarpc.encoding.thrift import load, ThriftClient

idl = path.join(path.dirname(crossdock.__file__), 'Echo.thrift')
service = load(idl)

token1 = rand.string(10)
token2 = rand.string(10)

# tuples of (desc, give, want)
tests = [
    (
        'valid headers',
        {'token1': token1, 'token2': token2},
        {'token1': token1, 'token2': token2},
    ),
    (
        'non-string values',
        {'token': 42},
        {'token': '42'},
    ),
    (
        'empty strings',
        {'token': ''},
        {'token': ''},
    ),
    (
        'no headers',
        None,
        {},
    ),
    (
        'empty map',
        {},
        {},
    ),
    (
        'varying casing',
        {'ToKeN1': token1, 'tOkEn2': token2},
        {'token1': token1, 'token2': token2},
    ),
    (
        'http header conflict',
        {'Rpc-Procedure': 'does not exist'},
        {'rpc-procedure': 'does not exist'},
    ),
    (
        'mixed case value',
        {'token': 'MIXED case Value'},
        {'token': 'MIXED case Value'},
    ),
]


@gen.coroutine
def headers(respw, server, transport, encoding, **kwargs):
    rpc = RPC(
        service='client',
        outbounds={
            'yarpc-test': tr.factory(server, transport),
        },
    )
    caller = get_caller(encoding, rpc.channel('yarpc-test'))

    for test in tests:
        desc, give, want = test
        try:
            resp = yield caller.call(give)
        except Exception as e:
            respw.fail('%s: call failed, %s' % (desc, str(e)))
        else:
            got = resp.headers
            if want != got:
                respw.fail(
                    '%s: call failed, got %s, want %s' % (desc, got, want)
                )
            else:
                respw.success('%s: returns valid headers' % desc)


def get_caller(encoding, channel):
    if encoding == 'raw':
        return RawCaller(channel)
    elif encoding == 'json':
        return JSONCaller(channel)
    elif encoding == 'thrift':
        return ThriftCaller(channel)
    else:
        raise ValueError('encoding must be either raw, json, or thrift')


class RawCaller(object):

    def __init__(self, channel):
        self._client = RawClient(channel)

    def call(self, headers):
        request = Request(
            procedure='echo/raw',
            ttl=10000,
            headers=headers,
        )
        return self._client.call(request)


class JSONCaller(object):

    def __init__(self, channel):
        self._client = JSONClient(channel)

    def call(self, headers):
        request = Request(
            procedure='echo',
            ttl=10000,
            headers=headers,
        )
        return self._client.call(request)


class ThriftCaller(object):

    def __init__(self, channel):
        self._client = ThriftClient(channel)

    def call(self, headers):
        request = Request(
            body=service.Echo.echo(service.Ping(beep='boop')),
            ttl=10000,
            headers=headers,
        )
        return self._client.call(request)

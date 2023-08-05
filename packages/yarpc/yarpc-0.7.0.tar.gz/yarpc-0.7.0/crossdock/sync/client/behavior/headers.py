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

from yarpc.sync import RPC

from crossdock import transport as tr
from crossdock.async.client.behavior.headers import (
    tests, get_caller
)


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
            resp = caller.call(give).result()
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

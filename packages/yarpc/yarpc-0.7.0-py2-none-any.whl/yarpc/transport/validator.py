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

from yarpc.errors import MissingParametersError, InvalidTTLError


class _Validator(object):
    def __init__(self, request):
        self._request = request
        self._error = None

    def parse_ttl(self, ttl):
        if ttl == '':
            self._request.ttl = 0
            return
        try:
            self._request.ttl = int(ttl)
        except (TypeError, ValueError):
            self._error = InvalidTTLError(
                service=self._request.service,
                procedure=self._request.procedure,
                ttl=ttl,
            )

    def validate(self):
        # already failed
        if self._error:
            raise self._error

        # check missing params
        missing = []
        if not self._request.service:
            missing.append('service name')
        if not self._request.procedure:
            missing.append('procedure')
        if not self._request.caller:
            missing.append('caller name')
        if not self._request.ttl:
            missing.append('TTL')
        if not self._request.encoding:
            missing.append('encoding')
        if missing:
            raise MissingParametersError(missing)

        # negative TTLs are invalid
        if self._request.ttl < 0:
            raise InvalidTTLError(
                service=self._request.service,
                procedure=self._request.procedure,
                ttl=self._request.ttl,
            )

        return self._request

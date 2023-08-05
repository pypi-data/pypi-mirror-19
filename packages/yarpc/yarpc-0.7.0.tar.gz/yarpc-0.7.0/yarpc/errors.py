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


class YARPCError(Exception):
    pass


class OneWayNotSupportedError(YARPCError):
    pass


class ValueExpectedError(YARPCError):
    pass


class NoOutboundForServiceError(YARPCError):
    pass


class UnexpectedError(YARPCError):
    pass


class BadRequestError(YARPCError):
    pass


class ProcedureFailedError(UnexpectedError):

    def __init__(self, exception, service, procedure):
        message = (
            'error for procedure "%s" of service "%s": %s' %
            (procedure, service, str(exception))
        )
        super(ProcedureFailedError, self).__init__(message)


class UnrecognizedProcedureError(BadRequestError):

    def __init__(self, procedure, service):
        message = (
            'unrecognized procedure "%s" for service "%s"'
            % (procedure, service)
        )
        super(UnrecognizedProcedureError, self).__init__(message)


class MissingParametersError(BadRequestError):

    def __init__(self, params):
        message = self._construct_message(params)
        super(MissingParametersError, self).__init__(message)

    @staticmethod
    def _construct_message(params):
        message = 'missing '
        if len(params) == 1:
            message += params[0]
            return message

        if len(params) == 2:
            message += '%s and %s' % (params[0], params[1])
            return message

        message += ', '.join(params[:-1])
        message += ', and %s' % params[-1]
        return message


class InvalidTTLError(BadRequestError):

    def __init__(self, service, procedure, ttl):
        message = (
            'invalid TTL "%s" for procedure "%s" of service "%s": '
            'must be positive integer' % (ttl, procedure, service)
        )
        super(InvalidTTLError, self).__init__(message)


class ServerDecodingError(BadRequestError):

    def __init__(self, exception, encoding, service, procedure, caller):
        message = (
            'failed to decode "%s" request body for procedure "%s" of '
            'service "%s" from caller "%s": %s' %
            (encoding, procedure, service, caller, str(exception))
        )
        super(ServerDecodingError, self).__init__(message)


class ServerEncodingError(UnexpectedError):

    def __init__(self, exception, encoding, service, procedure, caller):
        message = (
            'failed to encode "%s" response body for procedure "%s" '
            'of service "%s" from caller "%s": %s' %
            (encoding, procedure, service, caller, str(exception))
        )
        super(ServerEncodingError, self).__init__(message)


class EncodingMismatchError(BadRequestError):

    def __init__(self, want, got):
        message = 'expected encoding "%s" but got "%s"' % (want, got)
        super(EncodingMismatchError, self).__init__(message)

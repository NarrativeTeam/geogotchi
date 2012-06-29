# Copyright (c) 2012 Memoto AB
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class GeogotchiError(Exception): pass
class GeonamesError(GeogotchiError): pass
class AuthorizationException(GeonamesError): pass
class RecordDoesNotExist(GeonamesError): pass
class OtherError(GeonamesError): pass
class DatabaseTimeout(GeonamesError): pass
class InvalidParameter(GeonamesError): pass
class NoResultFound(GeonamesError): pass
class DuplicateException(GeonamesError): pass
class PostalCodeNotFound(GeonamesError): pass
class DailyLimitOfCreditsExceeded(GeonamesError): pass
class HourlyLimitOfCreditsExceeded(GeonamesError): pass
class WeeklyLimitOfCreditsExceeded(GeonamesError): pass
class InvalidInput(GeonamesError): pass
class ServerOverloadedException(GeonamesError): pass
class ServiceNotImplemented(GeonamesError): pass

_geonames_error_order = [AuthorizationException, RecordDoesNotExist, OtherError, 
                         DatabaseTimeout, InvalidParameter, NoResultFound, 
                         DuplicateException, PostalCodeNotFound, 
                         DailyLimitOfCreditsExceeded, 
                         HourlyLimitOfCreditsExceeded, 
                         WeeklyLimitOfCreditsExceeded, InvalidInput, 
                         ServerOverloadedException, ServiceNotImplemented]

def from_code(code):
    """Get exception class from a geonames.org error code.
    """
    if not (10 <= code <= 23):
        raise GeogotchiError("invalid code: %s" % code)
    return _geonames_error_order[code - 10]


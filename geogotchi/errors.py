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


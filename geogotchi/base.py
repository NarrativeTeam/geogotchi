import functools
import math
import json

import requests

from geogotchi.constants import BASE_URL
from geogotchi.constants import DEFAULT_USERNAME
from geogotchi import errors


def _latlon_params(latlon):
    return {"lat": latlon[0], "lng": latlon[1]}


def _geoname_id(geoname):
    try:
        geoname_id = geoname["geonameId"]
    except TypeError:
        geoname_id = geoname
    return int(geoname_id)


def _convert(convert_func, geonames, keys):
    """Convert values in a list of geonames.

    :param convert_func: Function to run on key values.
    :param geonames: Parsed list of geonames returned from the API.
    :param keys: List of keys that should be converted, if they exist
                 in a geoname.
    :returns: The same list of geonames, with values converted.
    """
    for geoname in geonames:
        for key in keys:
            if key in geoname:
                geoname[key] = convert_func(geoname[key])
    return geonames

_convert_float = functools.partial(_convert, float)


def _make_utf8(s):
    if isinstance(s, unicode):
        return s.encode("utf-8")
    return s


def _norm(V):
    L = math.sqrt(sum([x**2 for x in V]))
    if L == 0:
        max_val = float(max(map(abs, V)))
        if max_val == 0.0:
            return [0.0 for x in V]
        return [x/max_val for x in V]
    return [x/L for x in V]


class Geogotchi(object):

    def __init__(self, username=DEFAULT_USERNAME):
        self._username = username
        self._base_params = {
                "username": self._username,
                }

    def find_nearby_place(self, latlon, **kwargs):
        """Find nearby populated place (reverse geocoding).

        Does a "findNearbyPlaceNameJSON" API call behind the scenes.

        :param latlon: A latitude/longitude two-tuple.
        :param radius: Radius in km.
        :param max_rows: Max number of rows.
        :param style: Verbosity (SHORT, MEDIUM, LONG or FULL).
        """
        return self._find_nearby("findNearbyPlaceNameJSON", latlon, **kwargs)

    def find_nearby_toponym(self, latlon, **kwargs):
        """Find nearby toponym (reverse geocoding).

        Does a "findNearbyJSON" API call behind the scenes.

        :param latlon: A latitude/longitude two-tuple.
        :param radius: Radius in km.
        :param max_rows: Max number of rows.
        :param style: Verbosity (SHORT, MEDIUM, LONG or FULL).
        """
        return self._find_nearby("findNearbyJSON", latlon, **kwargs)

    def find_nearby_wikipedia(self, latlon, rank_weight=1.0, 
                              distance_weight=1.0, **kwargs):
        """Find nearby Wikipedia entries (reverse geocoding).

        Does a "findNearbyWikipediaJSON" API call behind the scenes. Results
        are sorted in descending order.

        :param latlon: A latitude/longitude two-tuple.
        :param radius: Radius in km.
        :param max_rows: Max number of rows.
        :param rank_weight: Weight of rank in sorting.
        :param distance_weight: Weight of distance in sorting.
        :param lang: Language code.
        """
        nearby = self._find_nearby("findNearbyWikipediaJSON", latlon, **kwargs)
        ranks = _norm([entry["rank"] for entry in nearby])
        dists = _norm([entry["distance"] for entry in nearby])
        indexed = list(enumerate(nearby))
        def score(x):
            rank_score = rank_weight * ranks[x[0]]
            dist_score = distance_weight * (1.0 - dists[x[0]])
            return rank_score + dist_score
        indexed.sort(key=score)
        indexed.reverse()
        return [x[1] for x in indexed]

    def _find_nearby(self, path, latlon, **kwargs):
        # Used by findNearby* API calls.
        params = self._base_params.copy()
        params.update(_latlon_params(latlon))

        radius = kwargs.pop("radius", None)
        if radius is not None:
            params["radius"] = radius

        max_rows = kwargs.pop("max_rows", None)
        if max_rows is not None:
            params["maxRows"] = max_rows

        lang = kwargs.pop("lang", None)
        if lang is not None:
            params["lang"] = lang

        params["style"] = kwargs.pop("style", "SHORT")
        url = BASE_URL + path
        response = requests.get(url, params=params)
        parsed_response = self._parse_response(response)
        return _convert_float(parsed_response["geonames"], ["distance"])

    def _parse_response(self, response):
        """Parse response. Returns a Python structure or raises an exception.
        """
        status_code = response.status_code
        if status_code != 200:
            raise errors.GeogotchiError("status code: %s" % status_code)
        parsed_response = json.loads(response.text) 
        self._maybe_raise_geoname_error(parsed_response)
        return parsed_response

    def _maybe_raise_geoname_error(self, parsed_response):
        """Raises an exception if the parsed response looks like an error.

        GeoName does not use HTTP status codes properly.
        """
        try:
            status = parsed_response["status"]
            error_code = status["value"]
            message = status.get("message", "no message")
        except TypeError:
            pass 
        except KeyError:
            pass
        else:
            error_class = errors.from_code(error_code)
            raise error_class(message)

    def get_hierarchy(self, geoname):
        """Returns all GeoNames higher up in the hierarchy of a place name. 

        :param geoname: A dict with a "geonameId" key or an integer.
        """
        params = self._base_params.copy()
        params["geonameId"] = _geoname_id(geoname)

        url = BASE_URL + "hierarchyJSON"
        response = requests.get(url, params=params)
        parsed_response = self._parse_response(response)
        return parsed_response["geonames"]

    def search(self, **kwargs):
        """Perform a search.

        One of `q`, `name` and `name_equals` must be given. Non-unicode string
        arguments are assumed to be UTF-8 encoded.

        :param q: Query over all attributes of a place.
        :param name: Query place name only.
        :param name_equals: Query exact place name.
        :param max_rows: Max number of rows.
        :param start_row: Used for paging results. If you want to get
                          results 30 to 40, use ``start_row=30`` and
                          ``max_rows=10``.
        :param country: ISO-3166 country code. 
        :param country_bias: Records from the country bias are listed first.
        :param continent_code: Restricts the search for a toponym of the
                               given continent (AF, AS, EU, NA, OC, SA, AN).
        :param feature_class: `GeoNames feature class 
                               <http://www.geonames.org/export/codes.html>`_
        :param feature_code: `GeoNames feature code 
                               <http://www.geonames.org/export/codes.html>`_
        :param lang: ISO-636 2-letter language code (en, de, fr, se...)
        :param style: Verbosity (SHORT, MEDIUM, LONG, FULL)
        :param operator: AND (default) or OR.
        :param fuzzy: Defines the fuzzyness of the search terms. Float between
                      0.0 and 1.0 (default 1.0).
        """
        params = self._base_params.copy()
        for kwarg_name, query_name, default, conv in [
                ("q", "q", None, _make_utf8),
                ("name", "name", None, _make_utf8),
                ("name_equals", "name_equals", None, _make_utf8),
                ("max_rows", "maxRows", None, int),
                ("start_row", "startRow", None, int),
                ("country", "country", None, _make_utf8),
                ("country_bias", "countryBias", None, _make_utf8),
                ("continent_code", "continentCode", None, _make_utf8),
                ("feature_class", "featureClass", None, _make_utf8),
                ("feature_code", "featureCode", None, _make_utf8),
                ("lang", "lang", None, _make_utf8),
                ("style", "style", "SHORT", _make_utf8),
                ("operator", "operator", "AND", _make_utf8),
                ("fuzzy", "fuzzy", 1.0, float),
                ]:
            kwarg_val = kwargs.get(kwarg_name, default)
            if kwarg_val is not None:
                params[query_name] = conv(kwarg_val)
        url = BASE_URL + "searchJSON"
        response = requests.get(url, params=params)
        parsed_response = self._parse_response(response)
        return parsed_response["geonames"]

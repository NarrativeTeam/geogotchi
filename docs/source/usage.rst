.. usage

Usage
=====

    >>> from geogotchi import Geogotchi
    >>> lkpg = (58.411, 15.622)
    >>> gg = Geogotchi(username="demo")

Find Nearby Toponyms
--------------------

    >>> gg.find_nearby_toponym(lkpg, radius=5, max_rows=3)
    [{u'countryCode': u'SE',
      u'distance': 0.02928,
      u'fcl': u'P',
      u'fcode': u'PPLA',
      u'geonameId': 2694762,
      u'lat': 58.4108622585562,
      u'lng': 15.62157154083252,
      u'name': u'Link\xf6ping',
      u'toponymName': u'Link\xf6ping'},
     ...]

Find Nearby Wikipedia Articles
-------------------------------

Sorted by article rank and distance::

    >>> gg.find_nearby_wikipedia(lkpg, radius=5, max_rows=3)
    [{u'countryCode': u'SE',
      u'distance': 0.0401,
      u'elevation': 58,
      u'feature': u'city',
      u'lang': u'en',
      u'lat': 58.41083333333333,
      u'lng': 15.62138888888889,
      u'rank': 100,
      u'summary': u'Link\xf6ping is a city in southern middle Sweden, with 104 232 inhabitants in 2010. It is the seat of Link\xf6ping Municipality with 146 736 inhabitants (2011) and the capital of \xd6sterg\xf6tland County. Link\xf6ping is also the episcopal see of the Diocese of Link\xf6ping (Church of Sweden) and is well known for (...)',
      u'thumbnailImg': u'http://www.geonames.org/img/wikipedia/90000/thumb-89377-100.jpg',
      u'title': u'Link\xf6ping',
      u'wikipediaUrl': u'en.wikipedia.org/wiki/Link%C3%B6ping'},
     ...]

Sorted only by article rank (number of links pointing to it)::

    >>> gg.find_nearby_wikipedia(lkpg, radius=5, max_rows=3, rank_weight=1, distance_weight=0)
    [{u'countryCode': u'SE',
      u'distance': 0.0401,
      u'elevation': 58,
      u'feature': u'city',
      u'lang': u'en',
      u'lat': 58.41083333333333,
      u'lng': 15.62138888888889,
      u'rank': 100,
      u'summary': u'Link\xf6ping is a city in southern middle Sweden, with 104 232 inhabitants in 2010. It is the seat of Link\xf6ping Municipality with 146 736 inhabitants (2011) and the capital of \xd6sterg\xf6tland County. Link\xf6ping is also the episcopal see of the Diocese of Link\xf6ping (Church of Sweden) and is well known for (...)',
      u'thumbnailImg': u'http://www.geonames.org/img/wikipedia/90000/thumb-89377-100.jpg',
      u'title': u'Link\xf6ping',
      u'wikipediaUrl': u'en.wikipedia.org/wiki/Link%C3%B6ping'},
     ...]

Hierarchies
-----------

Get all GeoNames higher up in the hierarchy of a place name::

    >>> nearby = gg.find_nearby_place(lkpg)
    >>> gg.get_hierarchy(nearby[0])
    [{u'adminName1': u'',
      u'countryName': u'',
      u'fcl': u'L',
      u'fclName': u'parks,area, ...',
      u'fcode': u'AREA',
      u'fcodeName': u'area',
      u'geonameId': 6295630,
      u'lat': 0,
      u'lng': 0,
      u'name': u'Earth',
      u'population': 6814400000,
      u'toponymName': u'Earth'},
     ...]

Text Search
-----------

Search for hotels in Sundsvall, Sweden::

    >>> gg.search(q="sundsvall", feature_code="HTL")
    [{u'countryCode': u'SE',
      u'fcl': u'S',
      u'fcode': u'HTL',
      u'geonameId': 6495350,
      u'lat': 62.414,
      u'lng': 17.349,
      u'name': u'Scandic Sundsvall North',
      u'toponymName': u'Scandic Sundsvall North'},
     ...]

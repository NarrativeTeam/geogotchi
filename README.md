# Geogotchi

Library for working with [GeoNames][geonames] services.

## Usage

```python
>>> from pprint import pprint
>>> from geogotchi import Geogotchi
>>> 
>>> lkpg = (58.411, 15.622)
>>> gg = Geogotchi(username="demo")
```

Find nearby toponyms:

```python
>>> pprint(gg.find_nearby_toponym(lkpg, radius=5, max_rows=3))
[{u'countryCode': u'SE',
  u'distance': u'0.02928',
  u'fcl': u'P',
  u'fcode': u'PPLA',
  u'geonameId': 2694762,
  u'lat': 58.4108622585562,
  u'lng': 15.62157154083252,
  u'name': u'Link\xf6ping',
  u'toponymName': u'Link\xf6ping'},
 {u'countryCode': u'SE',
  u'distance': u'0.0643',
  u'fcl': u'S',
  u'fcode': u'THTR',
  u'geonameId': 8199320,
  u'lat': 58.41153384530707,
  u'lng': 15.622424483299255,
  u'name': u'Sagateatern',
  u'toponymName': u'Sagateatern'},
 {u'countryCode': u'SE',
  u'distance': u'0.17547',
  u'fcl': u'S',
  u'fcode': u'CH',
  u'geonameId': 8128618,
  u'lat': 58.41139053707475,
  u'lng': 15.624918937683105,
  u'name': u'S:t Lars kyrka',
  u'toponymName': u'S:t Lars kyrka'}]
```

Find nearby Wikipedia articles, sorted by article rank and distance:

```python
>>> pprint(gg.find_nearby_wikipedia(lkpg, radius=5, max_rows=3))
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
 {u'distance': 0.0194,
  u'elevation': 57,
  u'lang': u'en',
  u'lat': 58.411,
  u'lng': 15.622333333333334,
  u'rank': 74,
  u'summary': u'Downtown Link\xf6ping, the Inner City, is the district that includes the center of the city of Link\xf6ping. Located here is the commercial and cultural center of the city, with shops, restaurants, bars, shopping mall, museums, churches, libraries, sports facilities, and parks (...)',
  u'title': u'Downtown Link\xf6ping',
  u'wikipediaUrl': u'en.wikipedia.org/wiki/Downtown_Link%C3%B6ping'},
 {u'countryCode': u'SE',
  u'distance': 0.3766,
  u'elevation': 56,
  u'lang': u'en',
  u'lat': 58.408,
  u'lng': 15.625,
  u'rank': 97,
  u'summary': u'Link\xf6ping Municipality (Link\xf6pings kommun) is a municipality in \xd6sterg\xf6tland County in southern Sweden. Its administrative center is the city of Link\xf6ping, with some 94,000 inhabitants. The municipality is bordered in the west by Motala, and thence clockwise by Finsp\xe5ng, Norrk\xf6ping, \xc5tvidaberg, (...)',
  u'title': u'Link\xf6ping Municipality',
  u'wikipediaUrl': u'en.wikipedia.org/wiki/Link%C3%B6ping_Municipality'}]
```

Nearby Wikipedia articles, sorted only by article rank (number of links pointing
to it):

```python
>>> pprint(gg.find_nearby_wikipedia(lkpg, radius=5, max_rows=3, rank_weight=1, distance_weight=0))
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
 {u'countryCode': u'SE',
  u'distance': 0.3766,
  u'elevation': 56,
  u'lang': u'en',
  u'lat': 58.408,
  u'lng': 15.625,
  u'rank': 97,
  u'summary': u'Link\xf6ping Municipality (Link\xf6pings kommun) is a municipality in \xd6sterg\xf6tland County in southern Sweden. Its administrative center is the city of Link\xf6ping, with some 94,000 inhabitants. The municipality is bordered in the west by Motala, and thence clockwise by Finsp\xe5ng, Norrk\xf6ping, \xc5tvidaberg, (...)',
  u'title': u'Link\xf6ping Municipality',
  u'wikipediaUrl': u'en.wikipedia.org/wiki/Link%C3%B6ping_Municipality'},
 {u'distance': 0.0194,
  u'elevation': 57,
  u'lang': u'en',
  u'lat': 58.411,
  u'lng': 15.622333333333334,
  u'rank': 74,
  u'summary': u'Downtown Link\xf6ping, the Inner City, is the district that includes the center of the city of Link\xf6ping. Located here is the commercial and cultural center of the city, with shops, restaurants, bars, shopping mall, museums, churches, libraries, sports facilities, and parks (...)',
  u'title': u'Downtown Link\xf6ping',
  u'wikipediaUrl': u'en.wikipedia.org/wiki/Downtown_Link%C3%B6ping'}]
```

[geonames]: http://www.geonames.org/

# coding=utf-8

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

import os
import unittest
import uuid
from operator import itemgetter

from geogotchi import Geogotchi
from geogotchi import errors
from geogotchi.constants import DEFAULT_USERNAME
import geogotchi.base

latlons = {
        "sthlm": (59.333, 18.065),
        "gbg": (57.707, 11.967),
        "malmo": (55.606, 13.001),
        "uppsala": (59.859, 17.645),
        "lkpg": (58.411, 15.622),
        }
username = os.environ.get("GEOGOTCHI_USERNAME", DEFAULT_USERNAME)
gg = Geogotchi(username=username)

def get_random_string():
    return uuid.uuid4().hex


class TestGeogotchi(unittest.TestCase):

    def test_invalid_username(self):
        sthlm = latlons["sthlm"]
        gg_invalid = Geogotchi(username=get_random_string())
        self.assertRaises(errors.AuthorizationException,
                          gg_invalid.find_nearby_toponym, sthlm)

    def test_find_nearby_place(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_place(sthlm)
        names = [n["name"] for n in nearby]
        self.assertTrue("Stockholm" in names)

    def test_find_nearby_toponym(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_toponym(sthlm)
        names = [n["name"] for n in nearby]
        self.assertTrue("Stockholm" in names)

    def test_find_nearby_wikipedia_default(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_wikipedia(sthlm)

    def test_validate_weight(self):
        self.assertTrue(geogotchi.base._valid_weight(0.0))
        self.assertTrue(geogotchi.base._valid_weight(1.0))
        self.assertFalse(geogotchi.base._valid_weight(-0.1))
        self.assertFalse(geogotchi.base._valid_weight(1.1))
        self.assertFalse(geogotchi.base._valid_weight(0))
        self.assertFalse(geogotchi.base._valid_weight(1))
        self.assertFalse(geogotchi.base._valid_weight("foo"))

    def test_find_nearby_wikipedia_sort_distance(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_wikipedia(sthlm, rank_weight=0)
        min_dist = min(n["distance"] for n in nearby)
        self.assertEqual(nearby[0]["distance"], min_dist)
        max_dist = max(n["distance"] for n in nearby)
        self.assertEqual(nearby[-1]["distance"], max_dist)

    def test_find_nearby_wikipedia_sort_rank(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_wikipedia(sthlm, distance_weight=0)
        max_rank = max(n["rank"] for n in nearby)
        self.assertEqual(nearby[0]["rank"], max_rank)
        min_rank = min(n["rank"] for n in nearby)
        self.assertEqual(nearby[-1]["rank"], min_rank)

    def test_find_nearby_toponym_with_radius_and_max_rows(self):
        sthlm = latlons["sthlm"]
        max_rows = 3
        nearby = gg.find_nearby_toponym(sthlm, radius=5, max_rows=max_rows)
        self.assertEqual(max_rows, len(nearby))

    def test_get_hierarchy(self):
        lkpg = latlons["lkpg"]
        geoname = gg.find_nearby_place(lkpg)[0]
        hierarchy = gg.get_hierarchy(geoname)
        self.assertEqual(hierarchy[0]["name"], u"Earth")
        self.assertEqual(hierarchy[-1]["name"], u"Link\xf6ping")

    def test_get_hierarchy_by_id(self):
        stlars = 8128618
        hierarchy = gg.get_hierarchy(stlars)
        self.assertEqual(hierarchy[0]["name"], u"Earth")
        self.assertEqual(hierarchy[-1]["name"], u"S:t Lars kyrka")

    def test_get_hierarchy_bad(self):
        bad_geoname = 1234123412341234
        self.assertRaises(errors.OtherError, gg.get_hierarchy, bad_geoname)

    def test_search_basic(self):
        name = itemgetter("name")
        def check_name(cmp_name, **kwargs):
            self.assertEqual(cmp_name, 
                             name(gg.search(max_rows=1, **kwargs)[0]))

        check_name(u"Sweden", q="Sweden")
        check_name(u"Sverige", q="Sweden", lang="sv")
        check_name(u"Arlanda", name="Arlanda", feature_code="AIRP")

    def test_search_hotel(self):
        hotels = gg.search(q="sundsvall", feature_code="HTL")
        names = [h["name"] for h in hotels]
        should_exist = [u"Elite Hotel Knaust", u"First Hotel Strand"]
        existing = [n for n in names if n in should_exist]
        self.assertTrue(existing)

#
# gPrime - A web-based genealogy program
#
# Copyright (C) 2016  Gramps Development Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import unittest
import os

from gprime.test.test_util import Gramps
from gprime.db import open_database
from gprime.lib import *
from gprime.const import DATA_DIR

TEST_DIR = os.path.abspath(os.path.join(DATA_DIR, "tests"))
example = os.path.join(TEST_DIR, "data.gramps")

class DBAPI:
    NAME = "Example DBAPI Test"
    backend = "dbapi"

    def __init__(self):
        self.gramps = Gramps()
        self.call("--config=database.backend:" + self.backend,
                  "-C", self.NAME, "--import", example)
        self.db = open_database(self.NAME, force_unlock=True)

    def call(self, *args, stdin=None):
        return self.gramps.run(*args, stdin=stdin)

    def close(self):
        self.db.close()
        self.call("-r", self.NAME)

#class DBAPITest(unittest.TestCase):
    # dbwrap = DBAPI()

    # def setUp(self):
    #     self.db = self.dbwrap.db

    # @classmethod
    # def tearDownClass(cls):
    #     cls.dbwrap.close()

    # def test_open(self):
    #     self.assertTrue(self.db is not None)

    # def test_default_person(self):
    #     person = self.db.get_default_person()
    #     self.assertTrue(person is not None)

    # def test_get_field_1(self):
    #     person = self.db.get_default_person()
    #     gid = person.get_field("gid")
    #     self.assertTrue(gid == "I0037", gid)

    # def test_get_field_2(self):
    #     person = self.db.get_default_person()
    #     result = person.get_field("event_ref_list")
    #     self.assertTrue(len(result) == 4, result)
    #     self.assertTrue(all([isinstance(r, EventRef) for r in result]), result)

    # def test_select_1(self):
    #     result = list(self.db._select("Person", ["gid"]))
    #     self.assertTrue(len(result) == 60, len(result))

    # def test_select_2(self):
    #     result = list(self.db._select("Person", ["gid"],
    #                                   where=("gid", "LIKE", "I000%")))
    #     self.assertTrue(len(result) == 10, len(result))

    # def test_select_3(self):
    #     result = list(self.db._select("Family", ["mother_handle.gid"],
    #                     where=("mother_handle.gid", "LIKE", "I003%")))
    #     self.assertTrue(len(result) == 6, result)

    # def test_select_4(self):
    #     result = list(self.db._select("Family",
    #           ["mother_handle.event_ref_list.ref.gid"]))
    #     self.assertTrue(len(result) == 23, len(result))

    # def test_select_5(self):
    #     result = list(self.db._select("Family",
    #           ["mother_handle.event_ref_list.ref.self.gid"]))
    #     self.assertTrue(len(result) == 23, len(result))

    # def test_select_6(self):
    #     result = list(self.db._select("Family", ["mother_handle.event_ref_list.0"]))
    #     self.assertTrue(all([isinstance(r["mother_handle.event_ref_list.0"],
    #                                     (EventRef, type(None))) for r in result]),
    #                     [r["mother_handle.event_ref_list.0"] for r in result])

    # def test_select_7(self):
    #     result = list(self.db._select("Family", ["mother_handle.event_ref_list.0"],
    #                             where=("mother_handle.event_ref_list.0", "!=", None)))
    #     self.assertTrue(len(result) == 21, len(result))

    # def test_select_8(self):
    #     result = list(self.db._select("Family", ["mother_handle.event_ref_list.ref.gid"],
    #                             where=("mother_handle.event_ref_list.ref.gid", "=", 'E0156')))
    #     self.assertTrue(len(result) == 1, len(result))

    # def test_queryset_1(self):
    #     result = list(self.db.Person.select())
    #     self.assertTrue(len(result) == 60, len(result))

    # def test_queryset_2(self):
    #     result = list(self.db.Person.where(lambda person: LIKE(person.gid, "I000%")).select())
    #     self.assertTrue(len(result) == 10, len(result))

    # def test_queryset_3(self):
    #     result = list(self.db.Family
    #                   .where(lambda family: LIKE(family.mother_handle.gid, "I003%"))
    #                   .select())
    #     self.assertTrue(len(result) == 6, result)

    # def test_queryset_4a(self):
    #     result = list(self.db.Family.select())
    #     self.assertTrue(len(result) == 23, len(result))

    # def test_queryset_4b(self):
    #     result = list(self.db.Family
    #                   .where(lambda family: family.mother_handle.event_ref_list.ref.gid == 'E0156')
    #                   .select())
    #     self.assertTrue(len(result) == 1, len(result))

    # def test_queryset_5(self):
    #     result = list(self.db.Family
    #                   .select("mother_handle.event_ref_list.ref.self.gid"))
    #     self.assertTrue(len(result) == 23, len(result))

    # def test_queryset_6(self):
    #     result = list(self.db.Family.select("mother_handle.event_ref_list.0"))
    #     self.assertTrue(all([isinstance(r["mother_handle.event_ref_list.0"],
    #                                     (EventRef, type(None))) for r in result]),
    #                     [r["mother_handle.event_ref_list.0"] for r in result])

    # def test_queryset_7(self):
    #     result = list(self.db.Family
    #                   .where(lambda family: family.mother_handle.event_ref_list[0] != None)
    #                   .select())
    #     self.assertTrue(len(result) == 21, len(result))

    # def test_order_1(self):
    #     result = list(self.db.Person.order("gid").select())
    #     self.assertTrue(len(result) == 60, len(result))

    # def test_order_2(self):
    #     result = list(self.db.Person.order("-gid").select())
    #     self.assertTrue(len(result) == 60, len(result))

    # def test_proxy_1(self):
    #     result = list(self.db.Person.proxy("living", False).select())
    #     self.assertTrue(len(result) == 31, len(result))

    # def test_proxy_2(self):
    #     result = list(self.db.Person.proxy("living", True).select())
    #     self.assertTrue(len(result) == 60, len(result))

    # def test_proxy_3(self):
    #     result = len(list(self.db.Person
    #                       .proxy("private")
    #                       .order("-gid")
    #                       .select("gid")))
    #     self.assertTrue(result == 59, result)

    # def test_map_1(self):
    #     result = sum(list(self.db.Person.map(lambda p: 1).select()))
    #     self.assertTrue(result == 60, result)

    # def test_tag_1(self):
    #     self.db.Person.where(lambda person: person.gid == "I0001").tag("Test")
    #     result = self.db.Person.where(lambda person: person.tag_list.name == "Test").count()
    #     self.assertTrue(result == 1, result)

    # def test_tag_2(self):
    #     self.db.Person.where(lambda person: person.gid == "I0001").tag("Test")
    #     result = self.db.Person.where(lambda person: person.tag_list.name == "Test").count()
    #     self.assertTrue(result == 1, result)
    #     self.db.Person.where(lambda person: person.gid == "I0001").tag("Test", remove=True)
    #     result = self.db.Person.where(lambda person: person.tag_list.name == "Test").count()
    #     self.assertTrue(result == 0, result)

    # def test_filter_1(self):
    #     from gprime.filters.rules.person import (IsDescendantOf,
    #                                                  IsAncestorOf)
    #     from gprime.filters import GenericFilter
    #     filter = GenericFilter()
    #     filter.set_logical_op("or")
    #     filter.add_rule(IsDescendantOf(["I0057", True]))
    #     filter.add_rule(IsAncestorOf(["I0057", True]))
    #     result = self.db.Person.filter(filter).count()
    #     self.assertTrue(result == 14, result)
    #     filter.where = lambda person: person.private == True
    #     result = self.db.Person.filter(filter).count()
    #     self.assertTrue(result == 1, result)
    #     filter.where = lambda person: person.private != True
    #     result = self.db.Person.filter(filter).count()
    #     self.assertTrue(result == 13, result)

    # def test_filter_2(self):
    #     result = self.db.Person.filter(lambda p: p.private).count()
    #     self.assertTrue(result == 1, result)

    # def test_filter_3(self):
    #     result = self.db.Person.filter(lambda p: not p.private).count()
    #     self.assertTrue(result == 59, result)

    # def test_limit_1(self):
    #     result = self.db.Person.limit(count=50).count()
    #     self.assertTrue(result == 50, result)

    # def test_limit_2(self):
    #     result = self.db.Person.limit(start=50, count=50).count()
    #     self.assertTrue(result == 10, result)

    # def test_ordering_1(self):
    #     worked = None
    #     try:
    #         result = list(self.db.Person
    #                       .filter(lambda p: p.private)
    #                       .order("private")
    #                       .select())
    #         worked = True
    #     except:
    #         worked = False
    #     self.assertTrue(not worked, "should have failed")

    # def test_ordering_2(self):
    #     worked = None
    #     try:
    #         result = list(self.db.Person.order("private")
    #                       .filter(lambda p: p.private)
    #                       .select())
    #         worked = True
    #     except:
    #         worked = False
    #     self.assertTrue(worked, "should have worked")

if __name__ == "__main__":
    unittest.main()

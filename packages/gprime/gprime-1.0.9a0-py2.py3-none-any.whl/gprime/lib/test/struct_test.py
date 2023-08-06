#
# gPrime - A web-based genealogy program
#
# Copyright (C) 2013 Doug Blank <doug.blank@gmail.com>
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

""" Unittest for to_struct, from_struct """

import unittest
import os

from  .. import (Person, Family, Event, Source, Place, Citation,
                 Repository, Media, Note, Tag)
from gprime.lib.struct import Struct
from gprime.merge.diff import import_as_dict
from gprime.cli.user import User
from gprime.merge.diff import *
from gprime.const import DATA_DIR

TEST_DIR = os.path.abspath(os.path.join(DATA_DIR, "tests"))
EXAMPLE = os.path.join(TEST_DIR, "example.gramps")

class BaseCheck:
    def test_from_struct(self):
        struct = self.object.to_struct()
        serialized = self.cls.from_struct(struct)
        self.assertEqual(self.object.to_struct(), struct)

    def test_from_empty_struct(self):
        serialized = self.cls.from_struct({})
        self.assertEqual(self.object.to_struct(), serialized.to_struct())

class PersonCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Person
        self.object = self.cls()

class FamilyCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Family
        self.object = self.cls()

class EventCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Event
        self.object = self.cls()

class SourceCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Source
        self.object = self.cls()

class PlaceCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Place
        self.object = self.cls()

class CitationCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Citation
        self.object = self.cls()

class RepositoryCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Repository
        self.object = self.cls()

class MediaCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Media
        self.object = self.cls()

class NoteCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Note
        self.object = self.cls()

class TagCheck(unittest.TestCase, BaseCheck):
    def setUp(self):
        self.cls = Tag
        self.object = self.cls()

class DatabaseCheck(unittest.TestCase):
    maxDiff = None

def generate_case(obj):
    """
    Dynamically generate tests and attach to DatabaseCheck.
    """
    struct = obj.to_struct()
    serialized = obj.__class__.from_struct(struct)
    def test(self):
        self.assertEqual(obj.to_struct(), struct)
    name = "test_serialize_%s_%s" % (obj.__class__.__name__, obj.handle)
    setattr(DatabaseCheck, name, test)
    ####
    #def test2(self):
    #    self.assertEqual(obj.to_struct(), from_struct(struct).to_struct())
    #name = "test_create_%s_%s" % (obj.__class__.__name__, obj.handle)
    #setattr(DatabaseCheck, name, test2)

db = import_as_dict(EXAMPLE, User())
for table in db.get_table_func():
    for handle in db.get_table_func(table,"handles_func")():
        obj = db.get_table_func(table,"handle_func")(handle)
        generate_case(obj)

class StructTest(unittest.TestCase):
    def test(self):
        family = db.get_family_from_gid("F0001")
        s = Struct(family.to_struct(), db)
        self.assertEqual(s["gid"], "F0001")
        s["gid"] = "TEST"
        self.assertEqual(s["gid"], "TEST")
        self.assertEqual(s.father_handle.primary_name.first_name,
                         "Allen Carl")
        s["father_handle.primary_name.first_name"] = "Edward"
        self.assertEqual(s["father_handle.primary_name.first_name"],
                         "Edward")

if __name__ == "__main__":
    unittest.main()

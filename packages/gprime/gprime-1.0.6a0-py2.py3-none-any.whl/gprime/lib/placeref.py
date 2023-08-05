#
# gPrime - A web-based genealogy program
#
# Copyright (C) 2000-2007  Donald N. Allingham
# Copyright (C) 2013       Nick Hall
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

"""
Place Reference class for Gramps
"""

#-------------------------------------------------------------------------
#
# Gprime modules
#
#-------------------------------------------------------------------------
from .secondaryobj import SecondaryObject
from .refbase import RefBase
from .datebase import DateBase
from .const import IDENTICAL, EQUAL, DIFFERENT
from .handle import Handle

#-------------------------------------------------------------------------
#
# Place References
#
#-------------------------------------------------------------------------
class PlaceRef(RefBase, DateBase, SecondaryObject):
    """
    Place reference class.

    This class is for keeping information about how places link to other places
    in the place hierarchy.
    """

    def __init__(self, source=None):
        """
        Create a new PlaceRef instance, copying from the source if present.
        """
        RefBase.__init__(self, source)
        DateBase.__init__(self, source)

    def to_struct(self):
        """
        Convert the data held in this object to a structure (eg,
        struct) that represents all the data elements.

        This method is used to recursively convert the object into a
        self-documenting form that can easily be used for various
        purposes, including diffs and queries.

        These structures may be primitive Python types (string,
        integer, boolean, etc.) or complex Python types (lists,
        tuples, or dicts). If the return type is a dict, then the keys
        of the dict match the fieldname of the object. If the return
        struct (or value of a dict key) is a list, then it is a list
        of structs. Otherwise, the struct is just the value of the
        attribute.

        :returns: Returns a struct containing the data of the object.
        :rtype: dict
        """
        return {
            "_class": "PlaceRef",
            "ref": Handle("Place", self.ref),
            "date": DateBase.to_struct(self)
            }

    @classmethod
    def get_schema(cls):
        from .date import Date
        return {
            "_class": "PlaceRef",
            "ref": Handle("Place", "PLACE-HANDLE"),
            "date": Date
        }

    @classmethod
    def from_struct(cls, struct):
        """
        Given a struct data representation, return a serialized object.

        :returns: Returns a serialized object
        """
        self = PlaceRef()
        RefBase.set_from_struct(self, struct)
        DateBase.set_from_struct(self, struct)
        return self

    def get_text_data_list(self):
        """
        Return the list of all textual attributes of the object.

        :returns: Returns the list of all textual attributes of the object.
        :rtype: list
        """
        return []

    def get_text_data_child_list(self):
        """
        Return the list of child objects that may carry textual data.

        :returns: Returns the list of child objects that may carry textual data.
        :rtype: list
        """
        return []

    def get_citation_child_list(self):
        """
        Return the list of child secondary objects that may refer citations.

        :returns: Returns the list of child secondary child objects that may
                  refer citations.
        :rtype: list
        """
        return []

    def get_note_child_list(self):
        """
        Return the list of child secondary objects that may refer notes.

        :returns: Returns the list of child secondary child objects that may
                  refer notes.
        :rtype: list
        """
        return []

    def get_referenced_handles(self):
        """
        Return the list of (classname, handle) tuples for all directly
        referenced primary objects.

        :returns: Returns the list of (classname, handle) tuples for referenced
                  objects.
        :rtype: list
        """
        return [('Place', self.ref)]

    def get_handle_referents(self):
        """
        Return the list of child objects which may, directly or through their
        children, reference primary objects..

        :returns: Returns the list of objects referencing primary objects.
        :rtype: list
        """
        return []

    def is_equivalent(self, other):
        """
        Return if this eventref is equivalent, that is agrees in handle and
        role, to other.

        :param other: The eventref to compare this one to.
        :type other: PlaceRef
        :returns: Constant indicating degree of equivalence.
        :rtype: int
        """
        if self.ref != other.ref or self.date != other.date:
            return DIFFERENT
        else:
            if self.is_equal(other):
                return IDENTICAL
            else:
                return EQUAL

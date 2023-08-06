#
# gPrime - A web-based genealogy program
#
# Copyright (C) 2000-2007  Donald N. Allingham
# Copyright (C) 2010       Michiel D. Nauta
# Copyright (C) 2011       Tim G L Lyons
# Copyright (C) 2013       Doug Blank <doug.blank@gmail.com>
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
Event Reference class for Gramps
"""

#-------------------------------------------------------------------------
#
# Gprime modules
#
#-------------------------------------------------------------------------
from .secondaryobj import SecondaryObject
from .privacybase import PrivacyBase
from .notebase import NoteBase
from .attrbase import AttributeBase
from .refbase import RefBase
from .eventroletype import EventRoleType
from .const import IDENTICAL, EQUAL, DIFFERENT
from .citationbase import IndirectCitationBase
from .handle import Handle

#-------------------------------------------------------------------------
#
# Event References for Person/Family
#
#-------------------------------------------------------------------------
class EventRef(PrivacyBase, NoteBase, AttributeBase, RefBase,
               IndirectCitationBase, SecondaryObject):
    """
    Event reference class.

    This class is for keeping information about how the person relates
    to the referenced event.
    """

    def __init__(self, source=None):
        """
        Create a new EventRef instance, copying from the source if present.
        """
        PrivacyBase.__init__(self, source)
        NoteBase.__init__(self, source)
        AttributeBase.__init__(self, source)
        RefBase.__init__(self, source)
        if source:
            self.__role = EventRoleType(source.role)
        else:
            self.__role = EventRoleType()

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
            "_class": "EventRef",
            "private": PrivacyBase.to_struct(self),
            "note_list": NoteBase.to_struct(self),
            "attribute_list": AttributeBase.to_struct(self),
            "ref": Handle("Event", self.ref),
            "role": self.__role.to_struct()
            }

    @classmethod
    def get_schema(cls):
        """
        Returns the schema for EventRef.

        :returns: Returns a dict containing the fields to types.
        :rtype: dict
        """
        from .attribute import Attribute
        return {
            "private": bool,
            "note_list": [Handle("Note", "NOTE-HANDLE")],
            "attribute_list": [Attribute],
            "ref": Handle("Event", "EVENT-HANDLE"),
            "role": EventRoleType,
        }

    @classmethod
    def get_labels(cls, _):
        """
        Given a translation function, returns the labels for
        each field of this object.

        :returns: Returns a dict containing the fields to labels.
        :rtype: dict
        """
        return {
            "private": _("Private"),
            "note_list": _("Notes"),
            "attribute_list": _("Attributes"),
            "ref": _("Event"),
            "role": _("Role"),
        }

    @classmethod
    def from_struct(cls, struct):
        """
        Given a struct data representation, return a serialized object.

        :returns: Returns a serialized object
        """
        self = default = EventRef()
        PrivacyBase.set_from_struct(self, struct)
        NoteBase.set_from_struct(self, struct)
        AttributeBase.set_from_struct(self, struct)
        RefBase.set_from_struct(self, struct)
        role = struct.get("role", {})
        self.__role = EventRoleType.from_struct(role)
        return self

    def get_text_data_list(self):
        """
        Return the list of all textual attributes of the object.

        :returns: Returns the list of all textual attributes of the object.
        :rtype: list
        """
        return [self.__role.string]

    def get_text_data_child_list(self):
        """
        Return the list of child objects that may carry textual data.

        :returns: Returns the list of child objects that may carry textual data.
        :rtype: list
        """
        return  self.attribute_list

    def get_citation_child_list(self):
        """
        Return the list of child secondary objects that may refer citations.

        :returns: Returns the list of child secondary child objects that may
                  refer citations.
        :rtype: list
        """
        return self.attribute_list

    def get_note_child_list(self):
        """
        Return the list of child secondary objects that may refer notes.

        :returns: Returns the list of child secondary child objects that may
                  refer notes.
        :rtype: list
        """
        return self.attribute_list

    def get_referenced_handles(self):
        """
        Return the list of (classname, handle) tuples for all directly
        referenced primary objects.

        :returns: Returns the list of (classname, handle) tuples for referenced
                  objects.
        :rtype: list
        """
        ret = self.get_referenced_note_handles()
        if self.ref:
            ret += [('Event', self.ref)]
        return ret

    def get_handle_referents(self):
        """
        Return the list of child objects which may, directly or through their
        children, reference primary objects..

        :returns: Returns the list of objects referencing primary objects.
        :rtype: list
        """
        return self.get_citation_child_list()

    def is_equivalent(self, other):
        """
        Return if this eventref is equivalent, that is agrees in handle and
        role, to other.

        :param other: The eventref to compare this one to.
        :type other: EventRef
        :returns: Constant indicating degree of equivalence.
        :rtype: int
        """
        if self.ref != other.ref or self.role != other.role:
            return DIFFERENT
        else:
            if self.is_equal(other):
                return IDENTICAL
            else:
                return EQUAL

    def merge(self, acquisition):
        """
        Merge the content of acquisition into this eventref.

        Lost: hlink and role of acquisition.

        :param acquisition: The eventref to merge with the present eventref.
        :type acquisition: EventRef
        """
        self._merge_privacy(acquisition)
        self._merge_attribute_list(acquisition)
        self._merge_note_list(acquisition)

    def get_role(self):
        """
        Return the tuple corresponding to the preset role.
        """
        return self.__role

    def set_role(self, role):
        """
        Set the role according to the given argument.
        """
        self.__role.set(role)
    role = property(get_role, set_role, None, 'Returns or sets role property')

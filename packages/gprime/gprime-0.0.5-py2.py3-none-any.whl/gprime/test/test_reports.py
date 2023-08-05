#! /usr/bin/env python3
#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (c) 2016 Gramps Development Team
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#

import unittest
import os
import shutil

from .test_util import Gramps
from gprime.db import open_database

ddir = os.path.dirname(__file__)
example = os.path.join(ddir, "..", "..",
                       "example", "gramps", "data.gramps")
sample = os.path.join(ddir, "..", "..",
                      "example", "gedcom", "sample.ged")

TREE_NAME = "Test_reporttest"

class ReportControl:
    def tearDown(self):
        out, err = self.call("-y", "--remove", TREE_NAME)
        out, err = self.call("-y", "--remove", TREE_NAME + "_import_gedcom")

    def call(self, *args):
        print("call:", args)
        self.gramps = Gramps()
        out, err = self.gramps.run(*args)
        print("out:", out, "err:", err)
        return out, err

    def __init__(self):
        super().__init__()
        self.tearDown() # removes it if it existed
        out, err = self.call("-C", TREE_NAME,
                             "--import", example)

    def addreport(self, class_, report_name, test_function,
                  files, **options):
        test_name = report_name.replace("-", "_")
        setattr(class_, test_name, dynamic_report_method(
            report_name,
            test_function,
            files,
            "--force",
            "-O", TREE_NAME,
            "--action", "report",
            "--options", "name=%s" % report_name,
            **options))

    def addcli(self, class_, report_name, test_function,
               files, *args, **options):
        test_name = report_name.replace("-", "_")
        setattr(class_, test_name,
                dynamic_cli_method(
                    report_name,
                    test_function,
                    files,
                    *args))

def dynamic_report_method(report_name, test_function,
                          files, *args, **options):
    args = list(args)
    args[-1] += "," + (",".join(["%s=%s" % (k, v) for (k,v) in options.items()]))
    options["files"] = files
    # This needs to have "test" in name:
    def test_method(self):
        out, err = self.call(*args)
        self.assertTrue(test_function(out, err, report_name, **options), "out: %s, err: %s" % (out, err))
    return test_method

def dynamic_cli_method(report_name, test_function,
                       files, *args, **options):
    options["files"] = files
    # This needs to have "test" in name:
    def test_method(self):
        out, err = self.call(*args)
        self.assertTrue(test_function(out, err, report_name, **options), "out: %s, err: %s" % (out, err))
    return test_method

class TestDynamic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            os.makedirs("temp")
        except:
            pass

    @classmethod
    def call(cls, *args):
        print("call:", args)
        gramps = Gramps()
        out, err = gramps.run(*args)
        print("out:", out, "err:", err)
        return out, err

    @classmethod
    def tearDownClass(cls):
        out, err = cls.call("-y", "--remove", TREE_NAME)
        out, err = cls.call("-y", "--remove", TREE_NAME + "_import_gedcom")

reports = ReportControl()

def report_contains(text):
    def test_output_file(out, err, report_name, **options):
        ext = options["off"]
        with open(report_name + "." + ext) as fp:
            contents = fp.read()
        print(contents)
        if options.get("files", []):
            for filename in options.get("files", []):
                if filename is None:
                    pass
                elif os.path.isdir(filename):
                    shutil.rmtree(filename)
                elif os.path.isfile(filename):
                    os.remove(filename)
                else:
                    raise Exception("can't find '%s' in order to delete it" % filename)
        elif os.path.isfile(report_name + "." + ext):
            os.remove(report_name + "." + ext)
        else:
            raise Exception("can't find '%s' in order to delete it" % (report_name + "." + ext))
        return text in contents
    return test_output_file

def err_does_not_contain(text):
    def test_output_file(out, err, report_name, **options):
        if options.get("files", []):
            for filename in options.get("files", []):
                if filename is None:
                    pass
                elif os.path.isdir(filename):
                    shutil.rmtree(filename)
                elif os.path.isfile(filename):
                    os.remove(filename)
                else:
                    raise Exception("can't find '%s' in order to delete it" % filename)
        else:
            ext = options["off"]
            if os.path.isfile(report_name + "." + ext):
                os.remove(report_name + "." + ext)
            else:
                raise Exception("can't find '%s' in order to delete it" % (report_name + "." + ext))
        return text not in err
    return test_output_file

def err_does_contain(text):
    def test_output_file(out, err, report_name, **options):
        if options.get("files", []):
            for filename in options.get("files", []):
                if filename is None:
                    pass
                elif os.path.isdir(filename):
                    shutil.rmtree(filename)
                elif os.path.isfile(filename):
                    os.remove(filename)
                else:
                    raise Exception("can't find '%s' in order to delete it" % filename)
        else:
            ext = options["off"]
            if os.path.isfile(report_name + "." + ext):
                os.remove(report_name + "." + ext)
            else:
                raise Exception("can't find '%s' in order to delete it" % (report_name + "." + ext))
        if isinstance(text, list):
            return all([(line in err) for line in text])
        else:
            return text in err
    return test_output_file

def out_does_contain(text):
    def test_output_file(out, err, report_name, **options):
        if options.get("files", []):
            for filename in options.get("files", []):
                if filename is None:
                    pass
                elif os.path.isdir(filename):
                    shutil.rmtree(filename)
                elif os.path.isfile(filename):
                    os.remove(filename)
                else:
                    raise Exception("can't find '%s' in order to delete it" % filename)
        else:
            ext = options["off"]
            if os.path.isfile(report_name + "." + ext):
                os.remove(report_name + "." + ext)
            else:
                raise Exception("can't find '%s' in order to delete it" % (report_name + "." + ext))
        if isinstance(text, list):
            return all([(line in out) for line in text])
        else:
            return text in out
    return test_output_file

reports.addreport(TestDynamic, "tag_report",
                  report_contains("I0037  Smith, Edwin Michael"),
                  [],
                  off="txt", tag="tag1")

#reports.addreport(TestDynamic, "WebCal",
#                  err_does_not_contain("Failed to write report."),
#                  ["/tmp/WEBCAL"],
#                  off="html", target="/tmp/WEBCAL")

# THIRD-PARTY
#reports.addreport(TestDynamic, "database-differences-report",
#                  err_does_not_contain("Failed to write report."),
#                  [],
#                  off="txt", filename=example)

reports.addcli(TestDynamic, "export_gedcom",
               err_does_contain("Cleaning up."),
               ["test_export.ged"],
               "--force",
               "-O", TREE_NAME,
               "--export", "test_export.ged")

# reports.addcli(TestDynamic, "export_csv",
#                err_does_contain("Cleaning up."),
#                ["test_export.csv"],
#                "--force",
#                "-O", TREE_NAME,
#                "--export", "test_export.csv")

# reports.addcli(TestDynamic, "export_wtf",
#                err_does_contain("Cleaning up."),
#                ["test_export.wtf"],
#                "--force",
#                "-O", TREE_NAME,
#                "--export", "test_export.wtf")

report_list = [
    ("ancestor_chart", "svg", ["ancestor_chart.svg",
                               "ancestor_chart-2.svg",
                               "ancestor_chart-3.svg",
                               "ancestor_chart-4.svg",
                               "ancestor_chart-5.svg",
                               "ancestor_chart-6.svg",
                           ]), # Ancestor Tree
    ("ancestor_report", "txt", []), # Ahnentafel Report
    ("birthday_report", "txt", []), # Birthday and Anniversary Report
    ("calendar", "svg", ["calendar-10.svg", "calendar-11.svg",
                         "calendar-12.svg", "calendar-2.svg",
                         "calendar-3.svg", "calendar-4.svg",
                         "calendar-5.svg", "calendar-6.svg",
                         "calendar-7.svg", "calendar-8.svg",
                         "calendar-9.svg", "calendar.svg"]), # Calendar
    ("descend_chart", "svg", []), # Descendant Tree
    ("descend_report", "txt", []), # Descendant Report
    ("det_ancestor_report", "txt", []), # Detailed Ancestral Report
    ("det_descendant_report", "txt", []), # Detailed Descendant Report
    ("endofline_report", "txt", []), # End of Line Report
    ("family_descend_chart", "svg", []), # Family Descendant Tree
    ("family_group", "txt", []), # Family Group Report
    ## COULD be dot ("familylines_graph", "dot", []), # Family Lines Graph
    ("fan_chart", "svg", []), # Fan Chart
    ## COULD be dot ("hourglass_graph", "dot", []), # Hourglass Graph
    ("indiv_complete", "txt", []), # Complete Individual Report
    ("kinship_report", "txt", []), # Kinship Report
    ("notelinkreport", "txt", []), # Note Link Report
    ("number_of_ancestors", "txt", []), # Number of Ancestors Report
    ## NEED a place ("place_report", "txt", []), # Place Report
    ("records", "txt", []), # Records Report
    ## COULD be dot ("rel_graph", "dot", []), # Relationship Graph
    ("statistics_chart", "svg", ["statistics_chart.svg",
                                 "statistics_chart-2.svg",
                                 "statistics_chart-3.svg"]), # Statistics Charts
    ("summary", "txt", []), # Database Summary Report
    ("timeline", "svg", ["timeline.svg", "timeline-2.svg"]), # Timeline Chart
]

for (report_name, off, files) in report_list:
    reports.addreport(TestDynamic, report_name,
                      err_does_not_contain("Failed to write report."),
                      files=files,
                      off=off)

# reports.addcli(TestDynamic, "tool_verify",
#                out_does_contain([
#                                  "W: Early marriage, Family: F0000, Smith, Martin and Jefferson, Elna",
#                                  "W: Multiple parents, Person: I0061, Jones, Roberta Michele",
#                                  "W: Multiple parents, Person: I0063, Jones, Frank Albert",
#                                  "W: Multiple parents, Person: I0076, Smith, Marie Astri",
#                                  "W: Multiple parents, Person: I0077, Smith, Susan Elizabeth",
#                                  "W: Old age but no death, Person: I0004, Smith, Ingeman",
#                                  "W: Old age but no death, Person: I0009, Smith, Emil",
#                                  "W: Old age but no death, Person: I0011, Smith, Hanna",
#                                  "W: Old age but no death, Person: I0058, Smith, Elaine Marie",
#                                  "W: Old age but no death, Person: I0072, Iverson, Alice Hannah",
#                                 ]),
#                [None],
#                "--force",
#                "-O", TREE_NAME,
#                "-y",
#                "--action", "tool",
#                "--options", "name=verify")

# reports.addcli(TestDynamic, "tool_check",
#                out_does_contain(["6 media objects were referenced, but not found",
#                                  "References to 6 media objects were kept"]),
#                [None],
#                "--force",
#                "-O", TREE_NAME,
#                "-y",
#                "--action", "tool",
#                "--options", "name=check")

if __name__ == "__main__":
    unittest.main()

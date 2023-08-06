# Copyright (C) 2009-2014 by Philip L. Budne
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

"""
XPath like query interface for JSON Storage Access Methods

The names "JPath" and "jsonpath" are already in use!

jsam.xpath(path [,output=xpath.Out.OBJS][,debug=0][,show_id=True])

PATH can be an XPath like query string (below), or an P4J path
(see jsam.p4j).

PATH grammar:
    PATH: ( "" | "/" | "//" ) STEP { ("/" | "//") STEP }

    STEP: ABBREV_STEP | [ AXIS "::" ] NODE_TEST [ PREDICATE ]

    ABBREV_STEP: "." | ".."

    AXIS: "ancestor" | "ancestor-or-self" | "child" |
                "descendant" | "descendant-or-self" | "following" |
                "following-sibling" | "parent" | "preceding" |
                "preceding-sibling" | "self" | "sibling"

    NODE_TEST: "*" | NAME | NUMBER

    PREDICATE: "[" EXPR "]"

    EXPR: AND_EXPR { "or" AND_EXPR }

    AND_EXPR: REL_EXPR { "and" REL_EXPR }

    REL_EXPR: PATH [ RELOP PRIMARY ]

    RELOP: "=" | "!=" | "<" | "<=" | ">" | ">=" | "like" | "regexp"

    PRIMARY: NAME | NUMBER | VAR_REF

format is one of:
        xpath.Out.IDS        return list of object id's for matching objects
        xpath.Out.PATHS      return list of paths for matching (sub) objects
        xpath.Out.PATHKEYS   return list of list of id and path keys/indices
        xpath.Out.OBJS       return list of matching (sub) objects

show_id controls whether object ID appears as a leading path step
        in searches and returned paths (ie; /ID/path...)
        If show_id is false, xpath.Out.PATHS returns a list (id,path) tuples.
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.9 $"

class Out(object):
    """output types for jsam.xpath"""
    IDS = 0     # return object ids
    PATHS = 1   # return XPath strings
    OBJS = 2    # return matched (sub)objects
    PATHKEYS = 3 # return list of keys/indices

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
JSDBI mix-in

Subclass of JSDBI for DB-API2 implementations that
support '?' for query parameters but not '%s'
(sqlite3, for example)
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.8 $"

import jsdbi

class JSDBIQMark(jsdbi.JSDBI):
    """JSDBI mix-in w/ an _execute() method that translates '%s' to '?'"""

    def __init__(self):
        jsdbi.JSDBI.__init__(self)

    def _execute(self, stmt, args):
        """execute a query, translating '%s' to '?'"""
        # this from Django-1.0:
        #   %s used for all args (most DB-API impl's implement it)
        #   if you want a '%' in the stmt, it must be doubled.
        #
        # Sneakier than my plan of str.replace("%s", "?")
        # (which would screw up on "%%s")
        #
        # preferring '%s' allows JSDBI.execute() debug mode to easily
        # format output string!
        nstmt = stmt % tuple(len(args) * "?")
        self.cur.execute(nstmt, args)

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
JSON object collection interface

User applies a series of keep/drop filters to an initially full set
of JSON objects, using method chaining (like jQuery and Django).

Each chained method returns a new object, so composition be be performed:
        a = full().keep(....)
        b = a.keep(.....)
        c = a.drop(.....)

keep() and drop() take the following arguments by keyword or position:

key:    the name of the object/dictionary key to test the value of
value:  the value to compare against
match:  comparison operator::
        * "exact": match entire string
        * "iexact": case independent match of entire string
        * "contains": value appears anywhere
        * "icontains": value appears anywhere (case independent)
        * "regex": value is an extended (egrep) regular expression
        * "iregex": value is an extended (egrep) regular expression (case ind)
        * "startswith": value is a prefix
        * "istartswith": value is a prefix (case independent)
        * "endswith": value is a suffix
        * "iendswith": value is a suffix (case independent)

        SQL based JSAMs also support:
        * "like": matching with % and _ wildcarding
        * ">", ">=", "<", "<="

Lookups are deferred until a collection is indexed or iterated over,
and results are cached.

Each keep/drop term applies independently to the entire JSON object,
NOT just to the (sub)tree(s) that were matched by previous terms.
This limitation is so that a simple file-based implementation
using "grep" is possible.

On SQL based JSAMs, an XPath query syntax (jsam.xpath) and a
a method chaining interface like jQuery[1] or JPath[2] (jsam.p4j)
are available.

BUGS: file based JSAMs may not honor all output formats.

[1] http://jquery.com/
[2] http://bluelinecity.com/software/jpath/
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.16 $"

import copy

class CollectionException(Exception):
    """Base Class for Collection Exceptions"""

class VirtualMethodError(CollectionException):
    """Raised by methods that need to be overridden"""

class UnknownMatchOpError(CollectionException):
    """Raised by storage/execution engines for unknown match operator"""

class UnknownOutputError(CollectionException):
    """Raised by storage/execution engines for unknown output format"""

class NeedKeyOrValueError(CollectionException):
    """Must have either Key or Value"""

class NeedKeepError(CollectionException):
    """Output format requires 'keep'"""

class _FN(object):
    """INTERNAL: Collection filter node representation"""

    def __init__(self, keep, key, match, value):
        """keep (or drop)"""
        if key is None and value is None:
            raise NeedKeyOrValueError()
        self.keep = keep
        self.key = key
        self.match = match
        self.value = value

    def __repr__(self):
        return "_FN(%s, %s, %s, %s)" % \
            (self.keep, self.key, self.match, self.value)

class Output(object):
    """Output formats (values for Collection.out)"""
    IDS = 1             # object ids
    KEYS = 2            # all key names
    TREES = 3           # full trees

    # for file based jsam last filter must be a "keep":
    VALUES = 4          # matching values
    IDVALUE = 5         # (id, value) tuples
    IDKEYVALUE = 6      # (id, key, value) tuples

    # formats below this line not implemented for file based jsams:
    # require at least one keep/drop:
    PATHS = 10          # (id, path) tuples to matched nodes
    PARENT = 11         # ancestor trees of matched nodes
    SUBTREES = 12       # subtrees including matched nodes

class Collection(object):
    """JSON Collection Object"""

    def __init__(self, full_=True):
        self.full = full_
        self.nodes = []
        self.cache = None
        self.out = Output.IDS
        self._order = 0
        self._distinct = True
        self._count = False
        self._limit = None
        self._offset = None

    def _keep_or_drop(self, node):
        """helper: copy existing object and append new node"""
        new = self._copy()
        new.nodes.append(node)
        return new

    def keep(self, key=None, value=None, match="exact"):
        """apply a filter to keep objects with matching keys/values
           like jQuery and Django 'filter'"""
        return self._keep_or_drop(_FN(True, key, match, value))

    # alias:
    filter = keep

    def drop(self, key=None, value=None, match="exact"):
        """apply a filter to drop objects with matching keys/values
           like jQuery 'not', Django 'drop'"""
        return self._keep_or_drop(_FN(False, key, match, value))

    ################ OUTPUT FORMAT

    def ids(self):
        """set collection output format to object ids"""
        new = self._copy()
        new.out = Output.IDS
        new._distinct = True
        return new

    def keys(self, leaves=True):
        """set collection output format to keys"""
        new = self._copy()
        new.out = Output.KEYS
        new._distinct = True
        new.leafkeys = leaves
        return new

    def values(self):
        """set collection output format to values"""
        new = self._copy()
        new.out = Output.VALUES
        new._distinct = True
        return new

    def idvalues(self):
        """set collection output format to id,value tuples"""
        new = self._copy()
        new.out = Output.IDVALUE
        new._distinct = True
        return new

    def idkeyvalues(self):
        """set collection output format to id,key,value tuples"""
        new = self._copy()
        new.out = Output.IDKEYVALUE
        new._distinct = True
        return new

    def trees(self):
        """set collection output format to full trees"""
        new = self._copy()
        new.out = Output.TREES
        new._distinct = True
        return new

    ##### output formats that require terminal keep:

    def paths(self):
        """set collection output format to path list"""
        new = self._copy()
        # set _distinct?
        new.out = Output.PATHS
        return new

    def parent(self, parent):
        """set collection output format to
           ancestor tree given ancestor node key,
           or integer index into ancestors"""
        new = self._copy()
        new.out = Output.PARENT
        new.parent = parent
        return new

    def subtrees(self):
        """set collection output format to child tree"""
        new = self._copy()
        new.out = Output.SUBTREES
        return new

    ################ OTHER QUERY/OUTPUT OPTIONS

    def count(self):
        """return list with count of matching objects"""
        new = self._copy()
        new._count = True
        return new

    def distinct(self, distinct=True):
        """return only one copy of each element"""
        new = self._copy()
        new._distinct = distinct
        return new

    def order(self, order=1):
        """Order on output type (ID, unless keys())
           order > 0 means forward sort; < 0 reverse sort; 0 no sorting"""
        new = self._copy()
        new._order = order
        return new

    def limit(self, limit=1, offset=None):
        """limit number of elements returned"""
        new = self._copy()
        new._limit = limit
        new._offset = offset
        return new

    ################ perform lookups, return list

    def lookup(self, refresh=False):
        """return cached values, or perform lookup"""
        if self.cache is None or refresh:
            self.cache = self._execute()
        return self.cache

    ################ MAGIC

    def __getitem__(self, key):
        """list indexing/slicing; perform query, return indexed item(s)"""
        if self.cache is None:
            self.cache = self._execute()
        return self.cache[key]

    def __len__(self):
        """list length; perform query if needed"""
        if self.cache is None:
            self.cache = self._execute()
        return len(self.cache)

    def __iter__(self):
        """list iterator: perform query if needed"""
        if self.cache is None:
            self.cache = self._execute()
        return iter(self.cache)

    ################ PRIVATE

    def _copy(self):
        """copy self, make new list of nodes, but don't copy nodes"""
        new = copy.copy(self)
        new.nodes = list(self.nodes)
        return new

    def _execute(self):
        """execute query: must be overridden"""
        raise VirtualMethodError()

    ################ methods for subclasses only:

    def get_count(self):
        """return output count setting (bool)"""
        return self._count

    def get_distinct(self):
        """return distinct output setting (bool)"""
        return self._distinct

    def get_limit(self):
        """return limit output setting (int or None)"""
        return self._limit

    def get_offset(self):
        """return offset output setting (int or None)"""
        return self._offset

    def get_order(self):
        """return order output setting
           > 0 means forward sort; < 0 reverse sort; 0 no sorting"""
        return self._order

def full():
    """return a full collection"""
    return Collection(True)

def empty():
    """return an empty collection"""
    return Collection(False)

if __name__ == "__main__":
    aaa = full()
    bbb = aaa.keep("a", "b")
    ccc = bbb.drop("c", "d")
    print aaa.nodes
    print bbb.nodes
    print ccc.nodes

    print empty().nodes

    try:
        empty().keep()
    except NeedKeyOrValueError:
        print "OK"

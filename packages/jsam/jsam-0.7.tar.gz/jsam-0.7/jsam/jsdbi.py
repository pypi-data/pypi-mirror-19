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
Thin Data Base Interface adaption layer on DB-API2 for JSONSQL

Currently provides only a single cursor.
"""

# Started October 2008
__author__ = "Phil Budne"
__revision__ = "$Revision: 1.21 $"

import time

class JSDBIException(Exception):
    """Base Class for JSDBI Exceptions"""

class JSDBINotImplemented(JSDBIException):
    """JSDBI Method Not Implemented"""

class Column(object):
    """representation of an SQL database table column"""
    def __init__(self, name, dtype, size='',
                 primary=False, auto_inc=False, index=False):
        self.name = name
        self.type = dtype
        self.size = size
        self.primary = primary
        self.auto_inc = auto_inc
        self.index = index

class Table(object):
    """representation of an SQL database table"""

    # class variable: dict of tables, indexed by table name
    tables = {}

    def __init__(self, conn, name):
        self.conn = conn
        self.name = name
        # list of Column objects
        self.cols = []
        # dict of columns, indexed by column name
        self.cols_by_name = {}
        Table.tables[name] = self

    def add_column(self, name, dtype, **kws):
        """add a column to the table"""
        col = Column(name, dtype, **kws)
        self.cols.append(col)
        self.cols_by_name[col.name] = col

class JSDBI(object):
    """Base Class for JSONSQL DataBase Interface implementations"""

    table_factory = Table

    def __init__(self):
        self.debug = 0
        self.conn = None
        self.cur = None

    def execute(self, stmt, args=(), debug=0):
        """execute an SQL stmt interpolating args for %s's
           if you want a '%' in the stmt, it must be doubled."""

        # both % operator and sqlite3 DB-API execute want tuple, not list:
        if isinstance(args, list):
            args = tuple(args)

        if self.debug > 0 or debug > 0:
            if self.debug > 1 or debug > 1:
                print "stmt:", stmt
                print "args:", args
            try:
                bracketed_args = tuple(["{%s}" % unicode(a) for a in args ])
                print stmt % bracketed_args
            except TypeError:
                print "FORMATING ERROR"
            start = time.time()
            self._execute(stmt, args)
            print "time:", time.time() - start
        else:
            self._execute(stmt, args)

    def execute_insert(self, stmt, table, idcol, args=(), debug=0):
        """execute an SQL 'INSERT' and return newly created row ID"""
        self.execute(stmt, args, debug)
        return self._lastrowid(table, idcol)

    def close(self):
        """close database connection"""
        if self.conn:
            self._close()
            self.conn = None

    def begin(self):
        """enter a transaction -- MUST provide "REPEATABLE READ"!!!"""
        # enter transaction behind DB-API's back!
        self.cur.execute("BEGIN")

    def commit(self):
        """end transaction"""
        # NOTE!! not cur.commit()! DB-API may not know we're in a transaction.
        self.cur.execute("COMMIT")

    def rollback(self):
        """abort transaction"""
        self.cur.execute("ROLLBACK")

    def iter(self):
        """return iterator for result rows"""
        return self.cur

    def fetchall(self):
        """return list of result rows"""
        return self.cur.fetchall()

    def fetchone(self):
        """return one result row"""
        return self.cur.fetchone()

    ################ SQL portability

    def table(self, *args):
        """table creation method"""
        # invoke subclass specific table class constructor
        return self.table_factory(self, *args)

    ################ internal: override!!

    def _lastrowid(self, table, column):
        """return 'autoincrement' created row id from last INSERT"""
        raise JSDBINotImplemented()

    def _close(self): 
        """INTERNAL: must be overridden"""
        raise JSDBINotImplemented()

    def _execute(self, stmt, args):
        """INTERNAL: must be overridden"""
        raise JSDBINotImplemented()

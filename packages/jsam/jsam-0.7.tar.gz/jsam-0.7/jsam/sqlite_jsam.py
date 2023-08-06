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
SQLite3 JSON Storage Database Interface Module

URL syntax:
        sqlite:///relative_path_for_database_file
        sqlite:////abs_path_for_database_file

In case of a typo, the "host" field is also accepted:
        sqlite://relative_path_for_database_file

If neither host nor path supplied, path defaults to ":memory:" (temporary db).
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.28 $"
# With help from Django-1.0 SQLite3 backend

import re
try:
    import sqlite3              # 2.5
except ImportError:
    from pysqlite2 import dbapi2 as sqlite3 # pre 2.5

import jsonsql
import jsdbi
import jsdbiqmark

# 3.2.6 needed for COUNT(DISTINCT ...)
assert sqlite3.sqlite_version_info >= (3, 2, 6), "Need SQLite 3.2.6 or later"

TYPES = {
    'CHAR': 'TEXT',
    'TEXT': 'TEXT',
    'INT24' : 'INTEGER',
    'INT32' : 'INTEGER'
}

class SQLite3Table(jsdbi.Table):
    """representation of an SQLite database table"""

    def create(self, if_not_exists=True):
        """create database table"""
        text = "CREATE TABLE "
        ine = "IF NOT EXISTS " if if_not_exists else " "
        text += ine
        text += self.name + " ("
        first = True
        for col in self.cols:
            if first:
                first = False
            else:
                text += ","
            text += "\n"
            text += "    %s %s" % (col.name, TYPES[col.type])
            if col.primary:
                text += " PRIMARY KEY"
            if col.auto_inc:
                text += " AUTOINCREMENT"
        text += ")"
        # print text
        self.conn.execute(text)
        for col in self.cols:
            if col.index:
                # just use self.add_index(col.name)?
                table = self.name
                self.conn.execute("CREATE INDEX %s%s_%s_index ON %s (%s);\n" % \
                                (ine, table, col.name, table, col.name))

    def add_index(self, *colnames):
        """add database index on columns"""
        cmd = "CREATE INDEX IF NOT EXISTS %s_%s_index ON %s (%s)" % \
                (self.name, "_".join(colnames), self.name, ",".join(colnames))
        self.conn.execute(cmd)

def _exact(pat):
    """identity function"""
    return pat

def _esclike(pat, pfx='', sfx=''):
    """perform escaping for LIKE match chars"""
    # XXX re.escape does this by exploding string to list, and re-joining
    return pfx + pat.replace("%", r'\%').replace('_', r'\_') + sfx

class SQLite3(jsdbiqmark.JSDBIQMark):
    """JSDBI wrapper for SQLite3"""

    table_factory = SQLite3Table

    # support for collections:
    # with help from Django-1.0/django/db/backends/sqlite3/base.py:
    #   "SQLite requires LIKE statements to include an ESCAPE clause
    #   if the value being escaped has a percent or underscore in it.
    #   See http://www.sqlite.org/lang_expr.html for an explanation."

    _likestr = r"LIKE %s ESCAPE '\'"
    operators = {
        'exact': ('= %s',  _exact),
        'iexact': (_likestr, _esclike),

        'like' : (_likestr, _exact),    # case sensitive; %/_ allowed

        'regex': ('REGEXP %s', _exact),
        'iregex': ('REGEXP %s', lambda x: '(?i)' + x),

        '>': ('> %s', _exact),
        '>=': ('>= %s', _exact),
        '<': ('< %s', _exact),
        '<=': ('<= %s', _exact),

        'startswith': (_likestr, lambda x: _esclike(x, sfx='%')),
        'endswith': (_likestr, lambda x: _esclike(x, pfx='%')),
        'contains': (_likestr, lambda x: _esclike(x, '%', '%')),

        'istartswith': ('REGEXP %s', lambda x: '(?i)' + re.escape(x) + '.*'),
        'iendswith': ('REGEXP %s', lambda x: '(?i).*' + re.escape(x)),
        'icontains': ('REGEXP %s', lambda x: '(?i).*' + re.escape(x) + '.*')
    }

    def __init__(self, jsurl):
        jsdbiqmark.JSDBIQMark.__init__(self)

        # take path or host, in case someone forgot the third slash!
        # sqlite:///relative_path
        # sqlite:////abs_path
        # default to memory-based database!
        fname = jsurl.path or jsurl.host or ":memory:"
        if jsurl.kws:
            self.conn = sqlite3.connect(fname, **jsurl.kws)
        else:
            self.conn = sqlite3.connect(fname)

        # The default isolation level for SQLite is SERIALIZABLE
        # (stronger than the "REPEATABLE READ" we require)

        # Tells pysqlite NEVER to start transactions on it's own.  If
        # enabled it ALWAYS starts one when it sees a data
        # modification stmt even if we want to start the transaction
        # earler (on a select)!  The pysqlite documentation refers to
        # this as enabling "autocommit", which we override by
        # explicitly execute'ing "BEGIN" statements:
        #
        # http://www.sqlite.org/c3ref/get_autocommit.html
        #   "Autocommit mode is on by default.
        #   Autocommit mode is disabled by a BEGIN statement
        #   Autocommit mode is re-enabled by a COMMIT or ROLLBACK."
        self.conn.isolation_level = None

        self.conn.create_function("REGEXP", 2, sqlite_regexp)
        self.cur = self.conn.cursor()

    def _close(self):
        """close database connection"""
        self.cur.close()
        self.conn.close()

    # _execute from JSDBIqmark

    def _lastrowid(self, table, column):
        """return auto-increment key generated by last insert
        called by default execute_insert() method"""
        return self.cur.lastrowid

def sqlite_regexp(expr, item):
    """support for SQLite REGEXP match operator"""
    return re.compile(expr).match(item) is not None

def sqlite_jsam_open(jsurl, user):
    """called from JSURL.open() method; user is for log entries""" 
    return jsonsql.JSONSQL(SQLite3(jsurl), user)

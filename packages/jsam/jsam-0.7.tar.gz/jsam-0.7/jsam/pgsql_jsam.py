# Copyright (C) 2011-2014 by Philip L. Budne
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
PostgreSQL JSON Storage Database Interface Module using psycopg2

Lightly tested.

XPath search 22% faster than SQLite
Insert speed depends on shared_buffers config;
        with 28MB (default), slower than SQLite
        with 64MB, faster than MySQL

URL syntax:
        pgsql://[[user]:passwd@][host][:port]/db?key1=val1&key2=val2

The values in each of the fields shown above are passed to
psycopg2.connect() by keyword.  Leave host empty for local (Unix
domain) connection.  Arbitrary keyword/value pairs can be specified
using CGI URL-encoded syntax.
"""

# 
__author__ = "Phil Budne"
__revision__ = "$Revision: 1.4 $"
# With help from Django-1.0

import psycopg2

import jsonsql
import jsdbi

_types = {
    'CHAR': 'CHAR(1)',
    'TEXT': 'TEXT',
    'INT24' : 'INT',
    'INT32' : 'INT'
}

class PgSQLTable(jsdbi.Table):
    """representation of a PgSQL database table"""

    def create(self, if_not_exists=True):
        """create table"""
        text = "CREATE TABLE "
        text += self.name + " ("
        first = True
        for col in self.cols:
            if first:
                first = False
            else:
                text += ","
            if col.size != '':
                wid = "(%s)" % col.size
            else:
                wid = ''
            text += "\n"
            if col.auto_inc:
                text += "    %s SERIAL" % col.name # implies PRIMARY KEY
            else:
                # XXX include wid?
                text += "    %s %s%s" % (col.name, _types[col.type], wid)
                if col.primary:
                    text += " PRIMARY KEY"
        text += ");"
        try:
            # wrap in a transaction so we can rollback() to clear the error?
            ttt = 'BEGIN;' + text + '; END'
            self.conn.execute(ttt)
        except psycopg2.ProgrammingError, e:
            if e.pgerror.endswith("already exists\n") and if_not_exists:
                self.conn.rollback()
                return
            raise

        for col in self.cols:
            if col.index:
                self.add_index(col.name)

    def add_index(self, *colnames):
        """create index given column names"""
        cmd = "BEGIN; CREATE INDEX %s_%s_index ON %s (%s); END" % \
                (self.name, "_".join(colnames), self.name, ",".join(colnames))
        try:
            self.conn.execute(cmd)
        except psycopg2.ProgrammingError, e:
            if e.pgerror.endswith("already exists\n"):
                self.conn.rollback()
                return
            raise

def _exact(x):
    """identity function"""
    return x

def _esclike(x, pfx='', sfx=''):
    """perform escaping for LIKE match chars"""
    # XXX re.escape does this by exploding string to list, and re-joining
    return pfx + x.replace("%", r'\%').replace('_', r'\_') + sfx

class PgSQL(jsdbi.JSDBI):
    """JSDBI wrapper for PgSQL"""
    table_factory = PgSQLTable

    # with help from Django-1.0/django/db/backends/mysql/base.py:
    operators = {
        'exact': ('= %s',  _exact),
        'iexact': ("ILIKE %s", _esclike),

        'like' : ("LIKE %s", _exact),    # case sensitive; %/_ allowed

        'regex': ('~ %s', _exact),
        'iregex': ('~* %s', lambda x: '(?i)' + x),

        '>': ('> %s', _exact),
        '>=': ('>= %s', _exact),
        '<': ('< %s', _exact),
        '<=': ('<= %s', _exact),

        'startswith': ("LIKE %s", lambda x: _esclike(x, sfx='%')),
        'endswith': ("LIKE %s", lambda x: _esclike(x, pfx='%')),
        'contains': ("LIKE BINARY %s", lambda x: _esclike(x, '%', '%')),

        'istartswith': ("ILIKE %s", lambda x: _esclike(x, sfx='%')),
        'iendswith': ("ILIKE %s", lambda x: _esclike(x, pfx='%')),
        'icontains': ("ILIKE %s", lambda x: _esclike(x, '%', '%')),
    }

    def __init__(self, url):
        jsdbi.JSDBI.__init__(self)

        # use url to construct dict with keywords for psycopg2.connect()
        args = {}
        if url.host:
            args["host"] = url.host
        if url.user:
            args["user"] = url.user
        if url.passwd is not None:
            args["password"] = url.passwd
        if url.path:
            args["database"] = url.path
        if url.port:
            args["port"] = url.port

        # CGI params: var1=val1&var2=val2
        # allows arbitrary psycopg2.connect args (ie; sslmode)
        # to be passed in:
        args.update(url.kws)

        self.conn = psycopg2.connect(**args)
        # also "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ)
        try:
            # not in psycopg 2.2.1 (with Ubuntu 11.04)
            # supposed to be the default....
            self.conn.autocommit = False
        except AttributeError:
            # complain?
            pass

        self.cur = self.conn.cursor()

    def _close(self):
        """close database connection"""
        self.cur.close()
        self.conn.close()

    def _execute(self, stmt, args):
        """execute database query"""
        self.cur.execute(stmt, args)

    def execute_insert(self, stmt, table, idcol, args=(), debug=0):
        """execute an SQL 'INSERT' and return newly created row ID"""
        stmt += " RETURNING %s" % idcol
        self.execute(stmt, args, debug)
        return self.cur.fetchone()[0]

def pgsql_jsam_open(url, user):
    """called from JSURL.open() method; user is for log entries""" 
    return jsonsql.JSONSQL(PgSQL(url), user)

if __name__ == "__main__":
    import jsurl

#   urlstr = 'pgsql://phil:password@localhost/test' # via TCP
    urlstr = 'pgsql://phil@/test' # via unix socket
    uuu = jsurl.parse(urlstr)
    jjj = mysql_jsam_open(uuu, 'phil')
    jjj.begin()
    jjj.put("2", {'name': 'phil'})
    jjj.commit()
    print jjj.get("2")

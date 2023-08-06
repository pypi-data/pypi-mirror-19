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
MySQL JSON Storage Database Interface Module using MySQLdb.

Only lightly tested.
Insert speed 2x faster than SQLite, but xpath search 2.5x slower!

URL syntax:
        mysql://user:passwd@host:port/db?key1=val1&key2=val2

The values in each of the fields shown above are passed to
MySQLdb.connect() by keyword.  Arbitrary keyword/value pairs can be
specified using CGI URL-encoded syntax.
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.22 $"
# With help from Django-1.0

import MySQLdb

import jsonsql
import jsdbi

_types = {
    'CHAR' : 'CHAR(1)',
    'TEXT' : 'MEDIUMTEXT', # upto 16MB
    'INT24' : 'MEDIUMINT',
    'INT32' : 'INT'
}

# MUST support transactions, "REPEATABLE READ"
_engine = "InnoDB"

class MySQLTable(jsdbi.Table):
    """representation of a MySQL database table"""

    def create(self, if_not_exists=True):
        """create table"""
        text = "CREATE TABLE "
        #ine = "IF NOT EXISTS " if if_not_exists else " "
        #text += ine
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
            text += "    %s %s%s" % (col.name, _types[col.type], wid)
            if col.auto_inc:
                text += " AUTO_INCREMENT"
            if col.primary:
                text += " PRIMARY KEY"
            # XXX include wid?
            if col.index:
                text += ",\n    INDEX(%s)" % col.name
        text += ") DEFAULT CHARSET utf8 ENGINE=%s;" % _engine
        try:
            self.conn.execute(text)
        except MySQLdb.OperationalError, e:
            if e.args[0] != 1050 or not if_not_exists:
                raise

    def add_index(self, *colnames):
        """create index given column names"""
        cmd = "CREATE INDEX %s_%s_index ON %s (%s)" % \
                (self.name, "_".join(colnames), self.name, ",".join(colnames))
        # sqlite3 allows "CREATE INDEX IF NOT EXISTS"
        # ignore OperationalError(1061, "Duplicate key name....") [MySQL 5.1]
        try:
            self.conn.execute(cmd)
        except MySQLdb.OperationalError, e:
            if e.args[0] != 1061:
                raise           # pass up

def _exact(x):
    """identity function"""
    return x

def _esclike(x, pfx='', sfx=''):
    """perform escaping for LIKE match chars"""
    # XXX re.escape does this by exploding string to list, and re-joining
    return pfx + x.replace("%", r'\%').replace('_', r'\_') + sfx

class MySQL(jsdbi.JSDBI):
    """JSDBI wrapper for MySQL"""
    table_factory = MySQLTable

    # with help from Django-1.0/django/db/backends/mysql/base.py:
    operators = {
        'exact': ('= %s',  _exact),
        'iexact': ("LIKE %s", _esclike),

        'like' : ("LIKE %s", _exact),    # case sensitive; %/_ allowed

        'regex': ('REGEXP BINARY %s', _exact),
        'iregex': ('REGEXP %s', lambda x: '(?i)' + x),

        '>': ('> %s', _exact),
        '>=': ('>= %s', _exact),
        '<': ('< %s', _exact),
        '<=': ('<= %s', _exact),

        'startswith': ("LIKE BINARY %s", lambda x: _esclike(x, sfx='%')),
        'endswith': ("LIKE BINARY %s", lambda x: _esclike(x, pfx='%')),
        'contains': ("LIKE BINARY %s", lambda x: _esclike(x, '%', '%')),

        'istartswith': ("LIKE %s", lambda x: _esclike(x, sfx='%')),
        'iendswith': ("LIKE %s", lambda x: _esclike(x, pfx='%')),
        'icontains': ("LIKE %s", lambda x: _esclike(x, '%', '%')),
    }

    def __init__(self, url):
        jsdbi.JSDBI.__init__(self)

        # use url to construct dict with keywords for MySQLdb.connect()
        args = { "charset" : "utf8", 'use_unicode': True }
        if url.host:
            args["host"] = url.host
        if url.user:
            args["user"] = url.user
        if url.passwd:
            args["passwd"] = url.passwd
        if url.path:
            args["db"] = url.path
        # port ignored if host == "localhost" (unix domain socket used?)
        if url.port:
            args["port"] = url.port

        # CGI params: var1=val1&var2=val2
        # allows arbitrary MySQLdb.connections.Connection kwargs
        # to be passed in:
        args.update(url.kws)

        self.conn = MySQLdb.connect(**args)

        # kill auto commit; we want to have control over transaction starts
        # to obtain "repeatable reads"
        self.conn.autocommit(False)

        self.cur = self.conn.cursor()

        # The default for InnoDB?  Set it, just in case:
        self.cur.execute(
            "SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ")

    def _close(self):
        """close database connection"""
        self.cur.close()
        self.conn.close()

    def _execute(self, stmt, args):
        """execute database query"""
        self.cur.execute(stmt, args)

    def _lastrowid(self, table, column):
        """return auto-increment key generated by last insert"""
        return self.conn.insert_id()

def mysql_jsam_open(url, user):
    """called from JSURL.open() method; user is for log entries""" 
    return jsonsql.JSONSQL(MySQL(url), user)

if __name__ == "__main__":
    import jsurl

#   urlstr = 'mysql://phil:secret@localhost/foo' # via unix socket
#   urlstr = 'mysql://phil:secret@phil-budnes-ibook-g4.local:3306/foo'
    urlstr = 'mysql://phil:secret@127.0.0.1:3306/foo'
    uuu = jsurl.parse(urlstr)
    jjj = mysql_jsam_open(uuu, 'phil')
#    print jjj.get("2")

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
JSAM (JSON Storage Access Methods) is a "NoSQL" Database for JSON objects.

JSAM's basic operations are get, put and remove, with basic support
for transactions via begin, commit and rollback.  All stored objects
are identified by an integer key.

A JSAM database is opened by supplying a URL to jsam.jsurl.parse()
and calling the open() method on the returned object.  The syntax of
URL depends on the particular "access method".

The following URL types currently exist::

    * file:   directory plain text JSON files
    * rcs:    directory plain text JSON files under RCS
    * cvs:    directory plain text JSON files under CVS (not tested)
    * svn:    directory plain text JSON files under SVN (not tested)
    * sqlite: object trees stored in an SQLite3 database
    * mysql:  object trees stored in a MySQL database (lightly tested)
    * pgsql:  object trees stored in a PostgreSQL database (lightly tested)

Query methods include::

    * Collections: a jQuery/Django-like method-chained interface
    * XPath query language subset (only supported for SQL backends)
    * P4J (E4X-like) query language (only supported for SQL backends)
        which allows construction of "xpath" queries in Python using
        method chaining and operator overload, bridging the lexical divide
        between code and query.

pydoc jsam.<URLTYPE>_jsam
  gives information on the URL syntax for <URLTYPE>

pydoc jsam.jsam.JSAM
  gives information on jsam object methods

pydoc jsam.xpath
  gives information on XPath query syntax (SQL backends only)

pydoc jsam.p4j
  gives information on P4J Python native query syntax

NOTE::

    * uses Python 2.6+ supplied "json"; requires "simplejson" on Python 2.5
    * file-based storage depends on POSIX file semantics
    * requires "MySQLdb" for MySQL
    * requires "psycopg2" for PostgreSQL

The name "JSAM" is a joke on IBM Mainframe O/S data "Access Methods"
(BDAM, BSAM, VSAM, ISAM, QSAM, BPAM).

The obvious name 'jsonstore' was already taken by another package
in the Python Package Index (PyPI).

The URL/URI syntax was cribbed from Django, which copied SQLAlchemy.
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.29 $"
__version__ = '0.7'

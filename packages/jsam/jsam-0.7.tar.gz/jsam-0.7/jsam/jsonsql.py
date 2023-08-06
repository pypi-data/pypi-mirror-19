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
Store JSON Objects in an SQL database!

JSON objects are stored in an SQL database as trees. Each stored
object is identified by an integer "id".  Objects can only be stored
and removed, not modified in place.

I forget what I was drinking when I thought this was a good idea.
I'm still not sure I'm proud of what I've done.
It was certainly a feat, but not necessarily a well-advised one.

Implements "JSON Storage Access Method" (JSAM) API
Basic search and retrieval is available thru 'Collection' API.
XPath-like searches available via "xpath()" method.

Divorced from database specifics via "jdbi" API.
"""

# Started July 2008
__author__ = "Phil Budne"
__revision__ = "$Revision: 1.60 $"

# XXX handle COMMIT failure!

# This seemed like a better idea than using XML and XPath or XQuery,
# and I wanted more exact searching than allowed by Jsonstore
# (jsonstore.org which (ISTR) stores a JSON string representation of
# the object using "Shove"), and less hairy than CouchDB.

# Had I seen the more recent versions of jsonstore at
# http://code.google.com/p/jsonstore/
#       With the "entries" search mechanism
# and
# http://dealmeida.net/hg/jsonstore/
#       with Sqlite indexing.
# I might not have bothered with all this!

# Objects are stored one node (scalar, dict, or list) per row.  While
# this is flexible, you (well, at least I) can't easily run queries
# for adjacent data, nevermind data at different levels of the
# hierarchy.  One concession is that dict labels are stored with the
# labeled datum, so you can easily query by node and value.  See below
# for a more detailed description of how data is stored.

# The original implementation used SQLite3 via "apsw". It can now (in
# theory) use any database with dbapi2 API (via JSDBI wrapper), but
# in practice every database is a little different.

# The legacy of having started on sqlite may be evident (ie; a certain
# callousness about typing).

# Anyway, SQLite maps well to my needs:
# * Light traffic
# * Infrequent writes
# * Needs no server process
# * Loose datatyping
# * I'm an utter SQL neophite, I'm not missing anything!
# * Seems quick

# NOTE! Database format is meant to be languange agnostic
# (*NOT* Python specific)

import jsam

class JSONSQLException(jsam.JSAMException):
    """Parent class for all JSONSQL Exceptions"""

class JSONSQLBadDataError(JSONSQLException):
    """Internal Error: Unknown 'type' in database"""

class JSONSQLNotFrozenError(JSONSQLException):
    """Internal Error: no transaction in progress when one expected"""

class JSONSQLFrozenError(JSONSQLException):
    """Internal Error: database transaction in progress"""

class JSONSQL(jsam.JSAM, jsam.CollectionJSAM, jsam.XPathJSAM):
    """JSON Store Access Method for SQL Databases"""

    OBJECT = "O"
    ARRAY = "A"
    STR = "S"
    INT = "I"
    FLOAT = "F"
    BOOL = "B"
    NULL = "n"
    REF = "R"

    def __init__(self, conn, user):
        """takes a JSDBI object connection 'conn' and 'user' for logging
           will initialize database if needed"""
        jsam.JSAM.__init__(self, user)
        self.database_frozen = 0
        self.conn = conn

        # Data Declation:
        #

        # "id" is "record id number" used to distinguish different JSON
        #       objects stored.
        # "node" is a unique identifier for this storage instance of a
        #       sub-object
        # "parent" is node number of sub-object's parent used only
        #       when reconsituting a retreived object. Object root
        #       rows have 0 for parent
        # "type" is type of node:
        #       OBJECT, ARRAY, STR (utf-8 encoded), INT, REAL, BOOL, NULL
        # "idx" array index (integer) or object (hash) key string of
        #       this object within it's parent.  Object root rows have
        #       id for index. SQLite3 was ok with a column named
        #       'key', but MySQL was not!
        # "value" object value
        #       (len(obj) for OBJECT, ARRAY, empty for NULL nodes-- so sue me)
        # "lleft" "lright"
        #       labels for "nested set" representation of each object tree
        #               Joe Celko in DBMS Magazine March 1996
        #                   http://www.dbmsmag.com/9603d06.html
        #       Also in:
        #               Joe Celko's Trees and Hierarchies in SQL For Smarties
        #                   [ISBN-13: 978-1558609204]
        #               Joe Celko's SQL for Smarties [ISBN-13: 978-1558605763]
        #                   http://www.developersdex.com/gurus/articles/112.asp
        #       The technique was first published by Michael J. Kamfonas as
        #               "The Relational Taboo" in "The Relational Journal"
        #                   October/November 1992
        #                   http://www.kamfonas.com/id3.html
        #       See also http://en.wikipedia.org/wiki/Nested_set_model
        #
        #       labels are applied while inserting the nodes:
        #       llabel (left label) is enumerated preorder, so first child's
        #               llabel is always one greater than parent node's llabel
        #       rlabel (right label) is enumerated postorder, so last child's
        #               rlabel is always one less than parent node's rlabel
        #       a node's children always have:
        #               child.llabel > node.llabel
        #               and child.rlabel < node.rlabel
        #       a node's ancestors always have:
        #               ancestor.llabel < node.llabel
        #               and ancestor.rlabel > node.rlabel
        #
        #       inserting nodes in a nested set tree requires renumbering,
        #       but this module does not allow modification of stored objects.
        #
        # An alternate labeling scheme, assigning "pre" and "post"
        # values from independent sequences space makes prettier
        # pictures when the labels are used as X and Y coordinates is
        # described in "Accelerating XPath Location Steps" by Torsten Grust
        #   ACM SIGMOD June 2002, Madison Wisconsin.
        #   http://www-db.informatik.uni-tuebingen.de/files/
        #           research/pathfinder/publications/xpath-accel.pdf
        # However the resulting tables require additional checks
        # to limit axis searches.

        self.nodes = self.conn.table("nodes")
        self.nodes.add_column("id", "INT32", index=True)
        self.nodes.add_column("node", "INT32", primary=True, auto_inc=True)
        self.nodes.add_column("parent", "INT32")
        self.nodes.add_column("type", "CHAR")
        self.nodes.add_column("idx", "TEXT") # was 'key'
        self.nodes.add_column("value", "TEXT")
        self.nodes.add_column("lleft", "INT24")
        self.nodes.add_column("lright", "INT24")
        self.nodes.create()

    def debug(self, value=1):
        """modify debug setting"""
        jsam.JSAM.debug(self, value)
        if self.conn:
            # pass down to JSDBI object
            self.conn.debug = value

    def begin(self):
        """begin a JSAM transaction"""
        jsam.JSAM.begin(self)
        return self._begin(True)

    def _begin(self, assert_unfrozen=False):
        """Freeze database/start transaction"""
        # NOT THREAD SAFE!
        if assert_unfrozen and self.database_frozen > 0:
            raise JSONSQLFrozenError()
        self.database_frozen += 1
        if self.database_frozen == 1:
            self.conn.begin()

    def commit(self):
        """commit transaction"""
        jsam.JSAM.commit(self)
        return self._commit()

    def _commit(self):
        """INTERNAL: commit nested transaction"""
        # NOT THREAD SAFE!
        self._assert_frozen()
        self.database_frozen -= 1
        if self.database_frozen == 0:
            self.conn.commit()

    def rollback(self):
        """rollback the transaction in progress (ends transaction)"""
        jsam.JSAM.rollback(self)
        if self.database_frozen != 0:
            self.conn.rollback()
            self.database_frozen = 0

    def _remove(self, oid):
        """INTERNAL: remove record 'oid' from store"""
        # XXX assert_frozen?
        self.conn.execute("DELETE FROM nodes WHERE id = %s", (oid,))

    def remove(self, oid):
        """remove object with id 'oid' from store"""
        jsam.JSAM.remove(self)
        # only one SQL statement, so no transaction needed, but we call
        # _begin(True) to assert user is calling us in a clean state
        self._begin(True)
        try:
            self._remove(oid)
        finally:
            self._commit()

    def put(self, oid, obj, refs=False):
        """Store a JSON obj in database as record 'oid'
           if refs is True, detect references to shared (sub)objects"""
        class Label(object):
            """helper for store2: generates a label stream.
                Need class because inner scope (function)
                cannot modify variable from an outer scope???"""
            def __init__(self):
                self.nextlabel = 0
            def next(self):
                """return next label"""
                tmp = self.nextlabel
                self.nextlabel += 1
                return tmp

        def store2(parent, objkey, obj):
            """recursive worker function for 'store'"""

            def putnode(parent, ntype, key, value, lleft, lright):
                """helper for store2: insert a node and return node number"""
                stmt = "INSERT INTO nodes " + \
                    "(id, parent, type, idx, value, lleft, lright) " + \
                    "VALUES(%s,%s,%s,%s,%s,%s,%s)"
                args = (oid, parent, ntype, key, value, lleft, lright)
                return self.conn.execute_insert(stmt, 'nodes', 'node', args)

            def putlright(node):
                """helper for store2: insert a compound obj's right label"""
                # performed badly on PostgreSQL without id check
                # (was fine under SQLite and MySQL)
                self.conn.execute("UPDATE nodes SET lright = %s " + \
                                      "WHERE id = %s AND node = %s",
                                  (label.next(), oid, node))

            # body of store2

            if isinstance(obj, bool):
                if obj:
                    val = "true"
                else:
                    val = "false"
                putnode(parent, self.BOOL, objkey, val,
                        label.next(), label.next())
            elif isinstance(obj, basestring):
                putnode(parent, self.STR, objkey, obj,
                        label.next(), label.next())
            elif isinstance(obj, (int, long)):
                putnode(parent, self.INT, objkey, obj,
                        label.next(), label.next())
            elif isinstance(obj, float):
                # check if obj.isinteger() ?
                putnode(parent, self.FLOAT, objkey, obj,
                        label.next(), label.next())
            elif isinstance(obj, dict):
                if refs and id(obj) in nodes:
                    putnode(parent, self.REF, objkey, nodes[id(obj)],
                            label.next(), label.next())
                else:
                    node = putnode(parent, self.OBJECT, objkey, len(obj),
                                   label.next(), -1)
                    for key in obj.keys():
                        store2(node, key, obj[key])
                    # update "right" label after children stored
                    putlright(node)
                    if refs:
                        nodes[id(obj)] = node
            elif isinstance(obj, list): # handle tuple too?
                if refs and id(obj) in nodes:
                    putnode(parent, self.REF, objkey, nodes[id(obj)],
                            label.next(), label.next())
                else:
                    node = putnode(parent, self.ARRAY, objkey, len(obj),
                                   label.next(), -1)
                    for index in xrange(0, len(obj)):
                        store2(node, index, obj[index])
                    # update "right" label after children stored
                    putlright(node)
                    if refs:
                        nodes[id(obj)] = node
            elif obj is None:
                putnode(parent, self.NULL, objkey, None,
                        label.next(), label.next())
            else:
                self.rollback()
                raise TypeError("%r is not JSON serializable" % (obj,))

        # body of put():
        jsam.JSAM.put(self, oid, obj)
        # get a fresh label stream
        label = Label()
        # if handling loops/copies, create memo dict
        if refs:
            nodes = dict()

        # start a transaction -- legal within user transaction
        self._begin()
        try:
            self._remove(oid)
            # new 2/27/2009: store oid for root's key
            store2(0, oid, obj)
            # XXX would be lovely to use nested transactions to back out remove
            # if store2 fails!!!

            # XXX just back out everything, raise exception if store2 fails???
        finally:
            self._commit()

    def retrieve_query(self, query, query_args):
        """INTERNAL: Retrieve a stored JSON object
           given an SQL query WHERE clause and query_args tuple"""

        if self._debug:
            print "retrieve_query:", query, query_args
        self.conn.execute("SELECT node, parent, type, idx, value FROM " + \
                              "nodes WHERE %s ORDER BY node" % query,
                          query_args)
        nodes = {}
        first = None

        def putnode(node, parent, key, value):
            """helper for retrieve_query(): store new node in nodes list;
                if parent known, point them to new node"""
            nodes[node] = value
            if parent in nodes:
                # XXX sigh: lists don't auto-expand
                if isinstance(nodes[parent], list):
                    nodes[parent].append(value)
                else:
                    nodes[parent][key] = value

        # body of retrieve_query()
        for (node, parent, ntype, key, value) in self.conn.iter():
            if ntype == self.OBJECT:
                putnode(node, parent, key, {})
            elif ntype == self.ARRAY:
                putnode(node, parent, key, [])
            elif ntype == self.STR:
                putnode(node, parent, key, value)
            elif ntype == self.INT:
                putnode(node, parent, key, int(value)) # handles longs too!
            elif ntype == self.FLOAT:
                putnode(node, parent, key, float(value))
            elif ntype == self.BOOL:
                putnode(node, parent, key, value == "true")
            elif ntype == self.NULL:
                putnode(node, parent, key, None)
            elif ntype == self.REF:
                putnode(node, parent, key, nodes[value])
            else:
                raise JSONSQLBadDataError(ntype)
            if first is None:
                first = nodes[node]

        if self._debug:
            print "retrieve_query returns:", first
        return first

    def get(self, oid):
        """retrieve object with id 'oid'"""
        return self.retrieve_query("id = %s", (oid,))

    def _assert_frozen(self):
        """INTERNAL: raise exception if not frozen"""
        if not self.database_frozen:
            raise JSONSQLNotFrozenError()

    def collect(self, query):
        """execute a Collection query"""
        jsam.CollectionJSAM.collect(self)
        import jsonsqlcollection
        # XXX keep reference to package?
        return jsonsqlcollection.collect(query, self)

    def xpath(self, path, params=(), **kws):
        """execute an XPath query"""
        jsam.XPathJSAM.xpath(self)
        import jsonsqlxpath
        # XXX keep reference to package?
        return jsonsqlxpath.xxpath(self,  path, params, **kws)

    def close(self):
        """USER: Close the Store"""
        self.conn.close()
        del self.conn

    #### Utilities for jsonsqlcollection and jsonsqlxpath

    def _select_nodes(self, where, vals):
        """INTERNAL: perform a query and return 'node fields' tuples necessary
           to identify an object's children or parents"""
        self._assert_frozen()
        self.conn.execute("SELECT %s FROM nodes WHERE %s" % \
                                (NODE_FIELDS, where), vals)
        return self.conn.fetchall()

    def select_parents(self, vals, limit=""):
        """INTERNAL: return list of 'node fields' tuples for parent nodes"""
        return self._select_nodes("id = %s AND lleft < %s AND lright > %s" + \
                                limit, vals)

    def retrieve_tree(self, node):
        """INTERNAL: take 'node fields' tuple and retrieve object.
           select_nodes/select_parents and retrieve tree sequences
           MUST be called on a frozen database to ensure 'repeatable reads'"""
        self._assert_frozen()
        return self.retrieve_query("id = %s AND " + \
                                    "lleft >= %s AND lright <= %s", node)

    def retrieve_key_path(self, node):
        """INTERNAL: take 'node fields' tuple and retrieve key list.
           MUST be called on a frozen database to ensure 'repeatable reads'"""
        self._assert_frozen()
        self.conn.execute("SELECT idx FROM nodes" + \
                        " WHERE id = %s AND" + \
                        " lleft <= %s AND lright >= %s ORDER BY node", node)
        tt = self.conn.fetchall()
#       print tt
        return [x for x, in tt]

NODE_FIELDS_LIST = ['id', 'lleft', 'lright']

# for _select_nodes, select_parents, retrieve_tree
NODE_FIELDS = ", ".join(NODE_FIELDS_LIST)

# preformat check for leaf nodes
LEAF_CHECK = " type != '%s' AND type != '%s'" % \
                        (JSONSQL.ARRAY, JSONSQL.OBJECT)

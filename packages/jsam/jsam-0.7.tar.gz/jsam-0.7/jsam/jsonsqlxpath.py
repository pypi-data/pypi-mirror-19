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

"""Perform XPath-like queries on a JSONSQL database;

Takes XPath strings (parsed by xparse) or p4j method chained objects
"""

### improve generated query indentation

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.41 $"

import jsonsql
import xpath

import p4j

AXES = {
    "ancestor" :
        "%(NEW)s.id = %(OLD)s.id AND " + \
        "%(NEW)s.lleft < %(OLD)s.lleft AND %(NEW)s.lright > %(OLD)s.lright",
    "ancestor-or-self" :
        "%(NEW)s.id = %(OLD)s.id AND " + \
        "%(NEW)s.lleft <= %(OLD)s.lleft AND %(NEW)s.lright >= %(OLD)s.lright",
    "child" :
        "%(NEW)s.parent = %(OLD)s.node",
    "descendant" :
        "%(NEW)s.id = %(OLD)s.id AND " + \
        "%(NEW)s.lleft > %(OLD)s.lleft AND %(NEW)s.lright < %(OLD)s.lright",
    "descendant-or-self" :
        "%(NEW)s.id = %(OLD)s.id AND " + \
        "%(NEW)s.lleft >= %(OLD)s.lleft AND %(NEW)s.lright <= %(OLD)s.lright",
    "following" :
        "%(NEW)s.id = %(OLD)s.id AND %(NEW)s.lleft > %(OLD)s.lright",
    "following-sibling" :
        "%(NEW)s.parent = %(OLD)s.parent AND %(NEW)s.lleft > %(OLD)s.lright",
    "parent" :
        "%(NEW)s.node = %(OLD)s.parent",
    "preceeding" :
        "%(NEW)s.id = %(OLD)s.id AND %(NEW)s.lright < %(OLD)s.lleft",
    "preceeding-sibling" :
        "%(NEW)s.parent = %(OLD)s.parent AND %(NEW)s.lright < %(OLD)s.lleft",
    # Not in XPath, but JSON objects are not ordered!!
    "sibling" :
        "%(NEW)s.parent = %(OLD)s.parent AND %(NEW)s.node != %(OLD)s.node"
}

class SubQuery(object):
    """a SubQuery collects fragments of an SQL query:
       1. the query string for the WHERE clause
       2. args to be substituted
       3. table names for the FROM clause"""

    def __init__(self, xpq):
        """'xpq' is parent XPathQuery"""
        self.xpq = xpq
        self.qstr = ""
        self.args = []
        self.tables = []

    def new_table_name(self):
        """add and return name for a new context node table instance"""
        # get new alias for nodes table unique within entire query
        table_name = self.xpq.new_table_name()
        self.tables.append("nodes %s" % table_name)
        return table_name

    def append(self, qstr, args=None, opr=None, tables=None):
        """append a new fragment to the query
           'op' is optional operator (ie; AND or OR)
           'qstr' is query string
           'args' is optional argument list
           'tables' is optional tables list"""
        if self.qstr:
            if opr:
                self.qstr += " %s" % opr
            self.qstr += "\n\t" # XXX indent
        self.qstr += qstr
        if args:
            self.args += args
        if tables:
            self.tables += tables

    def wrap(self, format):
        """wrap subquery string in another construct (like parens)"""
        self.qstr = format % self.qstr

    def __repr__(self):
        """make SubQuery object printable for debugging"""
        return '<SQ at %#x """%s""" args: %s tables: %s>' % \
            (id(self), self.qstr.replace('\n\t', ' '), self.args, self.tables)

class XPathQuery(object):
    """Class to generate and execute SQL code, given an
       XPath Abstract Syntax Tree"""

    def __init__(self, path, params, show_id=True):
        self.next_table_number = 0
        self.params = params
        # make object id visible as first path element
        self.show_id = show_id
        self.name, self.subq = self.path(path, None)

    def new_table_name(self):
        """return new table name for a node context"""
        name = "n%d" % self.next_table_number
        self.next_table_number += 1
        return name

    def append(self, qstr, arg=None):
        """append query string and args"""
        self.subq.append(qstr, [arg] )

    def abs(self, steps):
        """start an absolute location path '/....'"""
        subq = SubQuery(self)
        table = subq.new_table_name()
        subq.append("%s.parent = 0" % table)

        # crock to handle leading /id
        # MODIFIES REFERENCED LIST! handle in parser?
        # just consume the step here??
        if self.show_id and len(steps) > 0 and steps[0][0] == 'child':
            # root objects have ID in idx field
            # XXX need to tweak other axis types as well????
            #     descendant => descendant-or-self ??
            steps[0] = ('self', steps[0][1], steps[0][2])

        return (table, subq)

    def path(self, path, context=None):
        """path is tuple (path_type, step_list)
            path_type is one of 'abs', 'aalp', 'rel'
            step_list is list of 3-tuples: (axis, node_test, predicate_list)
           context is name of SQL context node table
           returns (node_name, SubQuery)"""

        path_type, steps = path

        # context is context node (name of table) for the first step
        # subq is SubQuery() to apply steps to
        if path_type == 'abs':
            context, subq = self.abs(steps)
        elif path_type == 'aalp':
            # abbreviated absolute location path '//....'
            subq = SubQuery(self)
            context = subq.new_table_name()
        elif path_type == 'rel':
            if context:
                # in a predicate, use current step as context
                # use provided context
                subq = SubQuery(self)
            else:
                # at top level: treat as absolute?
                context, subq = self.abs(steps)
        else:
            raise UnknownNodeTypeError(path_type)

        for step in steps:
            axis, node_test, predicates = step

            # new is context node generated by axis
            if axis == "self":
                new = context
            else:
                new = subq.new_table_name()
                nodes = { 'OLD': context, 'NEW': new }
                subq.append(AXES[axis] % nodes, opr="AND")

            # handle node test "functions" here
            if node_test != '*':
                subq.append("%s.idx = %%s" % new, [node_test], opr="AND")

            if predicates:
                for pred in predicates:
                    # print "pred %s | %s", (pred, new)
                    _, subq2 = self.eval(pred, new)
                    # print " pred => %s | %s" % (n, subq2)
                    # perform subquery?
                    #   (SELECT n.value FROM subq.tables
                    #    WHERE subq.qstr LIMIT 1) IS NOT NULL ??
                    subq.append("(%s)" % subq2.qstr, subq2.args,
                                opr="AND", tables=subq2.tables)

            # next step uses this step as context
            context = new
        return (context, subq)

    def eval(self, expr, node):
        """evaluate predicate 'expr' with context node 'node'
           return (name, SubQuery)"""
        # print "eval", expr, node
        opr = expr[0]
        if opr == 'and':
            subq = SubQuery(self)
            # print ">>>", expr
            for term in expr[1]:
                # print ">>>>", term
                context, subq2 = self.eval(term, node)
                # append parenthesized SubQuery
                # XXX wrap in EXISTS(SELECT ... WHERE ....)????
                subq.append("(%s)" % subq2.qstr, subq2.args,
                            opr=opr, tables=subq2.tables)
            return (context, subq)
        elif opr == 'or':
            # implement OR using EXISTS(SELECT ... UNION SELECT ... LIMIT 1)
            # Idea from "Query Rewrite for XML in Oracle XML DB"
            #  Muralidhar Krishnaprasad, Zhen Hua Liu, Anand Manikutty,
            #  James W. Warner, Vikas Arora, Susan Kotsovolos
            # http://www.vldb.org/conf/2004/IND5P4.PDF
            # http://www.oracle.com/technology/tech/xml/xquery/pdf/
            #           vldb04-814-XMLRewrite-in-OracleXMLDB.pdf
            # http://www.oracle.com/technetwork/database/features/xmldb/
            #           vldb04-814-xmlrewrite-in-oraclexmld-133185.pdf
            # Proceedings of the 30th Annual International Conference
            # on Very Large Data Bases. Toronto, Canada on Aug/Sep 2004.
            # *AND* Kevin Fitzgerald, who first mentioned using a UNION SELECT!
            subq = SubQuery(self)
            # print ">>>", expr
            union = ''
            for term in expr[1]:
                context, sq2 = self.eval(term, node)
                subq.append("%sSELECT NULL FROM %s WHERE\n\t%s" % \
                             (union, ", ".join(sq2.tables), sq2.qstr),
                         sq2.args)
                union = "\t\tUNION "
            subq.wrap("EXISTS(%s LIMIT 1)") # is LIMIT needed?
            return (context, subq)
        elif opr in ['abs', 'aalp', 'rel']:
            # existential test... use EXISTS(.... LIMIT 1)?
            return self.path(expr, node)
        elif opr in ['>=', '>', '<', '<=', '=', '!=', 'like', 'regexp']:
            # LHS (expr[1]) must be a path (eval returns a table/variable)
            context, subq = self.eval(expr[1], node)
            # table name and operator must be interpolated here
            # RHS (expr[2]) is currently always a constant or variable ref
            # XXX allow path [!]= path (compare p1.node to p2.node)
            val = expr[2]
            # handle $var -- fetch from parameters (list, tuple or dict)
            if val[0] == '$':
                index = val[1:]
                # wrap in try, throw a JSONSQLXPath based exception? 
                if isinstance(self.params, (list, tuple)):
                    val = self.params[int(index)]
                else:
                    val = self.params[index]
            subq.append("%s.value %s %%s" % (context, opr), [val], opr="AND")
            return (context, subq)
        elif opr == 'not':
            subq = SubQuery(self)
            # print ">>>", expr
            context, sq2 = self.eval(expr[1], node)
            subq.append("SELECT NULL FROM %s WHERE\n\t%s" % \
                            (", ".join(sq2.tables), sq2.qstr), sq2.args)
            subq.wrap("NOT EXISTS(%s LIMIT 1)") # is LIMIT needed?
            return (context, subq)
###
        raise UnknownNodeTypeError(opr)

    def makequery(self, fields):
        """return state formatted as a complete SQL query returning 'fields'"""

        comma_space = ", "
        select = comma_space.join([ "%s.%s" % (self.name, f) for f in fields])
        tables = comma_space.join(self.subq.tables)

        # dist = "DISTINCT "
        dist = ""
        return ("SELECT\t%s%s\nFROM\t%s\nWHERE\t%s;" %
                (dist, select, tables, self.subq.qstr))

    def query(self, qjsam, output, debug=0):
        """execute SQL query for this object against jsonsql jsam 'qjsam'
        'output' is an output type from class Out"""

        if not isinstance(qjsam, jsonsql.JSONSQL):
            raise JSONSQLXPathBadJSAM()

        if output == xpath.Out.IDS:
            qqq = self.makequery(['id'])
#           if debug: print qqq
            qjsam.conn.execute(qqq, self.subq.args, debug=debug)
            results = [x[0] for x in qjsam.conn.iter()]
        else:                   # OBJS or PATHS
            qqq = self.makequery(jsonsql.NODE_FIELDS_LIST)
#           if debug: print qqq
            results = []
            # enter transaction to ensure "repeatable reads"
            qjsam.begin()
            # "try/finally" to avoid leaving database frozen
            try:
                # must be called after qjsam.begin():
                qjsam.conn.execute(qqq, self.subq.args, debug=debug)
                nodes = qjsam.conn.fetchall()
                if output == xpath.Out.OBJS:
                    for node in nodes:
                        # retrieve object given "NODE_FIELDS" tuple
                        tree = qjsam.retrieve_tree(node)
                        results.append(tree)
                elif output == xpath.Out.PATHS:
                    for node in nodes:
                        # get path as list
                        path = qjsam.retrieve_key_path(node)
                        if self.show_id: # make object ID part of path
                            # format as an XPath w/ ID
                            results.append( "/" + "/".join(path))
                        else:
                            # make (id, xpath)
                            results.append(
                                (path[0], "/" + "/".join(path[1:])) )
                else:           # PATHKEYS
                    for node in nodes:
                        # get path as list
                        results.append( qjsam.retrieve_key_path(node) )
            finally:
                qjsam.commit()
        if debug:
            print results
            print '---'
        return results

class JSONSQLXPathError(Exception):
    """base class for jsonsqlxpath exceptions"""

class JSONSQLXPathInternalError(JSONSQLXPathError):
    """base class for internal errors"""

class UnknownNodeTypeError(JSONSQLXPathInternalError):
    """INTERNAL Error: unknown node type"""

class JSONSQLXPathBadJSAM(JSONSQLXPathError):
    """JSAM doesn't support SQL"""

def xxpath(qjsam, path, params=(), output=xpath.Out.OBJS, debug=0, **kws):
    """execute XPath string 'path' against jsonsql jsam 'qjsam'"""
    if debug:
        print "==== xxpath", path

    # NOT SQL SPECIFIC: pull up to xpath.py?
    if isinstance(path, basestring):
        import xparse           # XPath parser
        parser = xparse.XPath(xparse.XPathScanner(path))
        ast = parser.Start()    # produce AST
    elif isinstance(path, p4j.Path):
        # allow Predicate?
        ast = path._tup()

    if debug:
        print ast

    # convert AST into SQL
    xpq = XPathQuery(ast, params, **kws)
    # execute SQL
    return xpq.query(qjsam, output, debug)

def make_indices(jsp):
    """add additional indices to database"""
    # try speeding things up
    jsp.nodes.add_index("parent")
    jsp.nodes.add_index("lleft")
    jsp.nodes.add_index("lright")

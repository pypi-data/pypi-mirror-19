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

"""Implement Collection interface for JSONSQL"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.23 $"

import collection
import jsonsql

def collect(query, jsql):
    """execute a Collection query object 'query' against jsonsql store 'jsql'"""

    # list of triples: (where, vals, keep/drop)
    query_list = []
    lastleaf = False
    for node in query.nodes:
        qstr = ""
        vals = []

        if node.key:
            qstr += "idx = %s"
            vals.append(node.key)

        if node.value:
            if node.match not in jsql.conn.operators:
                raise collection.UnknownMatchOpError(node.match)
            if qstr:
                qstr += " AND"
            (matchop, func) = jsql.conn.operators[node.match]
            qstr += " value " + matchop + " AND" + jsonsql.LEAF_CHECK
            vals.append(func(node.value))
            lastleaf = True
        else:
            lastleaf = False

        query_list.append( (qstr, vals, node.keep) )

    sel = "SELECT"
    if len(query_list) > 0:
        # remove last term from query_list
        qstr, vals, keep = query_list.pop()
        where = " WHERE " + qstr
    else:
        # empty node list
        where = ""
        vals = []
        keep = True

    if query.get_count():
        sel += " COUNT("
    if query.get_distinct():
        sel += " DISTINCT"

    if query.out == collection.Output.IDS or \
            query.out == collection.Output.TREES:
        sel += " id"
    else:
        # output not IDS or TREES
        if not keep:
            raise collection.NeedKeepError()

        if query.out == collection.Output.KEYS:
            sel += " idx"
            if query.leafkeys:
                if where:
                    where += " AND"
                else:
                    where += " WHERE "
                where += jsonsql.LEAF_CHECK
        elif query.out in (collection.Output.VALUES, collection.Output.IDVALUE,
                           collection.Output.IDKEYVALUE):
            if not keep:
                raise collection.NeedKeepError()
            if query.out == collection.Output.VALUES:
                sel += " value"
            elif query.out == collection.Output.IDVALUE:
                sel += " id, value"
            else:
                sel += " id, idx, value"
            if not lastleaf:
                if where:
                    where += " AND"
                else:
                    where += " WHERE "
                where += jsonsql.LEAF_CHECK
        else:   # PATHS, PARENT, SUBTREES
            sel += ' ' + jsonsql.NODE_FIELDS
        # output not IDS or TREES
    if query.get_count():
        sel += " )"
    sel += " FROM nodes "
    if keep:
        sel += where
    else:
        sel += " WHERE id NOT IN (SELECT id FROM nodes %s)" % where
        # final "drop" was showing top level object "key":
        sel += " AND" + jsonsql.LEAF_CHECK

    for where, args, keep in query_list:
        sel += " AND id"
        if not keep:
            sel += " NOT"
        sel += " IN (SELECT id FROM NODES WHERE %s)" % where
        vals += args

    if query.get_order() != 0:
        sel += " ORDER BY"
        if query.out == collection.Output.KEYS:
            sel += " idx"
        elif query.out == collection.Output.VALUES:
            sel += " value"
        else:
            sel += " id"
        if query.get_order() < 0:
            sel += " DESC"

    if query.get_limit() is not None:
        sel += " LIMIT %d" % query.get_limit()
        if query.get_offset() is not None:
            sel += " OFFSET %d" % query.get_offset()

    if query.out in (collection.Output.IDS,
                 collection.Output.KEYS, collection.Output.VALUES):
        # simple scalar outputs
        jsql.conn.execute(sel, vals)
        ret = [x for x, in jsql.conn.iter()]
        return ret

    if query.out in (collection.Output.IDVALUE, collection.Output.IDKEYVALUE):
        # tuple outputs
        jsql.conn.execute(sel, vals)
        ret = list(jsql.conn.iter())
        return ret

    if query.out == collection.Output.TREES:
        jsql.conn.execute(sel, vals)
        # fetch everything to avoid needing second cursor
        ids = [x for x, in jsql.conn.iter()]
        return [jsql.get(x) for x in ids]

    if query.out not in (collection.Output.PATHS, collection.Output.PARENT,
                     collection.Output.SUBTREES):
        raise collection.UnknownOutputError()

    # two-step required (involving node labels), start transaction!!!
    jsql.begin()

    # "try/finally" to avoid leaving database frozen
    try:
        jsql.conn.execute(sel, vals)

        # XXX fetch everything to avoid needing second cursor
        nodes = jsql.conn.fetchall()

        ret = []
        if query.out == collection.Output.PATHS:
            for node in nodes:
                path = jsql.retrieve_key_path(node)
                # return (id, [keys]) tuple
                ret.append( (node[0], path[1:]) )
        elif query.out == collection.Output.PARENT:
            for node in nodes:
                if isinstance(query.parent, int):
                    # if query.parent >= 0, use query LIMIT & OFFSET:
                    # XXX not tested! could be off by one?!  need ORDER BY??
                    if query.parent >= 0:
                        # use str(x) so debug works!
                        parent_node = jsql.select_parents(
                            node + (str(query.parent),),
                            limit="LIMIT 1 OFFSET %s")[0]
                    else:
                        # negative parent index: return node location
                        # information for all parent nodes, and index
                        parent_node = jsql.select_parents(node)[query.parent]
                else:
                    # query.parent is string:
                    # return node location information for first parent
                    # with matching key.  Order by left parent (in one
                    # direction or other) to get highest or lowest?
                    parent_node = jsql.select_parents(
                        limit="LIMIT 1",
                        args=(node + (query.parent,)))[0]
                tree = jsql.retrieve_tree(parent_node)
                ret.append(tree)
        elif query.out == collection.Output.SUBTREES:
            for node in nodes:
                tree = jsql.retrieve_tree(node)
                ret.append(tree)
        else:
            raise collection.UnknownOutputError()
    finally:
        jsql.commit()

    return ret

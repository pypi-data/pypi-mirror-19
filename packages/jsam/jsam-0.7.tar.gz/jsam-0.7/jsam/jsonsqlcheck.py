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
(start of) jsonsql database checker
does not attempt repair
"""

# started 10/5/2011
__author__ = "Phil Budne"
__revision__ = "$Revision: 1.4 $"

# requires Python 2.6 for namedtuple
#import collections

import jsonsql

COLS = ['node', 'id', 'parent', 'type', 'idx', 'value', 'lleft', 'lright']
LEAF_TYPES = [jsonsql.JSONSQL.STR,
              jsonsql.JSONSQL.INT,
              jsonsql.JSONSQL.FLOAT,
              jsonsql.JSONSQL.BOOL,
              jsonsql.JSONSQL.NULL,
              jsonsql.JSONSQL.REF]

def checkdb(url):
    c = url.conn

    root_node_by_id = {}
    nodes = {}
    children_by_node = {}

    c.execute("select %s from nodes order by node;" % ",".join(COLS))

    # want Python 2.6 "namedtupple"
    class Node(object):
        __slots__ = COLS
        def __init__(self, tup):
            i = 0
            for name in COLS:
                setattr(self, name, tup[i])
                i += 1

    leaves = 0
    bad_value = 0
    containers = 0
    container_lengths = 0
    errors = 0
    for tup in c.iter():
        node = Node(tup)
        nodes[node.node] = node

        if node.parent == 0:
            root_node_by_id[node.id] = node
            if node.lleft != 0:
                print "root node", node.id, "id", node.id, "lleft", node.lleft
                errors += 1
            # XXX enforce type == OBJECT?
            # XXX check idx == node.id
        else:
            if node.lleft == 0:
                print "node", node.node, "id", node.id, "parent", node.parent,\
                    "lleft", node.lleft
                errors += 1

            # other siblings seen before
            if node.parent in children_by_node:
                c = children_by_node[node.parent]
                left_sib = c[-1]
                if node.lleft <= left_sib.lright:
                    print "node", node.node, "bad lleft"
                    errors += 1
            else:
                # first child
                if node.parent not in nodes:
                    print "node", node.node, "unknown parent", node.parent
                    errors += 1

                c = children_by_node[node.parent] = []

            c.append(node)
            p = nodes[node.parent]
            if node.lleft <= p.lleft:
                print "node", node.node, "bad lleft"
                errors += 1
            if node.lright >= p.lright:
                print "node", node.node, "bad lright"
                errors += 1

            if node.id != p.id:
                print "node", node.node, "id", node.id, "parent.id", p.id
                errors += 1

            # XXX validate idx against parent type!!

            if node.type in LEAF_TYPES:
                if node.lright != node.lleft + 1:
                    print "node", node.node, "bad leaf"
                    errors += 1

            if node.type == jsonsql.JSONSQL.STR:
                # anything goes? check if valid UTF-8? try unicode(node.value)?
                pass
            elif node.type == jsonsql.JSONSQL.INT:
                if not node.value.isint():
                    print "node", node.node, "bad int"
                    bad_value += 1
            elif node.type == jsonsql.JSONSQL.FLOAT:
                try:
                    x = float(node.value)
                except ValueError:
                    print "node", node.node, "bad float"
                    bad_value += 1
            elif node.type == jsonsql.JSONSQL.BOOL:
                if node.value not in ["true", "false"]:
                    print "node", node.node, "bad bool"
                    bad_value += 1
            elif node.type == jsonsql.JSONSQL.NULL:
                if node.value is not None:
                    print "node", node.node, "bad null!"
                    bad_value += 1
            # ARRAY, OBJECT (value is number of children) -- checked later
            # XXX REF !! (must not point to an ancestor) !!
        # else (node.parent != 0)
        if node.type in LEAF_TYPES:
            leaves += 1
        else:
            containers += 1
            if node.value is not None:
                container_lengths += 1
    # for tup

    # new format, "value" for arrays and objects is number of children
    if container_lengths > 0:
        for node in children_by_node:
            if len(children_by_node[node]) != nodes[node].value:
                print "node", node, "len", len(children_by_node[node]), \
                    nodes[node]
                errors += 1

        if containers != container_lengths:
            print containers, "containers", container_lengths, "container_lengths"
            errors += 1

    print "==== summary ===="
    print len(root_node_by_id), "objects,", len(nodes), "nodes,", errors, "errors"
    print leaves, "leaves,", bad_value, "with bad value"
    print containers, "containers,", container_lengths, "with length"

    return errors == 0 and bad_value == 0

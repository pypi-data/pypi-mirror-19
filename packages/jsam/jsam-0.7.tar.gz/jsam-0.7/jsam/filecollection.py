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
Implement 'Collection' interface for File JSON Storage Access Methods
using grep
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.25 $"

import os
import re
import subprocess
try:
    import json                 # 2.6
except ImportError:
    import simplejson as json   # 2.5

import file_jsam
import collection

def _exact(pat):
    """identity function"""
    return pat

def _contains(pat):
    """return grep regular expression for 'contains'"""
    return '.*' + re.escape(pat) + '.*'

def _start(pat):
    """return grep regular expression for 'startswith'"""
    return re.escape(pat) + '.*'

def _end(pat):
    """return grep regular expression for 'endswith'"""
    return '.*' + re.escape(pat)

# all operators can be prefixed w/ 'i' (case independent)
OPERATORS = {
    'exact': ("fgrep", _exact),
    'contains': ("grep", _contains),
    'regex': ("egrep", _exact),
    'startswith': ("grep", _start),
    'endswith': ("grep", _end)
}

def _quote(xstr):
    """return string as it would appear in JSON output"""
    return json.dumps(xstr)

def collect(query, jsam):
    """execute a collection query object for a File-based JSAM"""

    def _filter(key, match, val, files, flags):
        """execute a single FilterNode"""
        if len(files) == 0:
            return []
        if len(files) == 1 and '-h' not in flags and '-l' not in flags:
            files = list(files)
            files.append("/dev/null") # POSIX: force display of filenames
        match = match
        if match[0] == 'i':
            match = match[1:]
            flags.append("-i")
        if match not in OPERATORS:
            raise collection.UnknownMatchOpError()
        (grep, func) = OPERATORS[match]
        search = ""
        if key:
            search += _quote(key)
        search += ": "          # XXX depends on formatting!
        if val:
            search += _quote(func(val))
        cmd = [grep] + flags + [search] + list(files)

        # NOTE! shell=False avoids quoting and security nightmares
        proc = subprocess.Popen(cmd, cwd=jsam.filedir,
                                stdout=subprocess.PIPE, shell=False)
        new = [ line.strip("\n") for line in proc.stdout ]
        del proc
        if jsam._debug > 1:
            print " ".join(cmd), '=>', " ".join(new)
        return new

    # body of collect()
    if query.out not in (collection.Output.IDS, collection.Output.TREES,
                         collection.Output.KEYS, collection.Output.VALUES,
                         collection.Output.IDVALUE, collection.Output.IDKEYVALUE):
        raise collection.UnknownOutputError(query.out)

    if query.full:
        files = [file_jsam.id2name(x) for x in jsam.ids()]
    else:
        # useless, unless an "add" operator implemented
        files = []

    nodes = query.nodes
    final = None
    if query.out not in (collection.Output.IDS, collection.Output.TREES) and \
            len(query.nodes) > 0:
        # NOTE! not pop() don't want to alter query.nodes!!
        final = nodes[-1]
        nodes = nodes[:-1]
        if not final.keep:
            raise collection.NeedKeepError()

    for node in nodes:
        # unless/until "add" operator exists:
        if len(files) == 0:
            break
        new = _filter(node.key, node.match, node.value, files, ["-l"])
        if node.keep:
            files = new
        else:
            files = set(files).difference(new)

    # output (unless/until "add" exists):
    if len(files) == 0:
        query.cache = []
        return query.cache

    flags = []
    if final is not None:
        # have final node
        key = final.key
        match = final.match
        value = final.value

        if query.out in (collection.Output.IDS, collection.Output.TREES):
            flags.append('-l')
            out = [file_jsam.name2id(fname)
                   for fname in _filter(key, match, value, files, flags)]
        else:
            # query.out != IDS or TREES
            def dequote(val):
                # dequote
                """strip quotes (and trailing comma(space)) from JSON values.
                   avoid another re (for speed?).  Could probably be done
                   with a hairy enough re the first time but.... I'd really
                   rather be using SNOBOL patterns
                   (see my 'spipat' package in PyPI)"""

                if val == '':
                    return val
                if val[-2:] == ', ':
                    val = val[:-2]
                elif val[-1] == ',':
                    val = val[:-1]
                if val[0] == '"':
                    val = val[1:-1]
                return val
                # dequote

            # query.out != IDS or TREES
            if query.out == collection.Output.KEYS:
                flags.append('-h')
                if query.leafkeys:
                    exp = re.compile('.*"([^"]*)":\s[^{\[]')
                else:
                    exp = re.compile('.*"([^"]*)":')
                fun = lambda m: m.group(1)
            elif query.out == collection.Output.VALUES:
                flags.append('-h')  # suppress file name
                exp = re.compile('.*":\s*(.*)')
                fun = lambda m: dequote(m.group(1))
            elif query.out == collection.Output.IDVALUE:
                exp = re.compile('(\d+):.*":\s*([^{\[].*)$')
                fun = lambda m: (file_jsam.name2id(m.group(1)), dequote(m.group(2)))
            elif query.out == collection.Output.IDKEYVALUE:
                exp = re.compile('(\d+):\s*"([^"]*)":\s*([^{\[].*)$')
                fun = lambda m: (file_jsam.name2id(m.group(1)),
                                 m.group(2), dequote(m.group(3)))
            else:
                raise collection.UnknownOutputError(query.out)

            out = []
            for line in _filter(key, match, value, files, flags):
                m = exp.match(line)
                if m:
                    out.append( fun(m) )

            # query.out != IDS or TREES
        # have final node
    else:
        out = files

    if query.get_distinct():
        out = list(set(out))

    if query.get_count():
        query.cache = [ len(out) ]
        return query.cache

    if query.get_order() != 0:
        if isinstance(out, set):
            out = list(out)
        out.sort(reverse=query.get_order()<0)

    if query.get_offset() is not None or query.get_limit() is not None:
        out = out[query.get_offset():query.get_limit()]

    if query.out == collection.Output.TREES:
        query.cache = [jsam.get(x) for x in out]
    else:
        query.cache = out
    return query.cache

# a = filter_(True, None, "iexact", "budne", files)
# print filter_(False, "first", "exact", "Phil", a)
# 
# x = filter_(True, "gname", "regex", "ww2009-(cast|crew|team|chorus)", files)
# print len(x)
# 
# x = filter_(True, "gname", "regex", "2008-(cast|crew|team|chorus)", files)
# print len(x)
# 
# x = filter_(True, "gname", "regex", "2007-(cast|crew|team|chorus)", files)
# print len(x)
# 
# x = filter_(True, "gname", "regex", "2006-(cast|crew|team|chorus)", files)
# print len(x)
# 
# x = filter_(True, "gname", "regex", "2005-(cast|crew|team|chorus)", files)
# print len(x)

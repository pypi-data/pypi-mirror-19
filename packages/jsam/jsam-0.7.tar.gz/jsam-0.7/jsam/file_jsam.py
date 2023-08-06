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
JSON Storage Access Method for plain text files.

URL syntax:
        file:///relative_path_to_directory
        file:////absolute_path_to_directory

In case of a typo, the "host" field is also accepted:
        file://relative_path_to_directory

Supported keywords (CGI parameters):
    * keep_backups (keep .bak files): defaults to on
    * sort_keys (write dict keys in sorted order): defaults to on
        (minimizes diffs for source control methods)
"""

# XXX TODO: support subdirs (1000 objects per dir?)
# XXX TODO: support multiple put's per transaction (keep a list)

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.37 $"

import os
try:
    import json                 # >=2.6
except ImportError:
    import simplejson as json   # 2.5

import jsam

# XXX make into a method, use self.__format?
def id2name(oid):
    """Convert object id to file name string"""
    i = int(oid)
    # XXX split into subdirs xxx/xxxyyy
    # XXX need "mkdir" method (for SrcCtrl)
    # return "%d/%03d" % (i/1000, i)
    # XXX use oid.zfill(5)?
    return "%05d" % i

# XXX make into a method?
def name2id(name):
    """Convert file name to object id string"""
    return name.lstrip('0')

class File(jsam.JSAM, jsam.CollectionJSAM):
    """File based Blob Storage Access Method
        Only supports a single 'put' per transaction"""

    __tmp_ext = ".tmp"
    __bak_ext = ".bak"

    def __init__(self, jsurl, user, **kws):
        if os.name != 'posix':
            # see File.commit() method for reasons.
            raise jsam.JSAMPlatformError("File only works on POSIX systems")

        jsam.JSAM.__init__(self, user)
        # pick up file directory from JSURL
        self.filedir = jsurl.path or jsurl.host or ''
        self.attic = os.path.join(self.filedir, ".Attic")
        # True if a file has been "put", but not commit'ed
        # XXX Keep list of uncommited files??
        self.done_put = False

        self.options = {
            'keep_backups': True, # keep backup files
            'sort_keys': True     # output keys in sorted order
        }
        self.options.update(kws)
        self.options.update(jsurl.kws)

        self.path = None
        self.tmpfile = None
        self.bakfile = None

    def id2path(self, oid):
        """INTERNAL: Convert object id to path to file"""
        return os.path.join(self.filedir, id2name(oid))

    def get(self, oid):
        """Retrieve an object by id.
           legal in and outside transactions (but not after a put)"""
        assert not self.done_put
        try:
            jfd = file(self.id2path(oid))
            obj = json.load(jfd)
            jfd.close()
            return obj
        except IOError:
            return None

    def begin(self):
        """Begin a transaction"""
        jsam.JSAM.begin(self)

    def put(self, oid, obj):
        """Store 'obj' with 'oid'
           Must be called in transaction.
           Only a single 'put' may be done per transaction."""

        # take optional indent arg?
        jsam.JSAM.put(self, oid, obj)

        # need two-phase commit to handle multiple files
        assert not self.done_put

        # save for commit/rollback
        self.path = self.id2path(oid)
        self.tmpfile = "%s.%d%s" % (self.path, os.getpid(), self.__tmp_ext)
        self.bakfile = self.path + self.__bak_ext

        # XXX make subdir, if needed!
        jfd = file(self.tmpfile, "w")
        json.dump(obj, jfd, indent=1, sort_keys=self.options['sort_keys'])
        jfd.close()
        self.done_put = True

    def commit(self):
        """Commit the current transaction"""
        jsam.JSAM.commit(self)
        if self.done_put:
            # depends on POSIX hard link & atomic unlink/rename
            # neither of which work on Windoze...
            if self.options['keep_backups'] and os.path.isfile(self.path):
                if os.path.isfile(self.bakfile):
                    os.unlink(self.bakfile)
                # POSIX hard link:
                os.link(self.path, self.bakfile)
            # POSIX rename() removes existing file & renames atomicly;
            os.rename(self.tmpfile, self.path)
            self.done_put = False
        return True

    def rollback(self):
        """Abort the current transaction"""
        jsam.JSAM.rollback(self)
        if self.done_put and os.path.isfile(self.tmpfile):
            os.unlink(self.tmpfile)
        self.done_put = False

    def remove(self, oid):
        """Remove an object by id; not legal in a transaction
           Old files are kept in a .Attic subdirectory"""
        jsam.JSAM.remove(self)
        # XXX just remove if not self.options['keep_backups']:
        if not os.path.isdir(self.attic):
            os.mkdir(self.attic)
        os.rename(self.id2path(id), os.path.join(self.attic, id2name(oid)))

    def ids(self):
        """INTERNAL: Return list of all ids currently in use"""
        # XXX handle subdirs
        # only return names that are made ONLY of digits:
        return [ name2id(f) for f in os.listdir(self.filedir) if f.isdigit()]

    def collect(self, query):
        """Execute collection query"""
        jsam.CollectionJSAM.collect(self)
        import filecollection
        return filecollection.collect(query, self)

def file_jsam_open(jsurl, user):
    """called from JSURL.open() method; user is for log entries""" 
    return File(jsurl, user)

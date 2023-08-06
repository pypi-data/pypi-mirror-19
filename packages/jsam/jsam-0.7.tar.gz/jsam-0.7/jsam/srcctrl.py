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
superclass for command line source control methods

subclass of "file" JSAM
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.25 $"

import os
import os.path

import file_jsam
import jsam

class SrcCtrl(file_jsam.File):
    """Base class for Source Control JSON Storage Access Methods"""

    # override in subclass
    cmds = {}

    def __init__(self, jsurl, user, **kws):
        file_jsam.File.__init__(self, jsurl, user, keep_backups=False, **kws)

        if not user:
            user = os.getenv("USER", "") # XXX POSIX
        self.user = user
        self.args = {"USER": user}
        self.oid = None
        self.new = False

    def _cmd(self, cmdname, oid=None):
        """INTERNAL: method to format and execute commands"""
        if cmdname not in self.cmds:
            return
        if oid is not None:
            self.args["ID"] = file_jsam.id2name(oid)
            self.args["FILE"] = self.id2path(oid)
        cmd = self.cmds[cmdname] % self.args
        ret = os.system(cmd)
        if oid is not None:
            del self.args["ID"]
            del self.args["FILE"]
        if ret != 0:
            print cmdname, cmd, ret
            raise SrcCtrlError(cmdname, cmd, ret)

    def get(self, oid):
        """retrieve an object by id.
           make sure file is the latest version before reading it"""
        # if file exists, update to latest version
        if os.path.isfile(self.id2path(oid)):
            self._cmd("get", oid)
        return file_jsam.File.get(self, oid)

    def put(self, oid, obj):
        """Store 'obj' with id 'oid'
           Must be called in transaction.
           Only a single 'put' may be done per transaction."""
        assert not self.done_put
        self.oid = oid
        self.args["MSG"] = self.user
        # writes .tmp file
        return file_jsam.File.put(self, oid, obj)

    def commit(self):
        """Commit the current transaction"""
        if not self.done_put:
            return

        # if file exists, execute command to lock it:
        if os.path.isfile(self.id2path(self.oid)):
            self._cmd("lock", self.oid)
            self.new = False
        else:
            self.new = True

        # renames .tmp file, clears done_put
        file_jsam.File.commit(self)

        # if new file, add to repository
        if self.new:
            self._cmd("add", self.oid)

        # commit file to repository
        self._cmd("commit", self.oid)

    def rollback(self):
        """Abort the current transaction"""
        # save old done_put
        odp = self.done_put
        file_jsam.File.rollback(self)
        if odp:
            self._cmd("rollback", self.oid)

    def remove(self, oid):
        """Remove an object by id; not legal in a transaction"""
        # bypass File .Attic storage
        jsam.JSAM.remove(self)
        self.args["MSG"] = "removed by user %s" % self.user
        self._cmd("remove", oid)

class SrcCtrlError(jsam.JSAMException):
    """Error from Source Control based JSAM"""
    def __init__(self, cmdname, cmd, status):
        jsam.JSAMException.__init__(self)
        self.cmdname = cmdname
        self.cmd = cmd
        self.status = status

        def __str__(self):
            """string representation of SrcCtrlError"""
            return "%s: %s status %d" % \
                (self.cmdname, self.cmd, self.status)

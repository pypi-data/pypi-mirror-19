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
JSON Storage Access Method for plain text files under RCS source control.

URL syntax:
        rcs:///relative_path_to_directory
        rcs:////absolute_path_to_directory

In case of a typo, the "host" field is also accepted:
        rcs://relative_path_to_directory

An RCS directory will be created if none exists.

rcs is a subclass of SrcCtrl, which is a subclass of File.
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.22 $"

import os.path
import os

import srcctrl
import file_jsam

class RCS(srcctrl.SrcCtrl):
    """Use RCS for blob source control"""
    def __init__(self, jsurl, user, **kws):
        srcctrl.SrcCtrl.__init__(self, jsurl, user, **kws)

        self.rcsdir = os.path.join(self.filedir, "RCS")
        if not os.path.isdir(self.rcsdir):
            os.mkdir(self.rcsdir)       # makedirs?
        self.args["RCSDIR"] = self.rcsdir

        attic = os.path.join(self.rcsdir, ".Attic")
        if not os.path.isdir(attic):
            os.mkdir(attic)     # makedirs?
        self.args["ATTICDIR"] = attic

        # XXX prefix with RCS binary path
        self.args["CO"] = "co"
        self.args["CI"] = "ci"

        # -ko: suppress keyword expansion
        #       operadb (blob v0) depended on expansion for serial numbers!
        # -f: force
        # -q: quiet
        # -l: lock
        # -u: unlock
        checkout_unlocked = "%(CO)s -ko -q -f -u %(FILE)s"
        self.cmds = {
            "get": checkout_unlocked,
            "rollback": checkout_unlocked,

            # checkout locked (if exists):
            "lock": "%(CO)s -ko -q -f -l %(FILE)s",

            # save RCSFILE, remove working file:
            "remove": "mv -f %(RCSFILE)s %(ATTICDIR)s && rm -f %(FILE)s",

            # checkin, leave unlocked:
            # -k means something else!!
            # -t: file description (only used on initial checkin)
            "commit":
                "%(CI)s -q -u -w%(USER)s '-m%(MSG)s' '-t-%(ID)s' %(FILE)s",
        }

    def _cmd(self, cmd, oid=None):
        """INTERNAL: method to format and execute commands"""
        if id is not None:
            self.args["RCSFILE"] = os.path.join(
                self.rcsdir, file_jsam.id2name(oid) + ",v")
        ret = srcctrl.SrcCtrl._cmd(self, cmd, oid)
        if oid is not None:
            del self.args["RCSFILE"]
        return ret

def rcs_jsam_open(jsurl, user):
    """called from JSURL.open() method; user is for log entries""" 
    return RCS(jsurl, user)

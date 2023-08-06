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
JSON Storage Access Method for plain text files under Subversion source control.

NOTE: not tested!

URL syntax:
        svn:///relative_path_to_directory
        svn:////absolute_path_to_directory

In case of a typo, the "host" field is also accepted:
        svn://relative_path_to_directory

The directory must be a checkout of a directory in a Subversion
repository, complete with a .svn directory.

svn is a subclass of SrcCtrl, which is a subclass of File.
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.15 $"

import srcctrl

# NOT TESTED!

class SVN(srcctrl.SrcCtrl):
    """Use a Subversion repository for blob source control.
        /var/db/blobs/NAME/json must be a checkout of the repository"""
    def __init__(self, jsurl, user, **kws):
        srcctrl.SrcCtrl.__init__(self, jsurl, user, **kws)
        self.args["SVN"] = "svn"        # XXX full path?

        commit = "%(SVN)s -q ci -m '%(MSG)s' %(FILE)s"
        self.cmds = {
            # retrieve latest
            "get": "rm -f %(FILE); %(SVN)s -q update %(FILE)s",
            "add": "%(SVN)s -q add %(FILE)s",   # --force?? doesn't take msg
            "commit": commit,
            "rollback": "%(SVN)s -q revert %(FILE)s",
            "remove": "%(SVN)s -q rm %(FILE)s; " + commit
        }

def svn_jsam_open(jsurl, user):
    """called from JSURL.open() method:
       jsurl locates local checkout; user is for log entries""" 
    return SVN(jsurl, user)

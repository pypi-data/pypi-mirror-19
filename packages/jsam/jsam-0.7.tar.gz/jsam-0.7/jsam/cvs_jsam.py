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
JSON Storage Access Method for plain text files under CVS source control.

NOTE: not tested!

URL syntax:
        cvs:///relative_path_to_directory
        cvs:////absolute_path_to_directory

In case of a typo, the "host" field is also accepted:
        cvs://relative_path_to_directory

The directory must be a checkout of a CVS "module",
complete with a CVS directory.

cvs is a subclass of SrcCtrl, which is a subclass of File.
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.14 $"

# NOT TESTED!

import srcctrl

class CVS(srcctrl.SrcCtrl):
    """Use a CVS repository for blob source control.
        /var/db/blobs/NAME/json must be a checkout of the repository"""
    def __init__(self, url, user, **kws):
        srcctrl.SrcCtrl.__init__(self, url, **kws)
        self.args["CVS"] = "cvs"        # XXX full path?

        # retrieve latest
        get = "rm -f %(FILE); %(CVS)s -Q update %(FILE)s",
        commit = "%(CVS)s -Q ci -m '%(MSG)s' %(FILE)s"

        self.cmds = {
            "get": get,
            "add": "%(CVS)s -Q add -m '%(MSG)s' %(FILE)s",
            "commit": commit,
            "rollback": get,
            "remove": "rm -f %(FILE)s; %(CVS)s -Q rm %(FILE)s; " + commit
        }

def cvs_jsam_open(jsurl, user):
    """called from JSURL.open() method; user is for log entries""" 
    return CVS(jsurl, user)

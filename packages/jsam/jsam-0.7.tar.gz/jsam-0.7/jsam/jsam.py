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
Base class for all JSON Storage Access Methods (JSAMs)

The name is a joke on IBM Mainframe data Access Methods
(BDAM, BSAM, VSAM, ISAM, QSAM, BPAM)

Most methods of the JSAM base class just enforce transaction checks.
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.27 $"

class JSAM(object):
    """
    Base class for all JSON Storage Access Methods (JSAMs)
    The name is a joke on IBM Mainframe data Access Methods
    (BDAM, BSAM, VSAM, ISAM, QSAM, BPAM)

    Most methods of the JSAM base class just enforce transaction checks.
    """

    def __init__(self, user):
        self.in_transaction = False
        self.user = user
        self._debug = 0

    # get() legal in or out of transaction.  Here for documentation.
    def get(self, oid):
        """Retrieve object with integer object id 'oid'"""

    def debug(self, value=1):
        """modify debug setting"""
        self._debug = value

    def begin(self):
        """Begin a transaction; The only guarantee is that under
           normal conditions on "commit" object(s) that have been
           successfully "put" will be atomicly replaced with the new
           versions, and that on "rollback" the newly "put" objects will
           be discarded.  No guarantee is made regarding exclusive
           access to the objects."""
        assert not self.in_transaction
        self.in_transaction = True

    def put(self, oid, obj):
        """Store object 'obj' as object number 'oid'.
           Must be called in transaction.
           File based JSAMs only support a single 'put' in a transaction."""
        assert self.in_transaction

    def commit(self):
        """Commit the current transaction"""
        assert self.in_transaction
        self.in_transaction = False
        
    def rollback(self):
        """Abort the current transaction; discard any 'puts'"""
        assert self.in_transaction
        self.in_transaction = False
        
    def remove(self):
        """Remove entry; not legal in a transaction"""
        assert not self.in_transaction

    def collect(self):
        """Execute collection query"""
        raise JSAMNotImplementedError()

    def xpath(self):
        """Execute XPath query"""
        raise JSAMNotImplementedError()

    def __del__(self):
        """Handle deletion of JSAM object with a pending transaction"""
        assert not self.in_transaction    # rollback first?

class CollectionJSAM(object):
    """mixin for JSAMs implementing Collections"""

    def collect(self):
        """Execute collection query"""
        assert not self.in_transaction

class XPathJSAM(object):
    """mixin for JSAMs implementing XPath"""

    def xpath(self):
        """Execute XPath query"""
        assert not self.in_transaction

class JSAMException(Exception):
    """Exception: base class for all JSAM Exceptions"""

class JSAMNotImplementedError(JSAMException):
    """Exception: JSAM method not implemented"""

class JSAMPlatformError(JSAMException):
    """Exception: JSAM not supported on this platform"""

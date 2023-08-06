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
Parse and Open a JSON Storage Access Method URL

URL/URI syntax cribbed from Django, which copied SQLAlchemy

scheme://username:password@host:port/name?param=val&...#fragment

See documentation for module named jsam.SCHEME_jsam for information
on the interpretation of fields for a given URL scheme/access method.
"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.18 $"

import sys
import urlparse
import urllib

def parse(urlstr):
    """parse JSON Storage Access Method URL"""

    # urlparse "knows" things about URL schemes,
    # so tell it this is an HTTP URL:
    scheme, rest = urlstr.split(':', 1)
    arg = "http:" + rest
    url = urlparse.urlparse(arg)

    kws = {}
    if url.query:
        for keyval in url.query.split('&'):
            key, val = keyval.split('=', 1)
            kws[key] = urllib.unquote_plus(val)
    return JSURL(scheme=scheme, host=url.hostname, user=url.username,
                 passwd=url.password, port=url.port, path=url.path,
                 frag=url.fragment, kws=kws)

def open_url(urlstr, user=None):
    """parse and open a JSAM given JSON Storage Access Method URL string"""
    urlobj = parse(urlstr)
    return urlobj.open(user)

# make subclass of urlparse.ParseResult??
class JSURL(object):
    """A parsed JSON Access Method URL"""
    def __init__(self, scheme, host=None, user=None,
                 passwd=None, port=None, path=None, frag=None, kws=None):
        self.scheme = scheme
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.path = path[1:] if path else None
        self.frag = frag
        self.kws = kws

    def __str__(self):
        # use urlunparse??
        ret = [ self.scheme, "://"]
        if self.user or self.passwd:
            if self.user:
                ret.append(self.user)
            if self.passwd:
                ret.append(":")
                ret.append(self.passwd)
            ret.append("@")
        if self.host:
            ret.append(self.host)
        if self.port is not None:
            ret.append(":")
            ret.append(str(self.port))
        if self.path or self.kws:
            ret.append("/")
        if self.path:
            ret.append(self.path)
        if self.kws:
            ret.append("?")
            # sort kws list?
            keys = self.kws.keys()
            keys.sort()
            ret.append("&".join(["%s=%s" %
                                 (str(k), str(self.kws[k])) for k in keys]))
        if self.frag:
            ret.append("#")
            ret.append(self.frag)
        return ''.join(ret)

    def open(self, user=None):
        """open URL; user is for log entries"""
        # Use setuptools pkg_resources "plugins"? too complex for now.
        modname = 'jsam.%s_jsam' % self.scheme
        __import__(modname)
        module = sys.modules[modname]
        # pointer to jsam.SCHEME_jsam.SCHEME_jsam_open function
        openfunc = getattr(module, self.scheme + "_jsam_open")
        return openfunc(self, user)

if __name__ == "__main__":
    def check_parse(url):
        """check that URL can be parsed, and turned back to the same string"""
        print ">", url
        purl = parse(url)
        print "<", purl
        assert str(purl) == url

    # full monty:
    check_parse('aaa://username:password@host:123/path?p1=v1&p2=v2#fragment')

    # missing bits:
    check_parse('aaa://username@host:123/path?p1=v1&p2=v2#fragment')
    check_parse('aaa://:password@host:123/path?p1=v1&p2=v2#fragment')
    check_parse('aaa://host:123/path?p1=v1&p2=v2#fragment')
    check_parse('aaa://:123/path?p1=v1&p2=v2#fragment')
    check_parse('aaa://host/path?p1=v1&p2=v2#fragment')
    check_parse('aaa://username:password@host/path?p1=v1&p2=v2#fragment')
    check_parse('aaa://username:password@:123/path?p1=v1&p2=v2#fragment')
    check_parse('aaa://host:123')
    check_parse('aaa://host')
    check_parse('aaa://host/path')
    check_parse('aaa://host/?p1=v1&p2=v2#fragment')
    check_parse('aaa:///?p1=v1&p2=v2#fragment')

    # relative local path:
    check_parse('bbb:///rel_local_path')

    # absolute local path:
    check_parse('ccc:////abs_local_path')

#    parse("sqlite:///foo.db").open()
#    parse("sqlite://foo.db").open()
#    parse("sqlite:////foo.db").open()

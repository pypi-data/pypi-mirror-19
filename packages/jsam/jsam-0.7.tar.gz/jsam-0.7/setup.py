#!/usr/bin/env python

import distutils.core
import jsam as module

# * include tests in distribution
# * depend on simplejson if Python < 2.6
# * don't install yapps2.py?
# * check if xpath.py exists, and is newer than xpath.g
#       if not, run yapps2.py

name = module.__name__
version = module.__version__
url_base = "http://www.ultimate.com/phil/python/"
url = url_base + '#' + name
download_url = "%sdownload/%s-%s.tar.gz" % (url_base, name, version)
# extract description and long_description from module __doc__ string
lines = module.__doc__.split("\n")
while len(lines) > 0 and lines[0] == '':
    lines.pop(0)
empty = lines.index('')
descr = '\n'.join(lines[:empty])
long_descr = '\n'.join(lines[empty+1:])

distutils.core.setup(
    name=name,
    version=version,
    description=descr,
    # ReStructuredText: http://docutils.sourceforge.net/rst.html
    long_description=long_descr,
    author="Phil Budne",
    author_email="phil@ultimate.com",
    url=url,
    download_url=download_url,
    packages=['jsam'],
    classifiers=[
        # http://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 3 - Alpha',
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # want 'Topic :: Text Processing :: Markup :: JSON' !
        'Topic :: Text Processing :: Markup'
        ],
      license="GPL",
      platforms = ['POSIX']
)

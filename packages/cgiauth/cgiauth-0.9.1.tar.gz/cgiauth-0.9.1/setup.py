#!/usr/bin/env python

# $Id: setup.py,v 1.13 2010/01/22 22:15:19 phil Exp $

from distutils.core import setup
import cgiauth as module        # for __name__, __version__, __doc__

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

setup(name=name,
      version=version,
      description=descr,
      # ReStructuredText: http://docutils.sourceforge.net/rst.html
      long_description=long_descr,
      author="Phil Budne",
      author_email="phil@ultimate.com",
      url=url,
      download_url=download_url,
      py_modules=['cgiauth'],
      classifiers=[
        # http://pypi.python.org/pypi?:action=list_classifiers
        #'Development Status :: 3 - Alpha',
        "Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      license="GPL",
      platforms = ['Any']
      )

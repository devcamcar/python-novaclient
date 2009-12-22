#! /usr/bin/python

from setuptools import setup
from com.rackspace.cloud.servers.api.client import version

VERSION=version.get_version()
DESCRIPTION='Rackspace Cloud Servers Python API',
LONG_DESCRIPTION="""
"""
CLASSIFIERS = filter(None, map(str.strip,
"""
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines()))

# Only need simplejson if < Python 2.6.  2.6 +, it's included as json
# and the import will be handled properly by our jsonwrapper
import sys
if sys.version_info < (2, 6):
    REQUIRES = "simplejson"
else:
    REQUIRES = ""

#
## Hack to overcome deficiency in setuptools -- inability to exclude specific
## files...
##
## modify build process to exclude specific files from the build
##
## With credit to:
##
## http://xylld.wordpress.com/2009/09/24/python-setuptools-workaround-for-ignore-specific-files/
#

from distutils.command.build_py import build_py
find_package_modules_old = build_py.find_package_modules

def find_package_modules(self, package, package_dir):
    excludes = [
        ('cloudservers','tests','account.py'),
    ]

    modules = find_package_modules_old(self, package, package_dir)
    for pkg, module, fname in excludes:
        if (pkg, module, fname) in modules:
            modules.remove((pkg,module,fname))
            print "excluding pkg = %s, module = %s, fname = %s" % \
                (pkg,module,fname)
    return modules

build_py.find_package_modules = find_package_modules

setup(
    name='cloudservers',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Steve Steiner and Mike Mayo',
    author_email = "ssteinerX@gmail.com and mike.mayo@rackspace.com",
    url='http://www.rackspacecloud.com/',
    license="MIT License",
    packages=['cloudservers', 'cloudservers.shared', 'cloudservers.tests'],
    test_suite = 'nose.collector',
    keywords="cloud cloudservers rackspace on-demand",
    zip_safe=False,
    install_requires=REQUIRES
)

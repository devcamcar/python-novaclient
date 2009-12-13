# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
Constants used across entire Rackspace Cloud Servers Python API.
"""
import datetime

from cloudservers.version import get_version
__version__ = get_version()

user_agent = "python-cloudservers/%s" % __version__

default_authurl =  "https://auth.api.rackspacecloud.com/v1.0"

json_hdrs = {
   "Accept"         :   "application/json",
   "Content-Type"   :   "application/json",
}

xml_hdrs = {
    "Accept"        :   "application/xml",
    "Content-Type"  :   "application/xml",
}

DEFAULT_PAGE_SIZE = 1000
BEGINNING_OF_TIME = datetime.datetime(1969, 12, 31, 17, 0)
def get_version():
    return __version__





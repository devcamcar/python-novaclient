# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
Rackspace Cloud Servers Python API Tests

See README.txt in this directory for further info.

This package tests all of the functionality in the

    RackSpace Cloud Servers Python API

Anything that's in the API that's not tested by this suite should be!

Please file a bug report if you find something untested or find something that
doesn't work as expected.

See BUGREPORTS.txt for the bug reporting procedure.

Thanks!

S
"""

import os
import sys
import unittest

def get_test_account_credentials():
    """
    Get the account credentials to use for testing.  See README.txt for
    details.
    """
    pass
    
try:
    from com.rackspace.cloud.servers.api.client.tests.account import RS_UN, RS_KEY
except ImportError:
    sys.stderr.write(open(os.path.join(os.path.dirname(__file__),"README.txt")).read())
    sys.exit(1)

import com.rackspace.cloud.servers.api.client.shared.cslogging

#----------------------------------------------------------------------------
# Some convenience tags.  Also, coincidentally (!) tests creation of all these
# required classes...
#
# Access in test modules as tests.css, tests.sm, tests.im, etc.
#
# So many, many, many things have to go right at once for this to even get
# started that's it's a pretty big test all by itself.
#----------------------------------------------------------------------------
from com.rackspace.cloud.servers.api.client.cloudserversservice import CloudServersService
css     = cloudServersService   = CloudServersService(RS_UN, RS_KEY)
sm      = serverManager         = css.createServerManager()
im      = imageManager          = css.createImageManager()
fm      = flavorManager         = css.createFlavorManager()
sipgm   = sharedIpGroupManager  = css.createSharedIpGroupManager()


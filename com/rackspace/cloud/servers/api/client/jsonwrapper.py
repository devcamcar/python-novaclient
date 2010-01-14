# Copyright (c) 2010, Rackspace.
# See COPYING for details.


"""
Wrapper around JSON librarirs.  We start trying the JSON library built into
Python 2.6, and fall back to using simplejson otherwise.

NOTE: simplejson is installed if we're not on 2.6+ by our setup.py
"""

try:
    # 2.6 will have a json module in the stdlib
    import json
except ImportError:
    try:
        # simplejson is the thing from which json was derived anyway...
        import simplejson as json
    except ImportError:
        print "No suitable json library found, see INSTALL.txt"
        raise

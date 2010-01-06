import unittest
from nose import SkipTest

# I'll give it a shot.
#
# Here's the test case:
#
#   Get a list of servers at time X.
#
#  An If-modified-Since X should return a 304, not modified response.
#
#  Create a new server.
#
#  Wait until it is built.
#
#  Mark time Y.
#
#  Build another server, wait until it is built.
#
#  Mark time Z.
#
# A conditional get on any value between X and Y should return both new 
# servers.
#
# A conditional get on Z or greater should just the one new server.
#
# A conditional get on any time after Y should return 304, not modified.
#
# Is there anything else that should be added to the test case?
#
# Thanks,
#
#
class TestConditionalGet(unittest.TestCase):
    pass

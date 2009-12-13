import unittest

from nose import SkipTest
from nose.tools import assert_raises

from cloudservers.errors import AuthenticationFailed
from cloudservers.authentication import Authentication

class TestBaseAuthentication(unittest.TestCase):
    # NOTE: This class is never instantiated, no tests necessary
    def test___init__(self):
        # base_authentication = BaseAuthentication(username, api_key, authurl)
        pass # Base class, not called

    def test_authenticate(self):
        # base_authentication = BaseAuthentication(username, api_key, authurl)
        # self.assertEqual(expected, base_authentication.authenticate())
        pass # Base class, not called

class TestAuthentication(unittest.TestCase):
    def test_authenticate(self):
        # authentication = Authentication()
        # self.assertEqual(expected, authentication.authenticate())
        # Get the computeURL and authToken to use for subsequent queries
        auth = Authentication("badname", "really bad key")
        assert_raises(AuthenticationFailed,auth.authenticate)

if __name__ == '__main__':
    unittest.main()

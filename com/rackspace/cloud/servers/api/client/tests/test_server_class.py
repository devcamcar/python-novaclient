# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
Test Server object.  These tests just test the internals of the class itself, 
not the use thereof.
"""

from com.rackspace.cloud.servers.api.client.server import Server
from com.rackspace.cloud.servers.api.client.jsonwrapper import json

from com.rackspace.cloud.servers.api.client.tests.unittest_wrapper \
    import unittest

from com.rackspace.cloud.servers.api.client.tests.shared.printdoc \
    import printdoc

from com.rackspace.cloud.servers.api.client.tests import css, sm, im, fm, sipgm

class ServerClassTestCase(unittest.TestCase):
    """
    Tests server object internals.
    """
    def setUp(self):
        """Create a couple of server objects to play with"""
        self.server0 = Server(name="TestServer0", imageId=1, flavorId=2, \
                    metadata={"meta1":"0meta1 value", "meta2":"0meta2 value"})
        self.server1 = Server(name="TestServer1", imageId=2, flavorId=3)

    def tearDown(self):
        del self.server0
        del self.server1

    @printdoc
    def test_server0(self):
        """Test values of self.server0"""
        s = self.server0    # typing shorthand
        assert s.name == "TestServer0"
        assert s.imageId == 1
        assert s.flavorId == 2
        assert s.metadata["meta1"] == "0meta1 value"
        assert s.metadata["meta2"] == "0meta2 value"

    @printdoc
    def test_readonly(self):
        """
        Verify that Server properties are readonly.
        NOTE: name is mutable unless the Server is attached
              to a ServerManager.
        """
        awbb = "Anything Would Be Bad"
        def _test_set_imageId(o):
            o.imageId = awbb

        def _test_set_flavorId(o):
            o.flavorId = awbb

        def _test_set_metadata(o):
            o.metadata = awbb

        x = AttributeError  # typing shorthand
        self.assertRaises(x, _test_set_flavorId, self.server0)
        self.assertRaises(x, _test_set_imageId,  self.server0)
        self.assertRaises(x, _test_set_metadata, self.server0)

    @printdoc
    def test_asJSON(self):
        """
        Test JSON conversion of servers with and without metadata.
        """
        srvr0Dict = {"server":
                        {
                            "name"      : "TestServer0",
                            "imageId"   : 1,
                            "flavorId"  : 2,
                            "metadata"  : {"meta1":"0meta1 value",
                                           "meta2":"0meta2 value"}
                        }
                    }
        srvr0Json = json.dumps(srvr0Dict)
        self.assertEqual(self.server0.asJSON, srvr0Json)

        srvr1Dict = {"server":
                        {
                            "name"      : "TestServer1",
                            "imageId"   : 2,
                            "flavorId"  : 3,
                            "metadata"  : None
                        }
                    }
        srvr1Json = json.dumps(srvr1Dict)
        self.assertEqual(self.server1.asJSON, srvr1Json)

if __name__ == "__main__":
    unittest.main()

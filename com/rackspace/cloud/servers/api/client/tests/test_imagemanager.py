import unittest
from nose import SkipTest
from nose.tools import assert_equal

import com.rackspace.cloud.servers.api.client.tests as cst
from com.rackspace.cloud.servers.api.client.errors import BadMethodFault

class TestImageManager(unittest.TestCase):
    def test___init__(self):
        # image_manager = ImageManager(cloudServersService)
        raise  SkipTest # TODO: implement your test here

    def test_bad_methods(self):
        f = cst.imageManager
        self.assertRaises(BadMethodFault, f.create, None  )
        self.assertRaises(BadMethodFault, f.remove, None )
        self.assertRaises(BadMethodFault, f.update, None )
        self.assertRaises(BadMethodFault, f.refresh, None )
        self.assertRaises(BadMethodFault, f.wait, None )
        self.assertRaises(BadMethodFault, f.waitT, None, None )
        self.assertRaises(BadMethodFault, f.notify, None, None )
        self.assertRaises(BadMethodFault, f.stopNotify, None, None )

    def test_createEntityListFromResponse(self):
        # image_manager = ImageManager(cloudServersService)
        # self.assertEqual(expected, \
        #               image_manager.createEntityListFromResponse(response))
        raise  SkipTest # TODO: implement your test here

    def test_find(self):
        # image_manager = ImageManager(cloudServersService)
        # self.assertEqual(expected, image_manager.find(id))
        raise  SkipTest # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()

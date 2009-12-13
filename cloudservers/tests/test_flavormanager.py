import unittest
from nose import SkipTest

from cloudservers.flavormanager import FlavorManager
import cloudservers.tests as cst
from cloudservers.errors import BadMethodFault

class TestFlavorManager(unittest.TestCase):
    def test___init__(self):
        # flavor_manager = FlavorManager(cloudServersService)
        pass    # Will get tested by other tests

    def test_bad_methods(self):
        f = cst.flavorManager
        self.assertRaises(BadMethodFault, f.create, None  )
        self.assertRaises(BadMethodFault, f.remove, None )
        self.assertRaises(BadMethodFault, f.update, None )
        self.assertRaises(BadMethodFault, f.refresh, None )
        self.assertRaises(BadMethodFault, f.wait, None )
        self.assertRaises(BadMethodFault, f.waitT, None, None )
        self.assertRaises(BadMethodFault, f.notify, None, None )
        self.assertRaises(BadMethodFault, f.stopNotify, None, None )

    def test_createEntityListFromResponse(self):
        # flavor_manager = FlavorManager(cloudServersService)
        # self.assertEqual(expected, flavor_manager.createEntityListFromResponse(response))
        pass # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()

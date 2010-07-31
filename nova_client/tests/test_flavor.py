import unittest
from nose import SkipTest

from com.rackspace.cloud.servers.api.client.flavor import Flavor
from com.rackspace.cloud.servers.api.client.errors import BadMethodFault

class TestFlavor(unittest.TestCase):
    def test___init__(self):
        # flavor = Flavor(name)
        f = Flavor("dog")
        self.assertEqual(f.name, "dog")
        f = Flavor(None)
        self.assertEqual(f.name, None)

    def test_initFromResultDict(self):
        # flavor = Flavor(name)
        # self.assertEqual(expected, flavor.initFromResultDict(dic))
        f = Flavor("fido")
        f.initFromResultDict({'disk': 10, 'id': 1, 'ram': 256, \
                              'name': u'256 server'})
        self.assertEqual(f.disk,10)
        self.assertEqual(f.id,1)
        self.assertEqual(f.ram,256)
        self.assertEqual(f.name, u'256 server')

    def test_initFromNoneDict(self):
        f = Flavor("Name")
        f2 = Flavor("Name")
        f.initFromResultDict(None)
        f2.initFromResultDict(None)

    def test_equality(self):
        f = Flavor("Name")
        self.assertEqual(f.name, "Name")
        self.assertEqual(f.disk,None)
        self.assertEqual(f.id,None)
        self.assertEqual(f.ram,None)

        f2 = Flavor("Name")
        self.assertEqual(f, f2)
        f2.initFromResultDict({'disk':10})
        self.assertNotEqual(f2, f)

    def test_repr(self):
        f = Flavor("Snoopy")
        f.initFromResultDict({'disk': 10, 'id': 1, 'ram': 256, \
                              'name': u'256 server'})
        rep = f.__repr__()        # Just to make it happen for coverage

    def test_extra_attr(self):
        f = Flavor("Name")
        self.assertEqual(f.name, "Name")
        f2 = Flavor("Name")
        self.assertEqual(f, f2)
        f.dog = "woof"
        self.assertNotEqual(f, f2)

if __name__ == '__main__':
    unittest.main()

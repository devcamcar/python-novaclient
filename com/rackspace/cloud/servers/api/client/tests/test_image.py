import unittest
from nose import SkipTest
from nose.tools import assert_equal
from com.rackspace.cloud.servers.api.client.image import Image

class TestImage(unittest.TestCase):
    def test___init__(self):
        # flavor = Image(name)
        f = Image("dog")
        self.assertEqual(f.name, "dog")
        f = Image(None)
        self.assertEqual(f.name, None)

    def test_initFromResultDict(self):
        # flavor = Image(name)
        # self.assertEqual(expected, flavor.initFromResultDict(dic))
        f = Image("fido")
        f.initFromResultDict({'updated': "whatever", 'id': 1, 'created': "whenever", 'status': 'stateriffic', 'progress':'progresseriffic'})
        self.assertEqual(f.updated,"whatever")
        self.assertEqual(f.id,1)
        self.assertEqual(f.created,"whenever")
        self.assertEqual(f.status, 'stateriffic')
        self.assertEqual(f.progress, 'progresseriffic')

    def test_initFromNoneDict(self):
        f = Image("Name")
        f.initFromResultDict(None)
        self.assertEqual(f.name, "Name")
        self.assertEqual(f.updated,None)
        self.assertEqual(f.id,None)
        self.assertEqual(f.created,None)
        self.assertEqual(f.status,None)
        self.assertEqual(f.progress,None)

if __name__ == '__main__':
    unittest.main()

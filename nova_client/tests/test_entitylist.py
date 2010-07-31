import unittest
from nose import SkipTest
from nose.tools import assert_equal, assert_true, assert_false

from com.rackspace.cloud.servers.api.client.entitylist import EntityList
from com.rackspace.cloud.servers.api.client.errors import InvalidInitialization

def setupModule(module):
    pass

class TestEntityList(unittest.TestCase):

    def test___init__(self):
        self.assertRaises(InvalidInitialization, EntityList, None, True, None)
        self.assertRaises(InvalidInitialization, EntityList, "not a list", \
                          True, None)
        self.assertRaises(InvalidInitialization, EntityList, {"also":None, \
                          "not a list":None}, True, None)

    def test___iter__(self):
        # entity_list = EntityList(data)
        # self.assertEqual(expected, entity_list.__iter__())
        pass # TODO: implement your test here

    def test_delta(self):
        # entity_list = EntityList(data)
        # self.assertEqual(expected, entity_list.delta())
        pass # TODO: implement your test here

    def test_isEmpty(self):
        el1 = EntityList(["some", "data"],True,None)
        el2 = EntityList([],True,None)
        assert_false(el1.isEmpty())
        assert_true(el2.isEmpty())

if __name__ == '__main__':
    unittest.main()

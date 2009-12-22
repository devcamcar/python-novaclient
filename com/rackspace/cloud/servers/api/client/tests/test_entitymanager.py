import unittest
from nose import SkipTest
from com.rackspace.cloud.servers.api.client.errors import MustBeOverriddenByChildClass
from com.rackspace.cloud.servers.api.client.entitymanager import EntityManager

class TestEntityManager(unittest.TestCase):
    def test___init__(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        pass # Not instantiated directly

    def test_create(self):
        #entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        ## self.assertEqual(expected, entity_manager.create(entity))
        #self.assertRaises( MustBeOverriddenByChildClass, enti )
        pass    # TBD: should check for MustBeOverriddenByChildClass as above

    def test_createDeltaList(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.createDeltaList(detail, changes_since))
        pass # Not called directly

    def test_createDeltaListP(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.createDeltaListP(detail, changes_since, offset, limit))
        pass # Not called directly

    def test_createList(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.createList(detail))
        pass # Not called directly

    def test_createListP(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.createListP(detail, offset, limit))
        pass # Not called directly

    def test_find(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.find(id))
        pass # Not called directly

    def test_notify(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.notify(entity, changeListener))
        pass # Not called directly

    def test_refresh(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.refresh(entity))
        pass # Not called directly

    def test_remove(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.remove(entity))
        pass # Not called directly

    def test_stopNotify(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.stopNotify(entity, changeListener))
        pass # Not called directly

    def test_update(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.update(entity))
        pass # Not called directly

    def test_wait(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.wait(entity))
        pass # Not called directly

    def test_waitT(self):
        # entity_manager = EntityManager(cloudServersService, requestPrefix, responseKey)
        # self.assertEqual(expected, entity_manager.waitT(entity, timeout))
        pass # Not called directly

if __name__ == '__main__':
    unittest.main()

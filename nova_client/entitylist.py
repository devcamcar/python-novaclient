# Copyright (c) 2010, Rackspace.
# See COPYING for details.


"""
EntityList base class. Entity lists are created by an entity manager via the 
the createList and createDeltaList calls.
"""

from datetime import datetime
from com.rackspace.cloud.servers.api.client.errors import InvalidInitialization
from com.rackspace.cloud.servers.api.client.consts import DEFAULT_PAGE_SIZE

class EntityList(list):
    """
    EntityLists behave like regular Python iterables, sort of.

    Full lists automatically page through the collection of items, seeming
    to be a single continuous list.

    Lists created with specific offset and limit parameters do not page this
    way; they're limited to the records they started with.

    Please note that items are cached from the database so, if you iterate
    over the list, one of the things you iterate onto may no longer exist.

    For this reason, you must check that the item still exists before
    attempting to do anything with it and/or catch any exceptions that may be
    generted by accessing a non-existent object.
    """
    def __init__(self, data, detail, manager):
        """
        Create a new EntityList using the data, set to return detailed items
        if requested, and using manager to perform database operations for it.
         """
        if not isinstance(data, list):
            raise InvalidInitialization("Attempt to initialize EntityList with non-list 'data'", data)

        list.__init__(self)
        self.extend(data)
        self._lastModified = datetime.now()
        self._detail = detail
        self._manager = manager
        self._entityIndex = 0
        self._pageIndex = 0


    def setExtendedBehaviour(self, data):
        """
        Sets up internal variables so that future operations behave as
        expected.
        """
        pass


    @property
    def lastModified(self):
        return self._lastModified


    @property
    def detail(self):
        return self._detail


    @property
    def manager(self):
        """
        Get this list's EntityManager.
        """
        return self._manager


    def __iter__(self):
        """
        Iterate through the records by pulling them off the server a page
        at a time.

        Currently set to do DEFAULT_PAGE_SIZE records at a time as per spec.
        """
        x = 0
        while True:
            print "__iter__: ", self.detail, x, DEFAULT_PAGE_SIZE
            theList = self.manager.createListP(self.detail, x, DEFAULT_PAGE_SIZE)
            if theList:
                i = 0
                while True:
					try:
						yield theList[i]
						i += 1
					except IndexError:
						x += i
						break
            else:
                break
        raise StopIteration


    def isEmpty(self):
        return self is None or self == []


    def delta(self):
        return self.manager.createDeltaList(self.detail, self.lastModified)


	def _notAtEnd(self):
		return self._entityIndex < (len(self) + (self._pageIndex * DEFAULT_PAGE_SIZE))


    def hasNext(self):
        if self._notAtEnd():
            return True
        else:
            self = self.manager.createListP(self.detail, self._entityIndex, \
                                            DEFAULT_PAGE_SIZE)
            if len(self) > 0:
                self._pageIndex += 1
                return True
            else:
                return False
    
        
    def next(self):
        if self._notAtEnd():
            ret = self[self._entityIndex]
            self._entityIndex += 1
            return ret
        else:
            self = self.manager.createListP(self.detail, self._entityIndex, \
                    DEFAULT_PAGE_SIZE)
            if len(self) > 0:
                self._pageIndex += 1
                return self[self._entityIndex - 1]
            else:
                return False


    def reset(self):
        self = self.manager.createList(self.detail)
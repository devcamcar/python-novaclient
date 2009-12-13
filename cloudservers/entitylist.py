# Copyright (c) 2009, Rackspace.
# See COPYING for details.


"""
EntityList base class. Entity lists are created by an entity manager via the the
createList and createDeltaList calls.
"""

from datetime import datetime
from cloudservers.errors import InvalidInitialization
from cloudservers.consts import DEFAULT_PAGE_SIZE

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

    def setExtendedBehaviour(self, data):
        """
        Sets up internal variables so that future operations behave as
        expected.
        """






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
        while 1:
            theList = self.manager.createListP(self.detail, x,
                                              DEFAULT_PAGE_SIZE)
            if theList:
                i = 0
                while i < len(theList):
                    yield theList[i]
                    i += 1
                x += i
            else:
                break

        raise StopIteration

    def isEmpty(self):
        return self is None or self == []

    def delta(self):
        return self.manager.createDeltaList(self.detail, self.lastModified)
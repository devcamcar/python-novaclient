# Copyright (c) 2009, Rackspace.
# See COPYING for details.


"""
Flavor Entity.

A flavor is an available hardware configuration fora server. Each flavor has a
unique combination of disk space and memory capacity.
"""

import copy

from com.rackspace.cloud.servers.api.client.entity import Entity

class Flavor(Entity):
    """
    Flavor

    A flavor is an available hardware configuration for a server. Each flavor
    has a unique combination of disk space and memory capacity.

    """

    def __init__(self, name=None):
        super(Flavor, self).__init__(name)
        self._id = self._ram = self._disk = None
        self._manager = None

    def __eq__(self, other):
        return self._id == other._id and self._name == other._name and self._ram == other._ram and self._disk == other._disk

    def __ne__(self, other):
        return self._id != other._id or self._name != other._name or self._ram != other._ram or self._disk != other._disk

    def initFromResultDict(self, dic):
        """
        Fills up a Flavor object dict which is a result of a
        query (detailed or not) from the API
        """
        # This will happen when e.g. a find() fails.
        if dic == None:
            return

        # make a copy so we can decide if we should notify later
        flavorCopy = copy.copy(self)

        #
        ## All status queries return at least this
        #
        if 'id' in dic:
            self._id    = dic['id']

        if 'name' in dic:
            self._name  = dic['name']

        if 'ram' in dic:
            self._ram   = dic['ram']

        if 'disk' in dic:
            self._disk  = dic['disk']

        # notify change listeners if there are any and the server has changed
        self._notifyIfChanged_(flavorCopy)

    @property
    def ram(self):
        return self._ram

    @property
    def disk(self):
        return self._disk

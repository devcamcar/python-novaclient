# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
Flavor Manager - entity manager for Cloud Servers flavors.
"""

import copy
from datetime import datetime

from com.rackspace.cloud.servers.api.client.entitymanager import EntityManager
from com.rackspace.cloud.servers.api.client.entitylist import EntityList
from com.rackspace.cloud.servers.api.client.errors import *
from com.rackspace.cloud.servers.api.client.flavor import Flavor

"""
BadMethodFault is raised whenever a method is called that is not allowed.

Because flavors are immutable (provided by the API) and can not be changed
through the API.
"""
_bmf = BadMethodFault("FlavorManager")

class FlavorManager(EntityManager):
    """
    Manages the list of server Flavors
    """
    def __init__(self, cloudServersService):
        super(FlavorManager, self).__init__(cloudServersService, "flavors")
        self._flavorCopies = {} # for wait() comparisons

    def create(self, entity):
        raise _bmf

    def refresh(self, entity):
        entity.initFromResultDict(self.flavorDetails(entity.id))
        entity._manager = self

    def remove(self, entity):
        raise _bmf

    def find(self, id):
        """
        Find the flavor given by `id` and returns a Flavor object filled with
        data from the API or None if the `id` can't be found.
        """
        try:
            detailsDict = self.flavorDetails(id)
        except CloudServersAPIFault, e:
            if e.code == 404:   # not found
                return None     # just return None
            else:               # some other exception, just re-raise
                raise

        retFlavor = Flavor("")
        retFlavor.initFromResultDict(detailsDict)
        retFlavor._manager = self
        return retFlavor

    def flavorDetails(self, id):
        """
        Gets details dictionary for flavor with `id`.  If the flavor can't
        be found, returns None
        """
        retDict = None
        ret = self._GET(id, { "now": str(datetime.now()) })
        try:
            retDict = ret["flavor"]
        except KeyError, e:
            retDict = None

        return retDict

    #
    # Polling Operations
    #    
    def _wait(self, flavor):
        """
        Wait implementation
        """
        while flavor == self._flavorCopies[flavor.id]:
            try:
                self.refresh(flavor)
            except OverLimitFault as olf:
                # sleep until retry_after to avoid more OverLimitFaults
                timedelta = datetime.now - datetime.strptime(olf.retryAfter, '%Y-%m-%dT%H:%M:%SZ')                
                sleep((timedelta.days * 86400) + timedelta.seconds)
            except CloudServersFault:
                pass

    def wait (self, flavor, timeout=None):
        """
      	timeout is in milliseconds
        """
        self._flavorCopies[flavor.id] = copy.copy(flavor)
        if timeout==None:
            self._wait(flavor)
        else:
            result = self._timeout(self._wait, (flavor,), timeout_duration=timeout/1000.0)

    def notify (self, entity, changeListener):
        raise _bmf

    def stopNotify (self, entity, changeListener):
        raise _bmf

    def createEntityListFromResponse(self, response, detail):
        """
        Creates list of Flavor objects from response to list command sent
        to API
        """
        theList = []
        data = response["flavors"]
        for jsonObj in data:
            f = Flavor("")
            f.initFromResultDict(jsonObj)
            theList.append(f)

        return EntityList(theList, detail, self)

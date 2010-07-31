# Copyright (c) 2010, Rackspace.
# See COPYING for details.

"""
Flavor Manager - entity manager for Cloud Servers flavors.
"""

import copy
from datetime import datetime

from com.rackspace.cloud.servers.api.client.entitymanager import EntityManager
from com.rackspace.cloud.servers.api.client.entitylist import EntityList
import com.rackspace.cloud.servers.api.client.errors as ClientErrors
from com.rackspace.cloud.servers.api.client.flavor import Flavor

"""
BadMethodFault is raised whenever a method is called that is not allowed.

Because flavors are immutable (provided by the API) and can not be changed
through the API.
"""
_bmf = ClientErrors.BadMethodFault("FlavorManager")


class FlavorManager(EntityManager):
    """
    Manages the list of server Flavors
    """
    def __init__(self, cloudServersService):
        super(FlavorManager, self).__init__(cloudServersService, "flavors")

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
        except ClientErrors.CloudServersAPIFault, e:
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
        return ret.get("flavor")

    #
    # Polling Operations
    #    
    def _wait(self, flavor):
        """
        Wait implementation
        """
        thisFlavor = self._entityCopies[flavor.id]
        while flavor == thisFlavor:
            try:
                self.refresh(flavor)
            except ClientErrors.OverLimitFault as olf:
                # sleep until retry_after to avoid more OverLimitFaults
                self._sleepUntilRetryAfter_(olf)
            except ClientErrors.CloudServersFault:
                pass


    def wait (self, flavor, timeout=None):
        """
      	timeout is in milliseconds
        """
        self._entityCopies[flavor.id] = copy.copy(flavor)
        if timeout is None:
            self._wait(flavor)
        else:
            result = self._timeout(self._wait, (flavor,), timeout_duration=timeout/1000.0)


    def createEntityListFromResponse(self, response, detail):
        """
        Creates list of Flavor objects from response to list command sent
        to API
        """
        theList = []
        data = response["flavors"]
        for jsonObj in data:
            flavor = Flavor("")
            flavor.initFromResultDict(jsonObj)
            theList.append(flavor)
        return EntityList(theList, detail, self)

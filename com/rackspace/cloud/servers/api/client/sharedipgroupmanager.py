# -*- test-case-name: com.rackspace.cloud.servers.api.client.tests.test_sharedipgroupmanager -*-

# Copyright (c) 2010, Rackspace.
# See COPYING for details.

"""
SharedIpGroupManager class.  
Cloud Servers Entity Manager for Shared IP Groups.

Provides interface for all Shared IP Group operations as a component part of a
Cloud Servers Service object.
"""

import copy
from datetime import datetime

from com.rackspace.cloud.servers.api.client.entitymanager import EntityManager
from com.rackspace.cloud.servers.api.client.entitylist import EntityList
import com.rackspace.cloud.servers.api.client.errors as ClientErrors
from com.rackspace.cloud.servers.api.client.sharedipgroup import SharedIpGroup

# _bmf is shortcut for BadMethodFault with our classname
_bmf = ClientErrors.BadMethodFault("SharedIpGroupManager")
# _nie is shortcut for NotImplementedException
_nie = ClientErrors.NotImplementedException


class SharedIpGroupManager(EntityManager):
    """
    Manages the list of shared IP groups
    """
    def __init__(self, cloudServersService):
        super(SharedIpGroupManager, self).__init__(cloudServersService, "shared_ip_groups", "sharedIpGroups")


    def create(self, ipgroup):
        """
        Create an IP Group using the passed in ipgroup.  NOTE: it is an error
        to create an IP Group with the 'servers' ivar containing a list of
        more than one server.
        TBD: trap that and throw an exception here
        """
        ret = self._POST(ipgroup.asJSON)
        ipgroup._manager = self


    def update(self, ipgroup):
        raise _nie


    def refresh(self, entity):
        entity.initFromResultDict(self.sharedIpGroupDetails(entity.id))
        entity._manager = self


    def find(self, id):
        """
        Find the shared ip group given by `id` and return a SharedIpGroup
        object or None if the `id` can't be found.
        """
        try:
            detailsDict = self.sharedIpGroupDetails(id)
        except ClientErrors.CloudServersAPIFault, e:
            if e.code == 404:
                # not found; just return None
                return None
            else:
                # some other exception, just re-raise
                raise

        retSharedIpGroup = SharedIpGroup()  # shared ip group to populate
        retSharedIpGroup.initFromResultDict(detailsDict)
        retSharedIpGroup._manager = self
        return retSharedIpGroup


    def sharedIpGroupDetails(self, id):
        """
        Gets details dictionary for shared ip group with `id`.  Returns None
        if the sharedIpGroup can't be found.
        """
        retDict = None
        ret = self._GET(id, { "now": str(datetime.now()) })
        try:
            retDict = ret["sharedIpGroup"]
        except KeyError, e:
            retDict = None
        return retDict

    #
    # Polling Operations
    #
    def _wait(self, sharedIpGroup):
        """
        Wait implementation
        """
        thisGroup = self._entityCopies[sharedIpGroup.id]
        while sharedIpGroup == thisGroup:
            try:
                self.refresh(sharedIpGroup)
            except ClientErrors.OverLimitFault, e:
                # sleep until retry_after to avoid more OverLimitFaults
                self._sleepUntilRetryAfter_(e)
            except ClientErrors.CloudServersFault:
                pass


    def wait (self, sharedIpGroup, timeout=None):
        """
      	timeout is in milliseconds
        """
        self._entityCopies[sharedIpGroup.id] = copy.copy(sharedIpGroup)
        if timeout is None:
            self._wait(sharedIpGroup)
        else:
            result = self._timeout(self._wait, (sharedIpGroup,), timeout_duration=timeout/1000.0)


    def createEntityListFromResponse(self, response, detail):
        ip_groups = response["sharedIpGroups"]
        retList = []
        for g in ip_groups:
            shared = SharedIpGroup()
            shared.initFromResultDict(g)
            retList.append(shared)
        return EntityList(retList, detail, self)

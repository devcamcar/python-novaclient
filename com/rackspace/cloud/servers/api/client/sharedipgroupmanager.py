# -*- test-case-name: com.rackspace.cloud.servers.api.client.tests.test_sharedipgroupmanager -*-

# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
SharedIpGroupManager class.  Cloud Servers Entity Manager for Shared IP Groups.

Provides interface for all Shared IP Group operations as a component part of a
Cloud Servers Service object.
"""

import copy
from datetime import datetime

from com.rackspace.cloud.servers.api.client.entitymanager import EntityManager
from com.rackspace.cloud.servers.api.client.entitylist import EntityList
from com.rackspace.cloud.servers.api.client.errors import *
from com.rackspace.cloud.servers.api.client.sharedipgroup import SharedIpGroup

"""
_bmf is shortcut for BadMethodFault with our classname
"""
_bmf = BadMethodFault("SharedIpGroupManager")

"""
_nie is shortcut for NotImplementedException
"""
_nie = NotImplementedException

class SharedIpGroupManager(EntityManager):
    """
    Manages the list of shared IP groups
    """
    def __init__(self, cloudServersService):
        super(SharedIpGroupManager, self).__init__(cloudServersService, "shared_ip_groups", "sharedIpGroups")
        self._sharedIpGroupCopies = {} # for wait() comparisons

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
        except CloudServersAPIFault, e:
            if e.code == 404:   # not found
                return None     # just return None
            else:               # some other exception, just re-raise
                raise

        retSharedIpGroup = SharedIpGroup()  # create shared ip group to populate
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
        while sharedIpGroup == self._sharedIpGroupCopies[sharedIpGroup.id]:
            try:
                self.refresh(sharedIpGroup)
            except OverLimitFault as olf:
                # sleep until retry_after to avoid more OverLimitFaults
                timedelta = datetime.now - datetime.strptime(olf.retryAfter, '%Y-%m-%dT%H:%M:%SZ')                
                sleep((timedelta.days * 86400) + timedelta.seconds)
            except CloudServersFault:
                pass

    def wait (self, sharedIpGroup, timeout=None):
        """
      	timeout is in milliseconds
        """
        self._sharedIpGroupCopies[sharedIpGroup.id] = copy.copy(sharedIpGroup)
        if timeout==None:
            self._wait(sharedIpGroup)
        else:
            result = self._timeout(self._wait, (sharedIpGroup,), timeout_duration=timeout/1000.0)

    def createEntityListFromResponse(self, response, detail):
        ip_groups = response["sharedIpGroups"]
        retList = []
        for g in ip_groups:
            s = SharedIpGroup()
            s.initFromResultDict(g)
            retList.append(s)

        return EntityList(retList, detail, self)


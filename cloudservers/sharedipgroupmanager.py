# -*- test-case-name: cloudservers.tests.test_sharedipgroupmanager -*-

# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
SharedIpGroupManager class.  Cloud Servers Entity Manager for Shared IP Groups.

Provides interface for all Shared IP Group operations as a component part of a
Cloud Servers Service object.
"""

from cloudservers.entitymanager import EntityManager
from cloudservers.entitylist import EntityList
from cloudservers.errors import BadMethodFault, NotImplementedException
from cloudservers.sharedipgroup import SharedIpGroup

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

    def refresh(self, ipgroup):
        raise _nie

    def find(self, id):
        """
        Find the shared ip group given by `id` and return a SharedIpGroup
        object or None if the `id` can't be found.
        """
        try:
            detailsDict = self.serverDetails(id)
        except CloudServersAPIFault, e:
            if e.code == 404:   # not found
                return None     # just return None
            else:               # some other exception, just re-raise
                raise

        retServer = Server("")  # create empty server
        retServer.initFromResultDict(detailsDict)
        retServer._manager = self
        return retServer

    def sharedIpGroupDetails(self, id):
        """
        Gets details dictionary for shared ip group with `id`.  Returns None
        if the sharedIpGroup can't be found.
        """
        retDict = None
        ret = self._GET(id)
        try:
            retDict = ret["sharedIpGroup"]
        except KeyError, e:
            retDict = None

        return retDict

    #
    # Polling Operations
    #
    def wait (self, ipgroup):
        raise NotImplementedException

    def waitT (self, ipgroup, timeout):
        raise NotImplementedException

    def notify (self, ipgroup, changeListener):
        raise NotImplementedException

    def stopNotify (self, ipgroup, changeListener):
        raise NotImplementedException

    def createEntityListFromResponse(self, response, detail):
        ip_groups = response["sharedIpGroups"]
        retList = []
        for g in ip_groups:
            s = SharedIpGroup()
            s.initFromResultDict(g)
            retList.append(s)

        return EntityList(retList, detail, self)


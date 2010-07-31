# Copyright (c) 2010, Rackspace.
# See COPYING for details.

"""
SharedIpGroup object
"""

import copy

from com.rackspace.cloud.servers.api.client.entity import Entity
from com.rackspace.cloud.servers.api.client.jsonwrapper import json

"""
SharedIpGroup objects provide a convenient encapsulation of information about
shared IP groups.

As with Server objects, these objects must be manipulated with a manager class,
in this case, the SharedIpGroupManager.
"""


class SharedIpGroup(Entity):
    """
    Shared IP group objects.
    """
    def __init__(self, name="", server=None):
        """
        Create new SharedIpGroup instance. `servers` is singular since you can
        only create a new IP group by adding a single server.

        Further queries regarding the SharedIpGroup may include multiple
        servers in a list, but that info will be filled in by the API, and can
        not be done on construction.
        """
        super(SharedIpGroup, self).__init__(name)

        self._servers   = server
        self._manager = None


    def __str__(self):
        return "Name = %s : servers = %s" % (self._name, self._servers)


    def __eq__(self, other):
        return (self._id, self._name, self._servers) == (other._id, other._name, other._servers)


    def __ne__(self, other):
        return (self._id, self._name, self._servers) != (other._id, other._name, other._servers)


    def _get_name(self):
        """Get name from shared ip group object."""
        return self._name

    def _set_name(self, value):
        """Set name for this IP Group"""
        self._name = value
    name = property(_get_name, _set_name)


    @property
    def servers(self):
        return self._servers

    @property
    def asDict(self):
        """
        Return IP group object with attributes as a dictionary
        """
        # The key changes depending on whether we're dealing with a request,
        # where we're only supposed to have one, or a response, where the
        # API returns the list of servers in the IP group
        if hasattr(self._servers , "__iter__"):
            serverKey = "servers"
        else:
            serverKey = "server"

        return { "sharedIpGroup": { "id": self._id, "name": self._name, serverKey: self._servers } }

    @property
    def asJSON(self):
        """
        Return the backup schedule object converted to JSON
        """
        return json.dumps(self.asDict)


    def initFromResultDict(self, dic):
        """
        Fills up a shared ip group object from the dict which is a result of a
        query (detailed or not) from the API
        """
        # This will happen when e.g. a find() fails.
        if dic is None:
            return

        # make a copy so we can decide if we should notify later
        sharedIpGroupCopy = copy.copy(self)

        #
        ## All status queries return at least this
        #
        self._id = dic.get("id")
        self._name = dic.get("name")
        # if it has servers, grab those too
        self._servers = dic.get("servers")

        # notify change listeners if there are any and the server has changed
        self._notifyIfChanged_(sharedIpGroupCopy)

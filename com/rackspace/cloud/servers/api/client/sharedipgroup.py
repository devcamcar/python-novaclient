# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
SharedIpGroup object
"""

from cloudservers.entity import Entity
from cloudservers.jsonwrapper import json

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

    def get_name(self):
        """Get name from shared ip group object."""
        return self._name

    def set_name(self, value):
        """Set name for this IP Group"""
        self._name = value
    name = property(get_name, set_name)

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
        if hasattr(self._servers , '__iter__'):
            serverKey = "servers"
        else:
            serverKey = "server"

        bsAsDict = { "sharedIpGroup" :
                        {
                            "id"        : self._id,
                            "name"      : self._name,
                            serverKey   : self._servers,
                        }
                     }
        return bsAsDict

    @property
    def asJSON(self):
        """
        Return the backup schedule object converted to JSON
        """
        sharedIpAsJson = json.dumps(self.asDict)
        return sharedIpAsJson

    def initFromResultDict(self, dic):
        """
        Fills up a shared ip group object from the dict which is a result of a
        query (detailed or not) from the API
        """
        # This will happen when e.g. a find() fails.
        if dic == None:
            return

        #
        ## All status queries return at least this
        #
        # print "shared IP -- initFromResultDict, dic =  ", dic

        self._id        = dic['id']
        self._name      = dic['name']

        #
        ## if it has servers, grab those too
        #
        if 'servers' in dic:
            self._servers = dic['servers']

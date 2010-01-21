# Copyright (c) 2010, Rackspace.
# See COPYING for details.

"""
Server Entity
"""

import copy

from com.rackspace.cloud.servers.api.client.jsonwrapper import json
from com.rackspace.cloud.servers.api.client.entity import Entity

#
## This is what is specified in the docs, not sure what we'll use it for but
## wanted to have this around for reference
#
serverStatus = ("ACTIVE", "BUILD", "REBUILD", "SUSPENDED", "QUEUE_RESIZE",
        "PREP_RESIZE", "VERIFY_RESIZE", "PASSWORD", "RESCUE", "UNKNOWN")


class Server(Entity):
    def __init__(self, name, imageId=None, flavorId=None, metadata=None, personality=None):
        """
        Create new Server instance with specified name, imageId, flavorId and
        optional metadata.

        NOTE: This creates the data about the server, to actually create
        an actual "Server", you must ask a ServerManager.
        """
        super(Server, self).__init__(name)

        self._imageId = imageId
        self._flavorId = flavorId
        self._metadata = metadata
        # Set when a ServerManager creates a server
        self._manager = None
        # this server's ID
        self._id = None
        self._hostId = None
        self._progress = None
        self._addresses = None
        self._personality = None
        self._lastModified = None


    def __str__(self):
        return self.asJSON


    def initFromResultDict(self, dic, headers=None):
        """
        Fills up a server object from the dict which is a result of a query
        (detailed or not) from the API
        """
        # This will happen when e.g. a find() fails.
        if dic is None:
            return
        
        # make a copy so we can decide if we should notify later
        serverCopy = copy.copy(self)
         
        if headers:
            # they're tuples, so loop through and find the date
            for header in headers:
                if header[0] == 'date':
                    self._lastModified = header[1]
                    break

        #
        ## All status queries return at least this
        #
        self._id = dic.get("id")
        self._name = dic.get("name")
        self._status = dic.get("status")
        self._hostId = dic.get("hostId")
        self._metadata = dic.get("metadata")
        self._imageId = dic.get("imageId")
        self._flavorId = dic.get("flavorId")
        self._addresses = dic.get("addresses")
        # progress isn't necessarily always available
        self._progress = dic.get("progress")
        # We only get this on creation
        self._adminPass = dic.get("adminPass")

        # notify change listeners if there are any and the server has changed
        self._notifyIfChanged_(serverCopy)
        
    def _get_name(self):
        """Server's name (immutable once created @ Rackspace)."""
        return self._name

    def _set_name(self, value):
        """
        Rename a server.
        NOTE: This routine will throw a ServerNameIsImmutable fault if you try
        to rename a server attached to a ServerManager since that would
        put the name in the object and the name stored on the server
        out of sync.

        TBD:  there is an API call to change the server name and adminPass but
        it doesn't seem to allow for just changing the name.
        We could get around this by retrieving the password, then setting
        both in one shot, except you can't retrieve the password...

        TBD: Capture this comment/plan for next version.
        """
        if self._manager is None:   # if we're not owned by anyone
            self._name = value
        else:
            raise ServerNameIsImmutable("Can't rename server")
    name = property(_get_name, _set_name)


    def _get_personality(self):
        """Server's personality."""
        if self._personality:
            return self._personality
        else:
            return None

    def _set_personality(self, value):
        """Server's personality."""
        self._personality = value
    personality = property(_get_personality, _set_personality)


    @property
    def imageId(self):
        """
        Get the server's current imageId.
        """
        return self._imageId


    @property
    def flavorId(self):
        """
        Get server's current flavorId
        """
        return self._flavorId


    @property
    def metadata(self):
        """
        Return server's current metadata
        """
        return self._metadata


    @property
    def id(self):
        """
        Get the server's id
        """
        return self._id


    @property
    def hostId(self):
        """
        Get the server's hostId
        """
        return self._hostId


    @property
    def progress(self):
        """
        Server's progress as of the most recent status or 
        serverManager.ssupdate()
        """
        return self._progress


    @property
    def lastModified(self):
        """
        Server's last modified date as returned in Date header.  
        May not be the actual last modified date
        """
        return self._lastModified


    @property
    def addresses(self):
        """
        IP addresses associated with this server.
        """
        return self._addresses


    @property
    def adminPass(self):
        """
        Get admin password (only available if created within current session).
        """
        return self._adminPass


    @property
    def asDict(self):
        """
        Return server object with attributes as a dictionary suitable for use
        in creating a server json object.
        """
        serverAsDict = { "server": { "name": self.name,
                "imageId": self.imageId,
                "flavorId": self.flavorId,
                "metadata": self.metadata } }
        if self.personality:
            serverAsDict["server"]["personality"] = self.personality.asDict
        return serverAsDict


    @property
    def asJSON(self):
        """
        Return the server object converted to JSON suitable for creating a
        server.
        """
        return json.dumps(self.asDict)


    @property
    def status(self):
        """
        Get status of server, such as ACTIVE, BUILD, etc
        """
        return self._status

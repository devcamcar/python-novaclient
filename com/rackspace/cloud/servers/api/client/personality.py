# Copyright (c) 2009, Rackspace.
# See COPYING for details.

from com.rackspace.cloud.servers.api.client.jsonwrapper import json

class Personality:
    def __init__(self):
        self._files = None
        
    def get_files(self):
        return self._files

    def set_files(self, value):
        self._files = value
    files = property(get_files, set_files)

    @property
    def asDict(self):
        """
        Return personality object with attributes as a dictionary suitable for 
        use in creating a server json object.
        """
        personalityAsDict = { "personality": [] }
        
        for file in self.files:
            personalityAsDict['personality'].append(file.asDict)        
        return personalityAsDict

    @property
    def asJSON(self):
        """
        Return the personality object converted to JSON suitable for creating a
        server.
        """
        personalityAsJSON = json.dumps(self.asDict)
        return personalityAsJSON

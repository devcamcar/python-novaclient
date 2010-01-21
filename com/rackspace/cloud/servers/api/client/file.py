# Copyright (c) 2010, Rackspace.
# See COPYING for details.

import base64
from com.rackspace.cloud.servers.api.client.jsonwrapper import json

class File(object):
    def __init__(self, path=None, contents=None):
        self._path = path
        self._contents = base64.b64encode(contents)
        
    def get_path(self):
        return self._path

    def set_path(self, value):
        self._path = value
    path = property(get_path, set_path)

    def get_contents(self):
        return self._contents
        
    def set_contents(self, value):
        self._contents = base64.b64encode(value)
    contents = property(get_contents, set_contents)
    
    @property
    def asDict(self):
        """
        Return file object with attributes as a dictionary suitable for use
        in creating a server json object.
        """
        return { "file": { "path": self.path, "contents": self.contents } }

    @property
    def asJSON(self):
        """
        Return the file object converted to JSON suitable for creating a
        server.
        """
        return json.dumps(self.asDict)
    
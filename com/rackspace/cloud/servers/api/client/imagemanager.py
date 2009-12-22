# Copyright (c) 2009, Rackspace.
# See COPYING for details.


"""
ImageManager - EntityManager for managing image entities.
"""

from cloudservers.entitymanager import EntityManager
from cloudservers.entitylist import EntityList

from cloudservers.errors import BadMethodFault
from cloudservers.image import Image

"""
BadMethodFault is raised whenever a method is called that is not allowed
for flavors. Images are (currently) immutable (provided by the API) and can
not be changed through the API.
"""

_bmf = BadMethodFault("ImageManager")

class ImageManager(EntityManager):
    """
    Manages the list of server Images.
    """
    def __init__(self, cloudServersService):
        super(ImageManager, self).__init__(cloudServersService, "images")

    def create(self, entity):
        "Not implemented by this class, by design."
        raise _bmf

    def remove(self, entity):
        "Not implemented by this class, by design."
        raise _bmf

    def update(self, entity):
        "Not implemented by this class, by design."
        raise _bmf

    def refresh(self, entity):
        "Not implemented by this class, by design."
        raise _bmf

    #
    # Polling Operations
    #
    def wait (self, entity, timeout=None):
        "Not implemented by this class, by design."
        raise _bmf

    def notify (self, entity, changeListener):
        "Not implemented by this class, by design."
        raise _bmf

    def stopNotify (self, entity, changeListener):
        "Not implemented by this class, by design."
        raise _bmf

    def createEntityListFromResponse(self, response, detail):
        """
        Creates list of image objects from response to list command sent
        to API
        """
        theList = []
        data = response["images"]
        for jsonObj in data:
            i = Image("")
            i.initFromResultDict(jsonObj)
            theList.append(i)

        return EntityList(theList, detail, self)

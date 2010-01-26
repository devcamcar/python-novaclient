# Copyright (c) 2010, Rackspace.
# See COPYING for details.


"""
ImageManager - EntityManager for managing image entities.
"""

from datetime import datetime
import time
import copy

from com.rackspace.cloud.servers.api.client.entitymanager import EntityManager
from com.rackspace.cloud.servers.api.client.entitylist import EntityList
from com.rackspace.cloud.servers.api.client.errors import BadMethodFault, \
        NotImplementedException, CloudServersAPIFault
from com.rackspace.cloud.servers.api.client.image import Image

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
        entity.initFromResultDict(self.imageDetails(entity.id))
        entity._manager = self

    def find(self, id):
        """
        Find the image given by `id` and returns an Image object filled with
        data from the API or None if the `id` can't be found.
        """
        try:
            detailsDict = self.imageDetails(id)
        except CloudServersAPIFault, e:
            if e.code == 404:   # not found
                return None     # just return None
            else:               # some other exception, just re-raise
                raise
        retImage = Image("")
        retImage.initFromResultDict(detailsDict)
        retImage._manager = self
        return retImage

    def imageDetails(self, id):
        """
        Gets details dictionary for image with `id`.  If the image can't
        be found, returns None
        """
        retDict = None
        ret = self._GET(id, { "now": str(datetime.now()) })
        return ret.get("image")


    #
    # Polling Operations
    #
    def _wait(self, image):
        """
        Wait implementation
        """
        while image.status in ('ACTIVE', 'FAILED', 'UNKNOWN'):
            try:
                self.refresh(image)
            except OverLimitFault, e:
                # sleep until retry_after to avoid more OverLimitFaults
                self._sleepUntilRetryAfter_(e)
            except CloudServersFault:
                pass


    def wait (self, image, timeout=None):
        """
      	timeout is in milliseconds
        """
        self._entityCopies[image.id] = copy.copy(image)
        if timeout is None:
            self._wait(image)
        else:
            result = self._timeout(self._wait, (image, ), timeout_duration=timeout/1000.0)


    def createEntityListFromResponse(self, response, detail):
        """
        Creates list of image objects from response to list command sent
        to API
        """
        theList = []
        data = response["images"]
        for jsonObj in data:
            img = Image("")
            img.initFromResultDict(jsonObj)
            theList.append(img)
        return EntityList(theList, detail, self)

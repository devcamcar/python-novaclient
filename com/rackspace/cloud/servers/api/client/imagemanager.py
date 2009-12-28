# Copyright (c) 2009, Rackspace.
# See COPYING for details.


"""
ImageManager - EntityManager for managing image entities.
"""

from com.rackspace.cloud.servers.api.client.entitymanager import EntityManager
from com.rackspace.cloud.servers.api.client.entitylist import EntityList

from com.rackspace.cloud.servers.api.client.errors import BadMethodFault
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
        "Not implemented by this class, by design."
        raise _bmf

    #
    # Polling Operations
    #
    def _imageInWaitState(self, image):
        
        # For Images, the following are considered end states by the wait call: 
        end_states = ['ACTIVE', 'FAILED', 'UNKNOWN']
        
        try:
            end_states.index(image.status)
            inWaitState = False # if we made it this far, it's not in a wait state
        except ValueError:
            inWaitState = True
        return inWaitState
    
    
    def _wait(self, image):
        """
        Wait implementation
        """
        while self._imageInWaitState(image):
            try:
                self.refresh(image)
            except OverLimitFault as olf:
                # sleep until retry_after to avoid more OverLimitFaults
                timedelta = datetime.now - datetime.strptime(olf.retryAfter, '%Y-%m-%dT%H:%M:%SZ')                
                sleep((timedelta.days * 86400) + timedelta.seconds)
            except CloudServersFault:
                pass

    def wait (self, image, timeout=None):
        """
      	timeout is in milliseconds
        """
        if timeout==None:
            self._wait(image)
        else:
            result = self._timeout(self._wait, (image,), timeout_duration=timeout/1000.0)

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

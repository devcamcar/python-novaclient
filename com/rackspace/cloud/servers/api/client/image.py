# Copyright (c) 2009, Rackspace.
# See COPYING for details.


"""
Image Entity.

An image is a collection of files you use to create or rebuild a server.
Rackspace provides pre-built OS images by default.
"""

import copy

from com.rackspace.cloud.servers.api.client.entity import Entity


class Image(Entity):
    """
    Image

    An image is a collection of files you use to create or rebuild a server.
    Rackspace provides pre-built OS images by default. You may also create custom
    images.
    """
    def __init__(self, name=None):
        super(Image, self).__init__(name)
        self._id = self._updated = self._created = None
        self._status = self._progress = None
        self._manager = None

    def initFromResultDict(self, dic):
        """
        Fills up a Image object dict which is a result of a
        query (detailed or not) from the API
        """

        # This will happen when e.g. a find() fails.
        if dic == None:
            return

        # make a copy so we can decide if we should notify later
        imageCopy = copy.copy(self)

        #
        ## All status queries return at least this
        #
        self._id    = dic['id']

        if 'name' in dic:
            self._name  = dic['name']

        # Detailed queries have 'updated'
        if 'updated' in dic:
            self._updated   = dic['updated']

        if 'created' in dic:
            self._created   = dic['created']

        if 'status' in dic:
            self._status    = dic['status']

        # User created images have this...
        if 'progress' in dic:
            self._progress  = dic['progress']

        # notify change listeners if there are any and the server has changed
        self._notifyIfChanged_(imageCopy)

    @property
    def updated(self):
        return self._updated

    @property
    def created(self):
        return self._created

    @property
    def status(self):
        return self._status

    @property
    def progress(self):
        return self._progress







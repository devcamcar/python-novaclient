# Copyright (c) 2010, Rackspace.
# See COPYING for details.

"""
Cloud Servers Service class.

Container for the various Entity Managers that manage Rackspace Cloud Servers
entities such as Servers, Images, Shared IP Groups, and Flavors.
"""

from com.rackspace.cloud.servers.api.client.errors import NotImplementedException
from com.rackspace.cloud.servers.api.client.authentication import Authentication
from com.rackspace.cloud.servers.api.client.connection import Connection

from com.rackspace.cloud.servers.api.client.flavormanager import FlavorManager
from com.rackspace.cloud.servers.api.client.servermanager import ServerManager
from com.rackspace.cloud.servers.api.client.imagemanager import ImageManager
from com.rackspace.cloud.servers.api.client.sharedipgroupmanager import SharedIpGroupManager

from com.rackspace.cloud.servers.api.client.consts import json_hdrs
from com.rackspace.cloud.servers.api.client.jsonwrapper import json


class Settings(dict):
    """
    A thin wrapper over dict to conform to Java convention ivar access method
    names.
    """
    def __init__(self):
        self.setSetting = self.__setitem__
        self.getSetting = self.__getitem__


class ServiceInfo(object):
    """
    Provides service information about a CloudServersService object.
    """
    def __init__(self, owner):
        """
        ServiceInfo is a volatile object that can return current values
        for various information about the CloudServersService
        """
        # we are tied to one CloudServersService
        self._owner = owner

        self._versionInfo = None        # From Cloud Servers API, cached
        self._limits = None             # TBD: From CS API, volatile
        self._settings = None           # TBD: From CS API, volatile

    @property
    def limits(self):
        return self._owner.serviceInfoLimits

    @property
    def versionInfo(self):
        return self._owner.serviceInfoVersionInfo

    @property
    def settings(self):
        return self._owner.serviceInfoSettings


class CloudServersService(object):
    """
    Provides the main interface to, and serves as a container for all of the
    separate Entity Managers required to interface with Cloud Servers.
    """

    def __init__(self, userName, apiKey):
        """
        __init__ just makes sure the class's serviceInfo is initialized, once.
        """
        self._serviceInfo = ServiceInfo(self)

        # Get the computeURL and authToken to use for subsequent queries
        auth = Authentication(userName, apiKey)
        computeURL, authToken = auth.authenticate()

        self._auth = auth
        self._computeURL = computeURL
        self._authToken = authToken

        # defer all of these to be created as needed.
        self._conn =  None
        self._serverManager = self._imageManager = None
        self._sharedIpGroupManager = self._flavorManager = None


    def info(self, includePrivate=False):
        """
        TBD: better description
        Return all of the status information for the cloud servers service
        """
        raise NotImplementedException

    def versionInfo(self):
        """
        TBD: better description
        Return the version information.
        """
        raise NotImplementedException

    def createServerManager(self):
        if not self._serverManager:
            self._serverManager = ServerManager(self)
        return self._serverManager

    def createImageManager(self):
        if not self._imageManager:
            self._imageManager = ImageManager(self)
        return self._imageManager

    def createSharedIpGroupManager(self):
        if not self._sharedIpGroupManager:
            self._sharedIpGroupManager = SharedIpGroupManager(self)
        return self._sharedIpGroupManager

    def createFlavorManager(self):
        if not self._flavorManager:
            self._flavorManager = FlavorManager(self)
        return self._flavorManager

    def make_request(self, method, url, data='', headers=None, params=None,
             retHeaders=None):
        conn = self.get_connection()
        return conn.make_request(method, (url,), data=data, hdrs=headers,
                 params=params, retHeaders=retHeaders)

    def get_connection(self):
        """
        Handles getting a connection, redoing authorization if it's
        expired
        """
        if not self._conn:
            self._conn = Connection(auth=self._auth)
        return self._conn


    def GET(self, url, params=None, headers=None, retHeaders=None):
        """
        Feed a GET request through to our connection
        """
        # NOTE: ret is NOT an http response object, it's a digested
        #       object from reading the response object
        #       see Connection for implementation
        ret = self.make_request("GET", url, params=params, headers=headers,
                retHeaders=retHeaders)
        return ret


    def POST(self, url, data):
        """
        Feed a POST request through to our connection.
        """
        ret = self.make_request("POST", url, data=data)
        return ret


    def DELETE(self, url):
        """
        Feed a DELETE request through to our connection.
        """
        ret = self.make_request("DELETE", url)
        return ret


    def PUT(self, url):
        """
        Feed a PUT request through to our connection.
        """
        ret = self.make_request("PUT", url)
        return ret

    #
    # serviceInfo attribute and ServiceInfo class support
    #
    @property
    def serviceInfo(self):
        return self._serviceInfo

    @property
    def serviceInfoLimits(self):
        limits_dict = self.GET("limits")
        return limits_dict["limits"]

    @property
    def serviceInfoVersionInfo(self):
        raise NotImplementedException

    @property
    def serviceInfoSettings(self):
        raise NotImplementedException

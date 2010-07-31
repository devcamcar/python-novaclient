# Copyright (c) 2010, Rackspace.
# See COPYING for details.

"""
Connection class.
"""

import socket
from urllib import quote
from httplib import HTTPSConnection, HTTPConnection, HTTPException
from time import sleep
from datetime import datetime

from com.rackspace.cloud.servers.api.client.shared.utils import parse_url
from com.rackspace.cloud.servers.api.client.authentication import Authentication
from com.rackspace.cloud.servers.api.client.consts import default_authurl, user_agent, json_hdrs
from com.rackspace.cloud.servers.api.client.jsonwrapper import json

import com.rackspace.cloud.servers.api.client.errors as ClientErrors

class Connection(object):
    """
    Manages the connection to the cloud server system.  Support class, not
    to be used directly.

    @undocumented: http_connect
    @undocumented: make_request
    """
    def __init__(self, username=None, api_key=None, **kwargs):
        """
        Accepts keyword arguments for Rackspace  username and api key.
        Optionally, you can omit these keywords and supply an
        Authentication object using the auth keyword.
        """
        self.connection_args = None
        self.connection = None
        self.token = None

        # handle optional kwargs
        self.debuglevel = int(kwargs.get('debuglevel', 0))
        self.auth = kwargs.get('auth', None)
        socket.setdefaulttimeout = int(kwargs.get('timeout', 5))

        if not self.auth:
            # If we didn't get an auth object, do authentication
            authurl = kwargs.get('authurl', default_authurl)
            if username and api_key and authurl:
                self.auth = Authentication(username, api_key, authurl)
            else:
                # Raise an InvalidArgumentsFault
                err_msg = "Connection "
                if not username:
                    err_msg += "- missing username"
                if not api_key:
                    err_msg += "- missing api_key"
                if not authurl:
                    err_msg += "- missing authurl"
                raise ClientErrors.InvalidArgumentsFault(err_msg)
        self._authenticate()


    def _authenticate(self):
        """
        Authenticate and setup this instance with the values returned.
        """
        (self.url, self.token) = self.auth.authenticate()
        self.connection_args = parse_url(self.url)
        self.conn_class = (self.connection_args[3] and HTTPSConnection) or HTTPConnection
        self.http_connect()


    def http_connect(self):
        """
        Setup the http connection instance.
        """
        host, port, self.uri, is_ssl = self.connection_args
        self.connection = self.conn_class(host, port=port)
        self.connection.set_debuglevel(self.debuglevel)


    def make_request(self, method, path=[], data='', hdrs=None, params=None,
                     retHeaders=None):
        """
        Given a method (i.e. GET, PUT, POST, DELETE etc), a path, data, header
        and metadata dicts, and an optional dictionary of query parameters,
        performs an http request.
        """
        path = '/%s/%s' % (self.uri.rstrip('/'), '/'.join([quote(i) for i in path]))
        print "connection path: ", path

        if isinstance(params, dict) and params:
            query_args = ['%s=%s' \
                    % (quote(x),quote(str(y))) for (x,y) in params.items()]
            path = '%s?%s' % (path, '&'.join(query_args))

        headers = { 'User-Agent': user_agent,
                    'X-Auth-Token': self.token }
                  
        if data and (method in ('POST', 'PUT')):
            # content type is required for requests with a body
            headers.update(json_hdrs)
            
        if isinstance(hdrs, dict):
            headers.update(hdrs)

        dataLen = len(data)
        if dataLen:
            headers['Content-Length'] = dataLen

        def retry_request():
            """
            Re-connect and re-try a failed request once
            """
            self.http_connect()
            self.connection.request(method, path, data, headers)
            return self.connection.getresponse()

        try:
            self.connection.request(method, path, data, headers)
            response = self.connection.getresponse()
        except HTTPException:
            # A simple HTTP exception, just retry once
            response = retry_request()

        # If our caller needs the headers back, they'll have sent this in
        # and it must be a list()!
        if retHeaders:
            retHeaders.extend(response.getheaders())

        raw = response.read()

        # print "status: ", response.status
        # print "response: ", raw

        try:
            responseObj = json.loads(raw)
        except:
            responseObj = {"cloudServersFault": "No message, no response obj"}

        if response.status == 401:
            self._authenticate()
            response = retry_request()

        # if the response is bad, parse and raise the CloudServersFault
        if 400 <= response.status <= 599:
            key = responseObj.keys()[0]
            faultType = "%s%s%s" % (key[0].capitalize(), key[1:], 'Fault')
            fault = responseObj[key]
            faultClass = getattr(ClientErrors, faultType)
            if faultType == 'OverLimitFault':
                raise faultClass(fault['message'], '', fault['code'], fault['retryAfter'])
            else:
                raise faultClass(fault['message'], fault['details'], fault['code'])

        return responseObj

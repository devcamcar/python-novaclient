# Copyright (c) 2010, Rackspace.
# See COPYING for details.

"""
Authentication Classes

Authentication instances are used to interact with the remote authentication 
service, retreiving storage system routing information and session tokens.
"""

import urllib
from httplib import HTTPSConnection, HTTPConnection, HTTPException
from com.rackspace.cloud.servers.api.client.shared.utils import parse_url
import com.rackspace.cloud.servers.api.client.errors as ClientErrors
from com.rackspace.cloud.servers.api.client.consts import user_agent, default_authurl


class BaseAuthentication(object):
    """
    The base authentication class from which all others inherit.
    """
    def __init__(self, username, api_key, authurl=default_authurl):
        self.authurl = authurl
        self.headers = {
                'x-auth-user': username,
                'x-auth-key': api_key,
                'User-Agent': user_agent}
        self.host, self.port, self.uri, self.is_ssl = parse_url(self.authurl)
        self.conn_class = (self.is_ssl and HTTPSConnection) or HTTPConnection

    def authenticate(self):
        """
        Initiates authentication with the remote service and returns a
        two-tuple containing the storage system URL and session token.

        This is a dummy method from the base class. It must be overridden by
        sub-classes and will raise MustBeOverriddenByChildClass if called.
        """
        raise ClientErrors.MustBeOverriddenByChildClass

class Authentication(BaseAuthentication):
    """
    Authentication, routing, and session token management.
    """
    def authenticate(self):
        """
        Initiates authentication with the remote service and returns a
        two-tuple containing the storage system URL and session token.
        """
        def retry_request():
            '''Re-connect and re-try a failed request once'''
            self.http_connect()
            self.connection.request(method, path, data, headers)
            return self.connection.getresponse()

        try:
            conn = self.conn_class(self.host, self.port)
        except HTTPException:   # httplib threw this
            # Try again, throw one of our exceptions if we can't get it
            try:
                conn = self.conn_class(self.host, self.port)
            except HTTPException,e:
                raise ClientErrors.HTTPLibFault(e)

        conn.request('GET', self.authurl, '', self.headers)
        response = conn.getresponse()
        buff = response.read()

        # A status code of 401 indicates that the supplied credentials
        # were not accepted by the authentication service.
        if response.status == 401:
            raise ClientErrors.AuthenticationFailed()
        elif response.status != 204:
            raise ClientErrors.ResponseError(response.status, response.reason)

        # these must be provided or we have an error
        compute_url = auth_token = None

        hdrs = response.getheaders()

        for hdr in hdrs:
            hdr_key_lc = hdr[0].lower()
            hdr_value = hdr[1]
            if hdr_key_lc == "x-auth-token":
                auth_token = hdr_value
            elif hdr_key_lc == "x-server-management-url":
                compute_url = hdr_value

        conn.close()

        if not (auth_token and compute_url):
            raise ClientErrors.AuthenticationError("Invalid response from the authentication service.")

        return (compute_url, auth_token)

# vim:set ai ts=4 sw=4 tw=0 expandtab:

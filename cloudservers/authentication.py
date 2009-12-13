# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
Authentication Classes

Authentication instances are used to interact with the remote authentication service,
retreiving storage system routing information and session tokens.
"""

import urllib
from httplib                    import  HTTPSConnection, \
                                        HTTPConnection, \
                                        HTTPException
from cloudservers.shared.utils  import  parse_url
from cloudservers.errors        import  ResponseError, \
                                        AuthenticationError, \
                                        AuthenticationFailed, \
                                        HTTPLibFault
from cloudservers.consts        import  user_agent, default_authurl


class BaseAuthentication(object):
    """
    The base authentication class from which all others inherit.
    """
    def __init__(self, username, api_key, authurl=default_authurl):
        self.authurl = authurl
        self.headers = dict()
        self.headers['x-auth-user'] = username
        self.headers['x-auth-key'] = api_key
        self.headers['User-Agent'] = user_agent
        (self.host, self.port, self.uri, self.is_ssl) = parse_url(self.authurl)
        self.conn_class = self.is_ssl and HTTPSConnection or HTTPConnection

    def authenticate(self):
        """
        Initiates authentication with the remote service and returns a
        two-tuple containing the storage system URL and session token.

        This is a dummy method from the base class. It must be overridden by
        sub-classes and will raise MustBeOverriddenByChildClass if called.
        """
        raise MustBeOverriddenByChildClass

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
                raise HTTPLibFault(e)

        conn.request('GET', self.authurl, '', self.headers)
        response = conn.getresponse()
        buff = response.read()

        # A status code of 401 indicates that the supplied credentials
        # were not accepted by the authentication service.
        if response.status == 401:
            raise AuthenticationFailed()

        if response.status != 204:
            raise ResponseError(response.status, response.reason)

        compute_url = auth_token = None # these must be provided or we have an error

        hdrs = response.getheaders()

        for hdr in hdrs:
            hdr_key_lc = hdr[0].lower()
            hdr_value = hdr[1]
            if hdr_key_lc == "x-auth-token":
                auth_token = hdr_value
            if hdr_key_lc == "x-server-management-url":
                compute_url = hdr_value

        conn.close()

        if not (auth_token and compute_url):
            raise AuthenticationError("Invalid response from the " \
                    "authentication service.")
        # print auth_token, compute_url

        return (compute_url, auth_token)

# vim:set ai ts=4 sw=4 tw=0 expandtab:

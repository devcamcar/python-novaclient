# Copyright (c) 2010, Rackspace.
# See COPYING for details.

"""
Exception (fault) classes.
"""

# Error codes
class ErrorCodes(object):
    """
    Error code manifest constants
    """
    E_UNKNOWN = -1

    # Calls to unimplemented or illegal methods (e.g. delete on Flavors)
    E_NOT_IMPLEMENTED = 1
    E_BAD_METHOD_FAULT = 2

    # Bad use of API due to bad parameters
    E_BAD_PARAMETERS_FAULT = 10

    # Specifically a badly formed server name
    E_INVALID_SERVER_NAME = 30

    # A low-level exception, wrapped in one of our exceptions
    E_HTTPLIB_EXCEPTION = 40


class CloudServersAPIFault(Exception):
    """Interface definition for CloudServersFault"""
    def __init__(self, message, details, code):
        self._message = message
        self._details = details
        self._code = code


    def __repr__(self):
        """
        return error as formatted string
        """
        return str(self._code) + ":" + self._message + " : " + self._details

    def __str__(self):
        return "Code   : " + str(self.code) + " Message: " + self._message \
               + " Details: " + self._details


    @property
    def message(self):
        return self._message

    @property
    def details(self):
        return self._details

    @property
    def code(self):
        return self._code

NotImplementedException = CloudServersAPIFault("Required Method not\
                                               Implemented", "", \
                                               ErrorCodes.E_NOT_IMPLEMENTED)

class OverLimitAPIFault(CloudServersAPIFault):
    """
    Interface definition for an over-limit exception
    """
    def __init__(self, message, details, code, retryAfter):
        super(OverLimitAPIFault, self).__init__(message,details,code)
        self._retryAfter = retryAfter

    @property
    def retryAfter(self):
        return self._retryAfter


class CloudServersFault(CloudServersAPIFault):
    """
    Implementaiton of Cloud Servers Fault
    """
    pass


class OverLimitFault(OverLimitAPIFault):
    """
    Implementation of over-limit exception
    """
    pass


class BadMethodFault(CloudServersAPIFault):
    """
    BadMethodFault, raised when child class is not allowed to implement called
    method i.e. create(), remove() and update() for immutable children of
    EntityManager

    @param className: the name of the class on which the method was called
    """
    def __init__(self, className):
        super(BadMethodFault, self).__init__("Bad Method Fault", \
                                             "Method not allowd on %s class" \
                                             % (className,), \
                                             ErrorCodes.E_BAD_METHOD_FAULT)


class InvalidArgumentsFault(CloudServersAPIFault):
    """
    Invalid arguments passed to API call.  Use `message` to tell the user
    which call/parameter was involved.
    """
    def __init__(self, message):
        super(InvalidArgumentsFault,self).__init__(message, \
              "Bad or missing arguments passed to API call", \
              ErrorCodes.E_BAD_PARAMETERS_FAULT)


class HTTPLibFault(CloudServersAPIFault):
    """
    Wraps HTTPExceptions into our exceptions as per spec
    """
    def __init__(self, message):
        super(HTTPLibFault,self).__init__(message, "Low Level HTTPLib Exception",
                ErrorCodes.E_HTTPLIB_EXCEPTION)


class ServerNameIsImmutable(CloudServersAPIFault):
    def __init(self, message):
        super(ServerNameIsImmutable, self).__init__(message,
                "Server can't be renamed when managed by ServerManager")


#-----------------------------------------------------------------------------
# Faults from the Cloud Servers Developer Guide
#-----------------------------------------------------------------------------

class ServiceUnavailableFault(CloudServersAPIFault):
    def __init(self, message):
        super(ServiceUnavailableFault, self).__init__(message, "", ErrorCodes.E_UNKNOWN)


class UnauthorizedFault(CloudServersAPIFault):
    def __init(self, message):
        super(UnauthorizedFault, self).__init__(message, "", ErrorCodes.E_UNKNOWN)


class BadRequestFault(CloudServersAPIFault):
    def __init(self, message):
        super(BadRequestFault, self).__init__(message, "", ErrorCodes.E_UNKNOWN)


class BadMediaTypeFault(CloudServersAPIFault):
    def __init(self, message):
        super(BadMediaTypeFault, self).__init__(message, "", ErrorCodes.E_UNKNOWN)


class ItemNotFoundFault(CloudServersAPIFault):
    def __init(self, message):
        super(ItemNotFoundFault, self).__init__(message, "", ErrorCodes.E_UNKNOWN)


class BuildInProgressFault(CloudServersAPIFault):
    def __init(self, message):
        super(BuildInProgressFault, self).__init__(message, "", ErrorCodes.E_UNKNOWN)


class ServerCapacityUnavailableFault(CloudServersAPIFault):
    def __init(self, message):
        super(ServerCapacityUnavailableFault, self).__init__(message, "", ErrorCodes.E_UNKNOWN)


class BackupOrResizeInProgressFault(CloudServersAPIFault):
    def __init(self, message):
        super(BackupOrResizeInProgressFault, self).__init__(message, "", ErrorCodes.E_UNKNOWN)


class ResizeNotAllowedFault(CloudServersAPIFault):
    def __init(self, message):
        super(ResizeNotAllowedFault, self).__init__(message, "", ErrorCodes.E_UNKNOWN)


#-----------------------------------------------------------------------------
# Extra exceptions, not in formal spec
#-----------------------------------------------------------------------------

class NeedsTestError(Exception):
    pass


class InvalidServerNameFault(CloudServersAPIFault):
    """
    Thrown when an invalid server name is specified.
    """
    def __init__(self, serverName):
        super(InvalidServerName, self).__init__("Invalid Server Name",
                serverName, ErrorCodes.E_INVALID_SERVER_NAME)


class ResponseError(Exception):
    """
    Raised when the remote service returns an error.
    """
    def __init__(self, status, reason):
        self.status = status
        self.reason = reason
        Exception.__init__(self)

    def __repr__(self):
        return '%d: %s' % (self.status, self.reason)


class InvalidUrl(Exception):
    """
    Not a valid url for use with this software.
    """
    pass


class IncompleteSend(Exception):
    """
    Raised when there is a insufficient amount of data to send.
    """
    pass


class AuthenticationFailed(Exception):
    """
    Raised on a failure to authenticate.
    """
    pass


class AuthenticationError(Exception):
    """
    Raised when an unspecified authentication error has occurred.
    """
    pass


class MustBeOverriddenByChildClass(Exception):
    """
    Raised when child class does not override required method defined in
    base class.
    """
    pass


class InvalidInitialization(Exception):
    """
    Raised when a class initializer is passed invalid data.
    """
    pass

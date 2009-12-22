# Copyright (c) 2009, Rackspace.
# See COPYING for details.

import re
import string
from urlparse  import urlparse

from com.rackspace.cloud.servers.api.client.errors    import InvalidUrl

# initialize only once, when this is imported
stripchars = string.whitespace + '/'

def find_in_list(list, searchValue, keyIndex=0, valueIndex=0):
    """
    Finds an item in a list of sequences where the key is in
    list[item][keyIndex] and the value is in list[item][valueIndex]
    """
    for i in list:
        if searchValue == i[keyIndex].lower():
            return i[valueIndex]

    return None

def parse_url(url):
    """
    Given a URL, returns a 4-tuple containing the hostname, port,
    a path relative to root (if any), and a boolean representing
    whether the connection should use SSL or not.
    NOTE: this routine's error checking is very weak.  Bad ports like ABC are
    not detected, for example.
    """
    (scheme, netloc, path, params, query, frag) = urlparse(url)

    # We only support web services
    if not scheme in ('http', 'https'):
        raise InvalidUrl('Scheme must be one of http or https')

    is_ssl = scheme == 'https' and True or False

    # Verify hostnames are valid and parse a port spec (if any)
    match = re.match('([a-zA-Z0-9\-\.]+):?([0-9]{2,5})?', netloc)

    if match:
        (host, port) = match.groups()
        if not port:
            port = is_ssl and '443' or '80'
    else:
        raise InvalidUrl('Invalid host and/or port: %s' % netloc)

    return (host, int(port), path.strip('/'), is_ssl)



def build_url(*params):
    """
    Join two or more url components, inserting '/' as needed.

    Cleans up the params before joining them

        * Removes whitespace from both ends
        * Removes any leading and trailing slashes
        * Converts integers to strings (used for server id's a lot)

    Also, sequences in paramters are properly handled i.e.:

        build_url("this", ("that", "and", "the"), "other")

    will produce:

        "this/that/and/the/other"

    The nesting, padding, '/' chars etc. can be completely arbitrary and this
    routine will handle it.

    If you find a case where it can't, please send a bug report!
    """

    path = ""
    for p in params:
        if not p:       # we handle skipping None so callers needn't worry
            continue

        # If it's an iterable (this test will skip strings)
        #   go add it recursively
        if hasattr(p , '__iter__'):
            # Expand the iterable and pass it on, assign return value
            # to path and continue
            path = build_url(path, *p)
        else:
            if type(p) == type(123):    # see if it's the same type as an int
                p = str(p)

            # strip all leading and trailing whitespace and '/'

            p = p.strip(stripchars)

            # If path isn't empty, add trailing slash
            if path != "":
                path += '/'

            path += p

    return path


# Copyright (c) 2009, Rackspace.
# See COPYING for details.


"""
Tests for utility functions
"""

import unittest

from com.rackspace.cloud.servers.api.client.shared.utils import build_url, parse_url, find_in_list
from com.rackspace.cloud.servers.api.client.errors import InvalidUrl
from com.rackspace.cloud.servers.api.client.consts import get_version, __version__
from com.rackspace.cloud.servers.api.client.version import get_version as csv_get_version

class TestConsts(unittest.TestCase):
    """
    Test consts module
    """
    def testVersion(self):
        self.assertEqual(get_version(), __version__)
        self.assertEqual(get_version(), csv_get_version())

    def test_version_params(self):
        """
        Test permutations of parameters to get_version()
        """
        a = csv_get_version(True)
        b = csv_get_version(False)
        c = csv_get_version(True, False)
        d = csv_get_version(True, True)
        e = csv_get_version(False, False)
        f = csv_get_version(False, True)
        return

class TestUtilities(unittest.TestCase):
    """
    Test utility functions
    """
    def test_build_url(self):
        tiat = "this/is/a/test"
        urls =  [
                    # Simple list of params
                    (1,
                        (
                            "this", "is", "a", "test"
                        )
                    ),

                    # leading and trailing '/'
                    (2,
                        (
                        "////this///", "////is///",
                        "//////a/////", "///////test//////"
                        )
                    ),

                    # sequence + string
                    (3,
                        (
                            ("this", "is", "a"),
                            "test"
                        )
                    ),

                    # whitespace
                    (4,
                        (
                        "  this  ", "\r\nis  \r\n",
                        "\t\r\n a\r\n\t", "    test    "
                        )
                    ),
                ]

        for tn, param in urls:
            tr = build_url(param)
            self.assertEqual(tiat, tr)

            tr = build_url(*param)
            self.assertEqual(tiat, tr)

    def test_build_url_with_numbers(self):
        rslt = "123/456/abc/hithere"
        urls=[
                (1,
                    (
                    123, 456, "abc", "hithere"
                    )
                ),
                (2,
                    (
                    "123",456, "abc", "hithere"
                    )
                ),
                (3,
                    (
                    123,"456", "abc", "hithere"
                    )
                ),
                (4,
                    (
                    "123","456", "abc", "hithere"
                    )
                ),
            ]
        for tn, param in urls:
            tr = build_url(param)
            self.assertEqual(rslt, tr)

            tr = build_url(*param)
            self.assertEqual(rslt, tr)

    def test_parse_url(self):
        self.assertRaises(InvalidUrl, parse_url, "bad://doggie.not.valid.url.scheme")
        self.assertRaises(InvalidUrl, parse_url, "http://%%")

    def test_find_in_list(self):
        hl = [
                ('content-length', '18031'),
                ('accept-ranges', 'bytes'),
                ('server', 'Apache/2.2.9 (Debian) DAV/2 SVN/1.5.1 mod_ssl/2.2.9 OpenSSL/0.9.8g mod_wsgi/2.5 Python/2.5.2'),
                ('last-modified', 'Fri, 27 Nov 2009 22:03:14 GMT'),
                ('etag', '"105800d-466f-479617552ec80"'),
                ('date', 'Sat, 28 Nov 2009 02:03:43 GMT'),
                ('content-type', 'text/html'),
             ]
        last_modified = find_in_list(hl,"last-modified", 0, 1)
        self.assertEqual(last_modified, 'Fri, 27 Nov 2009 22:03:14 GMT')
        content_type = find_in_list(hl,"content-type", 0, 1)
        self.assertEqual(content_type, 'text/html')
        notThere = find_in_list(hl, "BADKEY", 0, 1)
        self.assertEqual(notThere, None)

if __name__ == "__main__":
    unittest.main()

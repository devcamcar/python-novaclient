# Copyright (c) 2009, Rackspace.
# See COPYING for details.



"""
Just wraps import of unittest in case we want to use e.g. Twisted's, if it's
available, or regular unittest otherwise.
"""

__all__ = []

# Was using twisted, removed
#try:
#    from twisted.trial import unittest as ut
#    import unittest as regular_unittest
#    ut.main = regular_unittest.main         # workaround for twisted.trial's lack of main()
#except ImportError:
#    import unittest as ut

import unittest

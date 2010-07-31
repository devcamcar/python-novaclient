# Copyright (c) 2010, Rackspace.
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
#    # workaround for twisted.trial's lack of main()
#    ut.main = regular_unittest.main 
#except ImportError:
#    import unittest as ut

import unittest

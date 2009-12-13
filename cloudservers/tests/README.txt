#----------------------------------------------------------------------------
# Rackspace Cloud Servers Python API
#
# Test suite.
#
#----------------------------------------------------------------------------

#*****************************************************************************
# WARNING...WARNING...WARNING...WARNING...WARNING...WARNING...WARNING...
#*****************************************************************************
# Please be aware that these tests create and destroy a LARGE number of 
# servers and, while we haven't computed the net cost of doing so, it could be 
# quite expensive and, since some of the tests look quite 'hackish' may lead
# to account suspension; at least until you explain yourself to the right 
# people.
#
# Please don't do this with a paid account unless you're prepared to pay all
# associated fees including those resulting from failed tests that may leave
# servers (and your bill!) running.
#*****************************************************************************
# WARNING...WARNING...WARNING...WARNING...WARNING...WARNING...WARNING...
#*****************************************************************************

#
# In order to run these unit tests, there must be a file in the
# "cloudservers/tests" directory called `account.py` which contains:
#
# RS_UN = "rackspace_username"
# RS_KEY = "rackspace_API_key"
#
# __all__ =(RS_UN, RS_KEY)
#
# Nothing in this directory can be run without a valid account.py in the 
# `tests` directory.
#
# if account.py's not there (it's not included in the distro):
#   we exit, printing out the contents of README.txt
#   then re-raise the import error, terminating the test.
# else:
#   we run the test/command line app, etc.
#

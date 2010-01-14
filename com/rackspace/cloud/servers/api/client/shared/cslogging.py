#
## Copyright (c) 2010, Rackspace.
## See COPYING for details.
#

"""
Logging functions for unit tests.

Logs are kept in the .../cloudservers/tests/logs directory.

If the cloudservers package is installed into the system Python, you may or 
may not have permission to create files in that location. This is normal and, 
if you're going to be using the test suite, you would be better off installing 
using the:

    python setup.py develop

command.

This just points your Python's library path at the directory into which you've 
checked out or unzipped the Cloud Servers Service. That way, you can write 
your changes, the unit test log files, etc. back to someplace you know you 
have 'write' permission.

Default rotation is 5 i.e. 5 results kept before oldest is overwritten.

There is currently no way to change rotation schedule other than modifying 
this code. This may be addressed in a future version of this API if there's a 
good reason to do so.


"""

import os
import logging
import logging.handlers

#
## Get the full path of the current Python file (cslogging.py)
#
this_file_path = os.path.dirname( os.path.realpath( __file__ ) )

#
## The log file path is one up (..) from this file, in a subdir called 'logs'
#
LOG_FILE_PATH = os.path.join(this_file_path, "..", "logs")

#
## If the log file path doesn't exist, attempt to create it.
## Any exception is an error and probably means we can't write to the
## installation directory.  That would be normal during an install into the 
## system Python is on, for example, OS X.
#

if not os.path.exists(LOG_FILE_PATH):
    os.makedirs(LOG_FILE_PATH)

#
## Set our testing logfile name and full path
##
## This localizes our logfile to the path from which we're testing so we
## have a separate log for each testing directory.  Very handy for figuring
## out why it works so well in some plaes, but not others.
#
LOG_FILE_NAME = "cloudfiles.test.log"
LOG_FILE = os.path.join(LOG_FILE_PATH, LOG_FILE_NAME)

#
## Create a logger
#
cslogger =  logging.getLogger('cs')

#
## Make sure it captures everything up to and including DEBUG output
#
cslogger.setLevel(logging.DEBUG)

#
## Keep history of last five runs, keep 125k of debug info
#
handler = logging.handlers.RotatingFileHandler(
              LOG_FILE, maxBytes=125*1024, backupCount=5)

#
## Set formatting to something we can read
#
formatter \
    = logging.Formatter("%(levelname)s: %(message)s %(pathname)s:%(lineno)d")

#
## Make sure out logger writes to the log file
#
cslogger.addHandler(handler)


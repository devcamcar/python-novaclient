Rackspace Cloud Servers Python API
----------------------------------
Copyright (c) 2009, Rackspace.
Authors:
Steve Steiner, ssteinerX at gmail dot com.
Mike Mayo, mike.mayo@rackspace.com, twitter: @greenisus

See COPYING for details.

Welcome to the Rackspace Cloud Servers Python API!

Installation
------------
Installation requires setuptools which can be installed by following the
instructions at:

    http://pypi.python.org/pypi/setuptools

It is *highly recommended* that you do your installation by pulling the
current development version using git and installing the library in
development mode:

    # git clone git@github.com/rackspace/python-cloudservers
    # cd python-cloudservers
    # python setup.py develop

That way, as development proceeds, you can just do a:

    cd python-cloudservers
    git pull

to update to the latest release version.

This makes it very easy to keep up with the latest changes without having to
reinstall anything.

Running the End-user Test Suite
-------------------------------

The End-user Test Suite runs a set of non-destructive connection and status
type tests.  It basically checks that your Rackspace user name and API key
are valid, then shows lists of all of the servers you have running, and lists
out all of the various server flavors, images, etc.

This is not the full test suite, but it will verify that everything can
connect, that the specific version of Python you're using is supported, and
that all required modules are present.

In order to run the test suite(s), you will need nose.  Since you've already
got setuptools installed, this is as simple as:

    # easy_install nose

Depending on your OS (OS X, particularly), you may have to run easy_install
with sudo as in:

    # sudo easy_install nose

In order to run any of the tests, you must create a file called account.py,
in the cloudservers/tests directory, with the following contents:

# account.py
RS_UN = "your RS username"
RS_KEY = "your RS API key"

__all__ =(RS_UN, RS_KEY)
# end of account.py

Then, change to the cloudservers directory and type:

    nosetests com.rackspace.cloud.servers.api.client.tests.user_tests

do NOT omit the com.rackspace.cloud.servers.api.client.tests.user_tests parameter or you will be running
the full test suite which creates, destroys, and resizes many servers in your
live account.

There is a console application in the python-cloudservers/cloudservers/tests
directory named cloud_servers_console.py, which can be run by:

    # python cloud_servers_console.py

This will let you explore the API by hand and there's a little snippet of
demo code for each API call right in the app.

Bug Reports
-----------

We have an open bug tracking system at github.com/rackspace/python-cloudservers/issues

Please, before reporting bugs, we ask that you first:

    1> Pull the latest version from version control. This product is under
    heavy development and we may already have fixed your issue.

    2> If you're still having a bug, please provide a minimal test case that
    demonstrates the issue.


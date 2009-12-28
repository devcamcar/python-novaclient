"""

 cloud_servers_console

 A very simple text menu based application for showing the status of
everything in your Cloud Servers account.

 I developed this to make it simple to test the functionality of the library
as I went along and found it to be so handy I just left it in.

 Also, it shows real-world examples of the API in actual use which is always
my favorite type of documentation.

 It is purposely written in the most simple, straight-forward way without the
 types of optimizations or error handling that could be done in a production
 app in order to clearly show the simplest use of the API calls.

 NOTE: In order to actually run the console, you must create the file
account.py, in the tests directory, with the settings for your Cloud Servers
account.

 NOTE: Any servers created by this program are actual, live, working, billable
servers in the RackSpace Cloud.

 Always make sure to clean up what you're not using. If it's running, you're
paying for it!
"""

from sys import stdin, exit
from time import sleep
from functools import partial
from pprint import pprint

# NOTE: this file must be created, see testing README.txt for info
from account import RS_UN, RS_KEY

# The __init__ for com.rackspace.cloud.servers.api.client.tests creates a a CloudServersServices instance
# (named `css`) as well as one of each type of manager.  A *lot* has to go
# right for this to get past this import at all.
from com.rackspace.cloud.servers.api.client.tests import css, serverManager, flavorManager, \
                               imageManager, sharedIpGroupManager

from com.rackspace.cloud.servers.api.client.sharedipgroup import SharedIpGroup
from com.rackspace.cloud.servers.api.client.servermanager import rebootType
from com.rackspace.cloud.servers.api.client.server import Server
from com.rackspace.cloud.servers.api.client.backupschedule import BackupSchedule
from com.rackspace.cloud.servers.api.client.errors import CloudServersFault
from com.rackspace.cloud.servers.api.client.personality import Personality
from com.rackspace.cloud.servers.api.client.file import File

# All utility functions for getting input and such
from com.rackspace.cloud.servers.api.client.tests.console_util import *

#----------------------------------------
# Backup Schedule
#----------------------------------------
def showBackupSchedule():
    """
    Show server's backup schedule.
    """
    id = getServerId()

    # Find is guaranteed not to throw a not-found exception
    server = serverManager.find(id)

    if server:
        schedule = serverManager.getSchedule(server)
        print "Backup schedule of server: ", id
        print schedule
    else:
        print "Server not found"

def setBackupSchedule():
    """
    Set server's backup schedule
    """
    id = getServerId()

    # Find is guaranteed not to throw a not-found exception
    server = serverManager.find(id)

    if server:
        backupSchedule = serverManager.getSchedule(server)
        print "Backup schedule of server: ", id
        print backupSchedule
        newbs = BackupSchedule(True, daily="H_0000_0200", weekly="SUNDAY")
        serverManager.setSchedule(server, newbs)
        backupSchedule = serverManager.getSchedule(server)
        print "Backup schedule of server: ", id
        print backupSchedule
    else:
        print "Server not found"

#----------------------------------------
# Servers
#----------------------------------------
def showStatus():
    """
    Get user input of server ID just show raw status object for that id

    Shows:
        Using find() to check an ID since it will just return None and not
        raise an exception.
    """
    id = getServerId()

    # Find is guaranteed not to throw a not-found exception
    server = serverManager.find(id)

    if server:
        status = serverManager.status(id)
        print "Status of server: ", id
        pprint(status)
    else:
        print "Server not found"

def showDetails():
    """
    Get user input of server ID just show raw status object for that id

    Shows:
        Catching the 404 error by hand instead of using find()
    """
    id = getServerId()
    try:
        server = serverManager.find(id)
    except CloudServersFault, cf:
        if cf.code == 404:
            print "Server not found"
            return

    print "Server: ", server
    pprint(server)
    print "Last Modified: ", server.lastModified

def showImageDetails():
    """
    Get user input of image ID and show details
    """
    id = getImageId()
    try:
        image = imageManager.find(id)
    except CloudServersFault, cf:
        if cf.code == 404:
            print "Server not found"
            return
    print "Image: ", id
    pprint(image)
        

def deleteServer():
    """
    Get user input of server ID and delete it
    """
    id = getServerId()
    serverToDelete = serverManager.find(id)

    if not serverToDelete:  # find() returns None on failure to find server
        print "Server not found %s" % id
    else:
        pprint(serverToDelete)
        status = serverManager.remove(serverToDelete)
        pprint(status)

def rebootServer():
    """
    Reboot a server, prompting for `id`
    """
    id = getServerId()
    serverToReboot = serverManager.find(id)
    if not serverToReboot:  # find() returns None on failure to find server
        print "Server not found %s" % id
        return

    print "Hard or Soft (h/S): "
    hard_soft = stdin.readline().strip()
    if hard_soft in "Hh":
        rType  = rebootType.hard
    else:
        rType = rebootType.soft

    sleepTime = getSleepTime()  # Get sleep time to avoid overlimit fault
    serverManager.reboot(serverToReboot, rType)
    status = serverToReboot.status
    while status != u"ACTIVE":
        status = serverToReboot.status
        print "Status   : ", serverToReboot.status
        print "Progress : ", serverToReboot.progress
        print "Sleeping : ", sleepTime
        sleep(sleepTime)        # pacing to avoid overlimit fault

    print "Rebooted!"

def createServer():
    """
    Creates a server with entered name, then shows how to poll for it
    to be created.
    """
    print "Server Name to Create: "
    name = stdin.readline().strip()
    s = Server(name=name, imageId=3, flavorId=1)
    # Create doesn't return anything, but fills in the server with info
    # (including) admin p/w
    serverManager.create(s)
    pprint(s)
    print "Server is now: ", s # just to show the server with all values filled in

    sleepTime = getSleepTime()
    status = s.status
    while status == "BUILD":
        status = s.status
        print "Status   : ", s.status
        print "Progress : ", s.progress
        print "Sleeping : ", sleepTime
        sleep(sleepTime)

    print "Built!"

def createServerAndWait():
    """
    Creates a server with entered name, then uses the wait() method to poll for it
    to be created.
    """
    print "Server Name to Create: "
    name = stdin.readline().strip()
    s = Server(name=name, imageId=3, flavorId=1)
    # Create doesn't return anything, but fills in the server with info
    # (including) admin p/w
    serverManager.create(s)
    pprint(s)
    print "Server is now: ", s # just to show the server with all values filled in
    serverManager.wait(s)

    print "Built!"

def resizeServer():
    """
    Resizes a server and asks you to confirm the resize.
    """
    #id = getServerId()
    id = 127862 # sample on mike's account for faster testing

    # Find is guaranteed not to throw a not-found exception
    server = serverManager.find(id)
    if server:
        print "Server: ", server
    else:
        print "Server not found"
        
    flavorId = 2    
    if server.flavorId == 2:
        flavorId = 1
    
    print "Resizing to Flavor ID ", flavorId
    serverManager.resize(server, flavorId)
    serverManager.wait(server)
    
    print "Done!  Ready to confirm or revert?  Type confirm or revert or press enter to do nothing:"
    action = stdin.readline().strip()
    
    if action == 'confirm':
        serverManager.confirmResize(server)
        serverManager.wait(server)
    elif action == 'revert':
        serverManager.revertResize(server)
        serverManager.wait(server)
        
    print "Done!"
    print "Server: ", server

#----------------------------------------
# Shared IP Groups
#----------------------------------------
def createSharedIpGroup():
    """
    Creates a shared IP group with entered name and single server id.

    Shows:
        how to poll while waiting for a server to be created.
    """
    print "Shared IP Group Name to Create: "
    name = stdin.readline().strip()

    print "Id of first server in group: "
    server = None
    found = False
    id = 0
    while not found and id != -1:
        id = getServerId()
        server = serverManager.find(id)
        found = (server != None)

    if found:
        ipg = SharedIpGroup(name, server.id )
        # Create doesn't return anything, but fills in the ipgroup with info
        sharedIpGroupManager.create(ipg)
        print "IP group is now:"
        pprint(ipg)

def deleteSharedIpGroup(self):
    """
    Delete a shared ip group by id
    """
    print "Shared IP Group id to delete: "
    name = stdin.readline().strip()
    ipg = sharedIpGroupManager.find(id)
    if not ipg:
        print "IP Group not found"
    else:
        sharedIpGroupManager.delete(ipg)

def addServerToIpGroup():
    """
    Add server to IP Group by id
    """
    pass

def testEntityListIter():
    """
    Test EntityList iterator methods
    """
    serverList = serverManager.createList(detail=False)
    expected_length = len(serverList)

    # test python iterator
    actual_length = 0
    for server in serverList:
        actual_length += 1
    print "testing 'for server in serverList': ", 'PASS' if actual_length == expected_length else ''

    # test hasNext() and next()
    actual_length = 0
    serverList = serverManager.createList(detail=False)
    while serverList.hasNext():
        serverList.next()
        actual_length += 1
    print "testing hasNext() and next():       ", 'PASS' if actual_length == expected_length else 'FAIL'

    # test reset()
    actual_length = 0
    serverList.reset()
    for server in serverList:
        actual_length += 1
    print "testing reset():                    ", 'PASS' if actual_length == expected_length else 'FAIL'
    
def testPersonality():
    s = Server(name="test", imageId=3, flavorId=1)
    p = Personality()
    f1 = File('/usr/local/personality1', 'this is a test.  if it is legible, the test failed')
    f2 = File('/usr/local/personality2', 'this is another test.  if it is legible, the test failed')
    p.files = [f1, f2]
    s.personality = p
    print "personality: ", s.personality
    print "files:"
    for file in p.files:
        print file.path, ' ', file.contents
    print "personality in server object:"
    print s.asJSON
    print "no personality in server object:"
    s.personality = None
    print s.asJSON


choices = dict()                    # just so it's there for beatIt decl

#
# Ok, I could probably reduce this further with generators, fibrilators, etc.
# but this'll do the job and is easy enough to understand.
#
ls   = partial(lister, manager=serverManager, tag="Server")
lf   = partial(lister, manager=flavorManager, tag="Flavor")
li   = partial(lister, manager=imageManager, tag="Image")
lsip = partial(lister, manager=sharedIpGroupManager, tag="SharedIP")

# TBD:
# Store this as array, do lookup with dict

shortLineLen = 40
longLineLen = 60
sepLine = '-' * shortLineLen

def groupHeader(groupName):
    groupLen = len(groupName)
    numDashes = (longLineLen - groupLen)  / 2
    return '\n' + '-' * numDashes + ' ' + groupName + ' ' + '-' * numDashes

choicesList = (
    (groupHeader("Servers"),),
    ("ls"       , ChoiceItem("List Servers",                            lambda: ls(False))  ),
    ("lsd"      , ChoiceItem("List Servers Detail",                     lambda: ls(True))   ),
    (sepLine,),
    ("ss"       , ChoiceItem("Show Server's Status by id",              showStatus)         ),
    ("sd"       , ChoiceItem("Show Server's Details by id",             showDetails)        ),
    (sepLine,),
    ("sc"       , ChoiceItem("Create Server",                           createServer)       ),
    ("scw"      , ChoiceItem("Create Server and wait",                  createServerAndWait)),
    ("sdel"     , ChoiceItem("Delete Server by id",                     deleteServer)       ),
    ("sr"       , ChoiceItem("Reboot Server by id",                     rebootServer)       ),
    ("sresize"  , ChoiceItem("Resize Server by id",                     resizeServer)       ),
    (sepLine,),
    ("sbs"      , ChoiceItem("Show Server's Backup Schedule by id",     showBackupSchedule) ),
    ("sbsup"    , ChoiceItem("Update Server's Backup Schedule by id",   setBackupSchedule)  ),

    (groupHeader("Flavors, Images"),),
    ("lf"       , ChoiceItem("List Flavors",                            lambda: lf(False))  ),
    ("lfd"      , ChoiceItem("List Flavors (detail)",                   lambda: lf(True))   ),
    (sepLine,),
    ("li"       , ChoiceItem("List Images",                             lambda: li(False))  ),
    ("lid"      , ChoiceItem("List Images (detail)",                    lambda: li(True))   ),
    ("lidid"    , ChoiceItem("List Image Details by id",                showImageDetails)   ),

    (groupHeader("Shared IP Groups"),),
    ("lip"      , ChoiceItem("List Shared IP Groups",                   lambda: lsip(False))),
    ("lipd"     , ChoiceItem("List Shared IP Groups (detail)",          lambda: lsip(True)) ),
    ("sipc"     , ChoiceItem("Create Shared IP Group",                  createSharedIpGroup)),
    ("sipdel"   , ChoiceItem("Delete Shared IP Group",                  deleteSharedIpGroup)),
    ("sipadd"   , ChoiceItem("Add Server to Shared IP Group by id",     addServerToIpGroup) ),

    (groupHeader("Misc Account Functions"),),
    ("ll"       , ChoiceItem("List Account Limits",                     showLimits)         ),

    (groupHeader("Misc Functions"),),
    ("iter"     , ChoiceItem("Test EntityList iterator",                testEntityListIter) ),
    ("pers"     , ChoiceItem("Server Personality get/set",              testPersonality)    ),

    (groupHeader("Quit"),),
    ("q"        , ChoiceItem("quit",                                    lambda: exit(0))    ),
    (sepLine,),
)

#
# Create dictionary for lookups
#
lookupDict = dict()
for choice in choicesList:
    if not '-' in choice[0]:        # skip our separators
        lookupDict[choice[0]] = choice[1]

#
# Get input from user, execute selected function
#   until interrupted by 'q' or Ctrl-C
#
slcu = "Servers Listing Console Utility"

choice = ""
while 1:
    if choice in lookupDict:
        lookupDict[choice].func()
    else:
        printChoices(choicesList)

    choice = raw_input("Command (enter to show menu...)")

    if choice == "q":
        print "Bye!"
        exit(0)

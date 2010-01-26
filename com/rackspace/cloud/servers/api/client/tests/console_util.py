#----------------------------------------------------------------------------
# console_util.py
#
# A very simple set of utilities for creating text menu based applications for
# simple manual testing.
#
# Developed to assist with the *_console.py test programs that are in the
# test directory but not really part of the "Test Suite" per se.
#----------------------------------------------------------------------------

from sys import stdin, exit
from functools import partial

# The __init__ for com.rackspace.cloud.servers.api.client.tests creates a 
# CloudServersServices instance (named `css`) as well as one of each type of 
# manager.  A *lot* has to go right for this to get past this import at all.
from com.rackspace.cloud.servers.api.client.tests import css, serverManager, \
                            flavorManager, imageManager, sharedIpGroupManager

#
# Choices for our fancy menu system
#
class ChoiceItem(object):
    """
    A prompt and a function to call
    """
    def __init__(self, prompt, func):
        """
        Create a choiceItem
        """
        self.prompt = prompt
        self.func = func

def getId(idType, showId=True):
    if showId == True:
        print idType + " ID: "
    else:
        print idType + ": "
    id = stdin.readline().strip()
    if id == "":    # If they leave it blank, just bail returning -1
        return -1

    # don't mind if it's not numeric
    # try:
    #     id = int(id)
    # except ValueError, e:
    #     print "ValueError : ", e
    #     id = -1
    return id
    
def getServerId():
    return getId("Server")

def getImageId():
    return getId("Image")

def getFlavorId():
    return getId("Flavor")
    
def getSharedIpGroupId():
    return getId("Shared IP Group")

def getIpAddress():
    return getId("IP Address", showId=False)

def printChoices(choices):
    """
    Print all of the choices, one per line, nicely formatted
    """
    for c in choices:
        # Print the whole thing if it's not a separator, else print separator
        if not '-' in c[0]:
            print "%-8s - %s" % (c[0], c[1].prompt)
        else:
            print c[0]

def getSleepTime():
    """
    Computes sleep time for polling operations
    """

    # Now, get the limits for our account to pace our "busy waiting"
    limits = css.serviceInfoLimits
    print "Limits are: ", limits

    queriesRateRecord =  limits["rate"][1]        
    queriesPerMinute = queriesRateRecord["value"] 

    sleepTime = 60/queriesPerMinute

    return sleepTime

#
# Generic Lister
#
def lister(detail, manager, tag):
    """
    List using:
        `manager`   manager to use to create the list
        `tag`       string to show what's being listed
        `detail`    whether to show detail or not
    """
    theList = (manager).createList(detail)
    
    print "%s List of %ss" %(detail and "Detailed" or "Quick", tag)
    
    print "List length: ", len(theList)
    
    for item in theList:
        print "id=%s" % (item.id,)
        if detail:
            print repr(item)
        else:
            print str(item)

        print

def showLimits():
    """
    Just show account limits
    """
    limits = css.serviceInfo.limits
    print limits

def notimp():
    print "Not implemented, yet..."


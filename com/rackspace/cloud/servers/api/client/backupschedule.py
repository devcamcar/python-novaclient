# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
BackupSchedule object
"""
from com.rackspace.cloud.servers.api.client.jsonwrapper import json

"""
Weekly Backup Schedule / Daily Backup Schedule dictionaries.

These are just used to keep requests to set the schedule honest i.e. if the
key's not found in wbs/dbs, it's not a valid value and needs to raise an
exception rather than pass bad data to the server.
"""

# Weekly Backup Schedule.
wbs = {
    "DISABLED":     "Weekly backup disabled",
    "SUNDAY":       "Sunday",
    "MONDAY":       "Monday",
    "TUESDAY":      "Tuesday",
    "WEDNESDAY":    "Wednesday",
    "THURSDAY":     "Thursday",
    "FRIDAY":       "Friday",
    "SATURDAY":     "Saturday",
}


# Daily Backup Schedule
dbs = {
    "DISABLED"   :             "Daily backups disabled",
    "H_0000_0200":             "0000-0200",
    "H_0200_0400":             "0200-0400",
    "H_0400_0600":             "0400-0600",
    "H_0600_0800":             "0600-0800",
    "H_0800_1000":             "0800-1000",
    "H_1000_1200":             "1000-1200",
    "H_1200_1400":             "1200-1400",
    "H_1400_1600":             "1400-1600",
    "H_1600_1800":             "1600-1800",
    "H_1800_2000":             "1800-2000",
    "H_2000_2200":             "2000-2200",
    "H_2200_0000":             "2200-0000",
}

class BackupSchedule(object):
    """
    Backup schedule objects.
    """
    def __init__(self, enabled=False, daily="", weekly=""):
        """
        Create new BackupSchedule instance with specified enabled, weekly,
        and daily settings.
        """
        self._enabled = enabled
        self._daily   = daily
        self._weekly  = weekly

    def __str__(self):
        return "Enabled = %s : Daily = %s : Weekly = %s" % (self._enabled, \
                                                            self._daily, \
                                                            self._weekly)

    def get_enabled(self):
        """Whether or not backups are enabled for this server."""
        return self._enabled

    def set_enabled(self, value):
        # TBD: is this supposed to follow weekly & daily != "DISABLED" ?
        self._enabled = value
    enabled = property(get_enabled, set_enabled)

    def get_weekly(self):
        return self._weekly

    def set_weekly(self, value):
        if value in wbs:
            self._weekly = value
        else:
            raise InvalidArgumentsFault("Bad value %s passed for weekly\
                                         backup", value)
    weekly = property(get_weekly, set_weekly)

    def get_daily(self):
        return self._daily

    def set_daily(self, value):
        if value in dbs:
            self._daily = value
        else:
            raise InvalidArgumentsFault("Bad value %s passed for daily\
                                         backup", value)
    daily = property(get_daily, set_daily)

    @property
    def asDict(self):
        """
        Return backup schedule object with attributes as a dictionary
        """
        bsAsDict = { "backupSchedule" :
                        {
                            "enabled"   : self._enabled,
                            "weekly"    : self.weekly,
                            "daily"     : self.daily,
                        }
                     }
        return bsAsDict

    @property
    def asJSON(self):
        """
        Return the backup schedule object converted to JSON
        """
        serverAsJSON = json.dumps(self.asDict)
        return serverAsJSON

    def initFromResultDict(self, dic):
        """
        Fills up a BackupSchedule object from the dictionary returned from a
        get backup schedule query of the API
        """
        # dic will be None when e.g. a find() fails.
        if dic:
            self._daily   = dic['daily']
            self._weekly  = dic['weekly']
            self._enabled = dic['enabled']


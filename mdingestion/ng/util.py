import datetime
import time

import logging


def remove_duplicates_from_list(a_list):
    return list(dict.fromkeys(a_list))

def utc2seconds(dt):
    """
    converts datetime to seconds since year 0

    Copyright (C) 2015 Heinrich Widmann.
    Licensed under AGPLv3.
    """
    year1epochsec=62135600400
    utc1900=datetime.datetime.strptime("1900-01-01T11:59:59Z", "%Y-%m-%dT%H:%M:%SZ")
    # print(f"utc900={utc1900}")
    # utc=self.date2UTC(dt)
    utc = dt
    # print(f"utc={utc}")
    try:
       utctime = datetime.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
       # print(f"utctime={utctime}")
       diff = utc1900 - utctime
       # print(f"diff={diff}")
       diffsec= int(diff.days) * 24 * 60 *60
       if diff > datetime.timedelta(0): ## date is before 1900
          sec=int(time.mktime((utc1900).timetuple()))-diffsec+year1epochsec
       else:
          sec=int(time.mktime(utctime.timetuple()))+year1epochsec
    except Exception as err :
       logging.exception(f'utc2seconds date-time {utc} can not converted!')
       return None
    return sec

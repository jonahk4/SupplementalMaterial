"""Configuration for cooldowns on commands."""
import datetime


def getdifference(t1):
  t2 = datetime.datetime.utcnow()
  timetoformat = t1
  timestringformat = timetoformat.split("-")
  year = timestringformat[0]
  month = timestringformat[1]
  othertimestring = timestringformat[2].split(" ")
  day = othertimestring[0]
  timestring = othertimestring[1].split(":")
  hour = timestring[0]
  minute = timestring[1]
  t1 = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
  t2 = datetime.datetime.utcnow()
  tdelta = t2 - t1
  seconds = tdelta.total_seconds()
  return seconds
#!/usr/bin/python3
import sys
last_second = 4
seconds = float(sys.argv[1])
seconds -= last_second
seconds = int(seconds)
hours = seconds // 3600
seconds -= hours * 3600
minutes = seconds // 60
seconds -= minutes * 60
hours = '0' + str(hours) if hours < 10 else str(hours)
minutes = '0' + str(minutes) if minutes < 10 else str(minutes)
seconds = '0' + str(seconds) if seconds < 10 else str(seconds)
print("{0}:{1}:{2}".format(hours, minutes, seconds))
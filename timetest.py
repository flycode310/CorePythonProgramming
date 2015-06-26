#! /usr/bin/env python

import time
import datetime

time1 = datetime.datetime.now()
time.sleep(3)
time2 = datetime.datetime.now()

print (time2 - time1).microseconds

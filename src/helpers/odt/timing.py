"""
    A file with methods for calculating the running time of scripts.
"""

import atexit
import time
from functools import reduce

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
           reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                  [(t*1000,), 1000, 60, 60])

line = "="*40
def log(s, elapsed=None):
    print(line)
    print(secondsToStr(time.process_time()), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)

def endlog():
    end = time.process_time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

def now():
    return secondsToStr(time.process_time())

start = time.process_time()
atexit.register(endlog)
log("Start Program")
#!/usr/bin/env python3

import re
import time
import sys

log = open("/home/trick/.fldigi/fldigi20190304.log", "r")
# TODO: if file is quite large, seek to the last few hundred lines or so

recent = []

rx_match = re.compile("^RX \d+ : RTTY \(.*\): (\$\$EAGLE.*\*....)$")
#rx_match = re.compile("^RX")

def clear_screen():
    sys.stdout.write("\033[2J")

last_matches = []
partial = ""

while True:
    # read some data
    position = log.tell()
    line = log.readline()
    if not line:
        time.sleep(1)

    # decide if it's a partial line or not
    if line.count("\n") == 0:
        partial = line.strip()
        log.seek(position)
        time.sleep(0.1)
    else:
        # if it's a full line, match it
        line = line.strip()

        if rx_match.match(line):
            partial = ""
            #print("MATCH   : ", line)
            if len(last_matches) > 10:
                last_matches = last_matches[1:]
            last_matches.append(line)
        else:
            # what to do with non-matching lines?
            pass

    # now print all of the output assuming the screen is clear
    for x in last_matches:
        print(x)
    print("Partial: ", partial)
    clear_screen()

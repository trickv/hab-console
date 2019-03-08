#!/usr/bin/env python3

import re
import time
import sys

log = open("/home/trick/.fldigi/fldigi20190304.log", "r")
# TODO: if file is quite large, seek to the last few hundred lines or so

recent = []

rx_match = re.compile("^RX \d+ : RTTY \(.*\): (?P<sentence>\$\$EAGLE.*\*....)$")
eagle_nofix_sentence = re.compile("^\$\$EAGLE,(?P<sequence>\d+),NOFIX,(?P<time>\d\d\:\d\d\:\d\d),0,0,0,(?P<numsats>\d+),(?P<temperature>\d+\.\d+),(?P<pressure>\d+\.\d),(?P<humidity>\d+\.\d),(?P<uptime>\d+),(?P<internaltemperature>\d+\.\d),(?P<voltage>\d+\.\d+),(?P<current>-?\d+)\*....$")
#rx_match = re.compile("^RX")

def clear_screen():
    sys.stdout.write("\033[2J")


good_data = []
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

        result = rx_match.match(line)
        if result:
            partial = ""
            #print("MATCH   : ", line)
            if len(last_matches) > 10:
                last_matches = last_matches[1:]
            last_matches.append(line)

            parse_result = eagle_nofix_sentence.match(result.group("sentence"))
            if parse_result:
                if len(good_data) > 4:
                    good_data = good_data[1:]
                good_data.append(parse_result)
        else:
            # what to do with non-matching lines?
            pass

    # now print all of the output assuming the screen is clear
    for y in good_data:
        print(y.group(0))
        print(y.group("sequence"))
    print(".")
    for x in last_matches:
        print(x)
    print("Partial: ", partial)
    clear_screen()

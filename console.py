#!/usr/bin/env python3

import re
import time
import sys

log = open("/home/trick/.fldigi/fldigi20190304.log", "r")
# TODO: if file is quite large, seek to the last few hundred lines or so

recent = []

rx_match = re.compile("^RX \d+ : RTTY \(.*\): (\$\$EAGLE.*\*....)$")
#rx_match = re.compile("^RX")

while True:
    position = log.tell()
    line = log.readline()
    if not line:
        time.sleep(1)
    if line.count("\n") == 0:
        print(" . . .  : ", line)
        log.seek(position)
        time.sleep(0.1)
        sys.stdout.write("\033[F") # Cursor up one line
        sys.stdout.write("\033[K") # Clear to the end of line
        continue
    line = line.strip()
    if rx_match.match(line):
        print("MATCH   : ", line)
    else:
        print("        : ", line)

#!/usr/bin/env python3

import sys

for line in sys.stdin:
    if line.startswith("#"):
        continue
    
    line = line.strip().split("\t", 1)

    if len(line) < 2:
        print('%s\t%s' % ("$Search_Movie", line[0].lower()))
    
    else:
        print('%s\t%s' % (line[0], line[1]))


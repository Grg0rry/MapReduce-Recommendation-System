#!/usr/bin/env python3

import sys

last_MovieID = ""

for line in sys.stdin:
    line = line.strip().split("\t", 1)
    
    MovieID = int(line[0])

    if last_MovieID != MovieID:
        print('%s\t%s' % (MovieID, ""))

    last_MovieID = MovieID


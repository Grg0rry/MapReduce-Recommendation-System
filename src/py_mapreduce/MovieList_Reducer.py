#!/usr/bin/env python3

import sys

last_MovieTitle = ""

for line in sys.stdin:
    line = line.strip().split("\t", 1)
    
    MovieTitle = line[0]

    if last_MovieTitle != MovieTitle:
        print('%s\t%s' % (MovieTitle, ""))

    last_MovieTitle = MovieTitle


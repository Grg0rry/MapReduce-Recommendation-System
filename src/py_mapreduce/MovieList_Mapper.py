#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip().split(",", 2)

    if len(line) < 3:
        continue

    MovieTitle = line[0]

    print('%s\t%s' % (MovieTitle, ""))
#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip().split(",", 2)

    Movietitle = int(line[0])

    print('%s\t%s' % (Movietitle, ""))
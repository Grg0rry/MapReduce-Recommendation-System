#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip().split(",", 2)

    UserID = int(line[1])

    print('%s\t%s' % (UserID, ""))
#!/usr/bin/env python3

import sys

for line in sys.stdin:
    if line.startswith("$Search_Key"):
        print('%s\t%s' % ("$Search_Key", line.strip().split(",")[1]))

    else:
        line = line.strip().split('\t', 1)
        print('%s\t%s' % (line[0], line[1]))

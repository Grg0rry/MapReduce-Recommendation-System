#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip().split('\t', 1)
    
    print('%s\t%s' % (line[0], line[1]))

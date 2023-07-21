#!/usr/bin/python3

import sys, math

for line in sys.stdin:
    line = line.strip().split('\t', 1)

    MovieTitle = line[0]
    vector = line[1][1:-1].split(',')
    length = math.sqrt(sum(v**2 for v in vector))
    normalized_vector = [v / length for v in vector]

    print('%s\t%s' % (MovieTitle, normalized_vector))
